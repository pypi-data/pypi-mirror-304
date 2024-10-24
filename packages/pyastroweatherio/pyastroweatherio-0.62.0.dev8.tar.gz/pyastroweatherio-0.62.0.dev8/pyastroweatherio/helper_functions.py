"""Contains Helper functions for AstroWeather."""

import logging
import math
from datetime import UTC, datetime, timedelta
from math import degrees as deg

import ephem
from ephem import degree
from zoneinfo import ZoneInfo

# import metpy.calc as mpcalc
# from metpy.units import units
# import numpy as np
from pyastroweatherio.const import (
    ASTRONOMICAL_DUSK_DAWN,
    CIVIL_DUSK_DAWN,
    MAG_DEGRATION_MAX,
    NAUTICAL_DUSK_DAWN,
    SEEING_MAX,
)

# from pyastroweatherio.models import DarknessDataModel, MoonDataModel, SunDataModel
from pyastroweatherio.dataclasses import (
    DarknessData,
    DarknessDataModel,
    MoonData,
    MoonDataModel,
    SunData,
    SunDataModel,
)

_LOGGER = logging.getLogger(__name__)


class ConversionFunctions:
    """Convert between different units."""

    async def epoch_to_datetime(self, value) -> str:
        """Converts EPOC time to Date Time String."""

        return datetime.datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")

    async def anchor_timestamp(self, value) -> datetime:
        """Converts the datetime string from 7Timer to DateTime."""

        return datetime.strptime(value, "%Y%m%d%H")


class AtmosphericRoutines:
    """Calculate atmospheric attributes."""

    def __init__(
        self,
    ):
        _LOGGER.debug("AtmosphericRoutines calculation mode active")

        # Relative humidity (0.0 to 1.0)
        # Temperature in Celsius
        # Cloud cover fraction (0.0 to 1.0)
        # Wind speed in meters per second
        # Humidity in percent
        # Altitude in meters
        # Dew point temperature in Celsius
        # Air pressure at sea level in hPa
        # aerosol_density in kg/m^3

    # #####################################################
    # Calculate lifted index
    # #####################################################
    async def calculate_lifted_index(self, temperature, altitude, dew_point_temperature, air_pressure_at_sea_level):
        """Calculate atmospheric lifted index."""
        # https://en.wikipedia.org/wiki/Lifted_index

        if not all(
            v is not None
            for v in [
                temperature,
                altitude,
                dew_point_temperature,
                air_pressure_at_sea_level,
            ]
        ):
            return None

        # Constants
        env_temp_500mb = -20  # Celsius (environmental temperature at 500 mb level)

        # Calculate saturation vapor pressure at surface temperature
        # Checked with https://www.weather.gov/epz/wxcalc_vaporpressure
        es = self._calculate_vapor_pressure(temperature)

        # Calculate actual Vapor Pressure at surface
        # Checked with https://www.weather.gov/epz/wxcalc_vaporpressure
        e = self._calculate_vapor_pressure(dew_point_temperature)  # 6.112 * (10 ** (7.5 * (Td - Tn) / (Td - 35.85)))

        # Calculate Mixing Ratio at Surface in grams per kilogram
        # Checked with https://www.weather.gov/epz/wxcalc_mixingratio
        w = self._calculate_mixing_ratio(e, air_pressure_at_sea_level)

        # Calculate Lifting Condensation Level
        lcl = self._calculate_lifting_condensation_level(w, air_pressure_at_sea_level)

        # Calculate temperature of lifted parcel at 500 mb level
        lifted_temp_500mb = (
            env_temp_500mb + (temperature - lcl) * 0.5
        )  # Assumption: 500 mb is halfway through the troposphere

        # Calculate Lifted Index
        lifted_index = (env_temp_500mb - lifted_temp_500mb) * 2 + 7

        # Ensure lifted index is within the valid range [-7, 7]
        lifted_index = max(-7, min(7, lifted_index))

        # _LOGGER.debug(f"Vapor Pressure: {e}")
        # _LOGGER.debug(f"Mixing Ratio: {w}")
        # _LOGGER.debug(f"Lifting Condensation Level: {lcl}")
        # _LOGGER.debug(f"Temperature of Lifted Parcel: {lifted_temp_500mb}")
        # _LOGGER.debug(f"Lifted Index: {lifted_index}")

        return lifted_index

    # #####################################################
    # Calculate magniture degradation based on transparency
    # #####################################################
    async def magnitude_degradation(
        self,
        temperature,
        humidity,
        cloud_cover,
        wind_speed,
        altitude,
        dew_point_temperature,
        air_pressure_at_sea_level,
    ):
        """
        Calculates the magnitude_degradation of the atmosphere.
        This algorithm first calculates the lifted index and the seeing and uses them to calculate
        the transparency from which the magnitude degradation is derived from.

        Args:
        - temperature: Surface temperature in Celsius.
        - humidity: Humidity in Percent.
        - dew_point_temperature: Dew point temperature in Celsius.
        - wind_speed: Wind speed in meters per second.
        - altitude: Altitude in meters.
        - air_pressure_at_sea_level: Air pressure at sea level.
        - cloud_cover: Cloud cover in Percent.
        - lifted_index:
        - seeing:

        Returns:
        - seeing: In Arcsecs
        """

        if not all(
            v is not None
            for v in [
                temperature,
                humidity,
                cloud_cover,
                wind_speed,
                altitude,
                dew_point_temperature,
                air_pressure_at_sea_level,
            ]
        ):
            return None

        lifted_index = await self.calculate_lifted_index(
            temperature, altitude, dew_point_temperature, air_pressure_at_sea_level
        )
        seeing = await self.calculate_seeing(
            temperature,
            humidity,
            dew_point_temperature,
            wind_speed,
            cloud_cover,
            altitude,
            air_pressure_at_sea_level,
        )

        # Calculate transparency
        transparency = self._calculate_transparency(
            humidity,
            temperature,
            cloud_cover,
            wind_speed,
            altitude,
            dew_point_temperature,
            air_pressure_at_sea_level,
            lifted_index,
            seeing,
        )

        # Convert transparency to magnitude degradation
        magnitude_degradation = self._transparency_to_magnitude_degradation(transparency)

        # _LOGGER.debug(
        #     "Magnitude Degradation: {:.2f} mag (".format(magnitude_degradation)
        #     + "Lifted Index (LI): {:.2f} °C, ".format(lifted_index)
        #     + "Seeing: {:.2f} arcsec, ".format(seeing)
        #     + "Estimated Atmospheric Transparency: {:.2f})".format(transparency)
        # )

        return magnitude_degradation

    # #####################################################
    # Calculate atmospheric seeing
    # #####################################################
    # Modell 6:
    # This algorithm first calculates the seeing factor based on temperature, humidity, wind speed
    # and altitude above sea level. It is similar to Model 4 and 5 but uses the air pressure at sea level
    # and dew point provided by Met.no.
    async def calculate_seeing(
        self,
        temperature,
        humidity,
        dew_point_temperature,
        wind_speed,
        cloud_cover,
        altitude,
        air_pressure_at_sea_level,
    ):
        """
        Calculated seeing of the atmosphere. This algorithm first calculates the seeing factor based on temperature,
        humidity, wind speed and altitude above sea level. The seeing factor is then used to calculate the astronomical
        seeing in arcseconds. The empirical relationship used here states that the seeing in arcseconds is approximately
        equal to the reciprocal of the seeing factor multiplied by a conversion factor of 0.98.

        Used by: magnitude degradation

        Args:
        - temperature: Surface temperature in Celsius.
        - humidity: Humidity in Percent.
        - dew_point_temperature: Dew point temperature in Celsius.
        - wind_speed: Wind speed in meters per second.
        - cloud_cover: Cloud cover in Percent.
        - altitude: Altitude in meters.
        - air_pressure_at_sea_level: Air pressure at sea level.

        Returns:
        - seeing: In Arcsecs

        Flow:
        - _calculate_water_vapor_pressure
        - adjusted_pressure
        - relative_pressure
        - seeing_factor
        - seeing
        """

        if not all(
            v is not None
            for v in [
                temperature,
                humidity,
                dew_point_temperature,
                wind_speed,
                cloud_cover,
                altitude,
                air_pressure_at_sea_level,
            ]
        ):
            return None

        # Constants
        C = 6.5  # 1.7

        water_vapor_pressure = self._calculate_water_vapor_pressure(dew_point_temperature, humidity)

        # adjusted_pressure = air_pressure_at_sea_level * math.exp(-0.00012 * altitude)
        adjusted_pressure = self._calculate_adjusted_pressure(air_pressure_at_sea_level, altitude)
        relative_pressure = adjusted_pressure / air_pressure_at_sea_level

        seeing_factor = C * (water_vapor_pressure / 10) ** 0.25 * (wind_speed / 10) ** 0.75 * relative_pressure
        seeing = 0.98 / seeing_factor

        # _LOGGER.debug(
        #     "Seeing: {:.2f} arcsec (".format(seeing)
        #     + "Water Vapor Pressure: {:.2f} mbar, ".format(water_vapor_pressure)
        #     + "Wind Speed: {:.2f} m/s, ".format(wind_speed)
        #     + "Relative Pressure: {:.2f} mbar, ".format(relative_pressure)
        #     + "Seeing Factor: {:.2f})".format(seeing_factor)
        # )

        if seeing > SEEING_MAX:
            seeing = SEEING_MAX  # max out seeing

        return seeing

    # #####################################################
    # Atmospheric calculations
    # #####################################################
    def _calculate_adjusted_pressure(self, pressure_sea_level, altitude):
        """
        Calculate the adjusted pressure at a given altitude above sea level.
        """

        lapse_rate = -0.0065  # Temperature lapse rate in K/m
        temperature_sea_level = 288.15  # Temperature at sea level in K
        gravity = 9.80665  # Acceleration due to gravity in m/s^2
        molar_mass_air = 0.02896  # Molar mass of Earth's air in kg/mol
        gas_constant = 8.31447  # Universal gas constant in J/(mol*K)

        pressure_adjusted = pressure_sea_level * (1 - (lapse_rate * altitude) / temperature_sea_level) ** (
            (gravity * molar_mass_air) / (gas_constant * lapse_rate)
        )

        return pressure_adjusted

    def _calculate_vapor_pressure(self, temperature):
        """
        Calculate the actual or saturation vapor pressure at the surface using the Magnus-Tetens formula.
        If the surface temperature is given, the actual vapor pressure is calculated.
        The dew point temperature calculates ths saturation vapor pressure.

        Used by: lifted index, seeing

        Args:
        - temperature: Surface or dew point temperature in Celsius.

        Returns:
        - e: Actual vapor pressure at the surface in millibars (mb) or hectopascals (hPa).

        Magnus coefficients:

        Temperatures in between -45°C bis 60°C:
            a=17.62
            b=243.12
        Temperatures in between 0°C bis 100°C:
            a=7.5
            b=237.7
        Temperatures in between -10°C bis 50°C:
            a=17.27
            b=237.7
        """
        # # Constants
        # A = 17.62
        # B = 243.12

        # # Monteith and Unsworth (2008) provide Tetens' formula for temperatures above 0 °C
        A = 17.27
        B = 237.3

        # Murray (1967) provides Tetens' equation for temperatures below 0 °C
        # A = 21.875
        # B = 265.5

        # Calculate vapor pressure using Magnus-Tetens formula
        e = 0.61078 * math.exp((A * temperature) / (temperature + B))

        return e

    def _calculate_water_vapor_pressure(self, dew_point_temperature, humidity):
        """
        Calculate the water vapor pressure based on temperature and humiditye.

        Used by: seeing

        Args:
        - dew_point_temperature: Dew point temperature in Celsius.
        - humidity: Humidity in Percent.

        Returns:
        - water_vapor_pressure: Water vapor pressure at the surface in millibars (mb) or hectopascals (hPa).
        """

        es = self._calculate_vapor_pressure(dew_point_temperature)
        water_vapor_pressure = (humidity / 100) * es

        return water_vapor_pressure

    def _calculate_mixing_ratio(self, e, air_pressure_at_sea_level):
        """
        Calculate the mixing ratio.

        Used by: lifted index

        Args:
        - e: Vapor pressure
        - air_pressure_at_sea_level: Air pressure at sea level

        Returns:
        - w: mixing ratio at surface in grams per kilogram
        """

        # Constants
        A = 621.97

        # Calculate actual vapor pressure using Magnus-Tetens formula
        w = A * (e / (air_pressure_at_sea_level - e))

        return w

    def _calculate_lifting_condensation_level(self, w, air_pressure_at_sea_level):
        """
        The Lifting Condensation Level is the level at which a parcel becomes saturated. It can be used as
        a reasonable estimate of cloud base height when parcels experience forced ascent.
        Here, we calculate it using the Clausius-Clapeyron equation. This equation relates the saturation vapor
        pressure (e) to the temperature and pressure.
        https://en.wikipedia.org/wiki/Lifted_condensation_level

        Used by: lifted index

        Args:
        - w: Mixing ratio
        - air_pressure_at_sea_level: Air pressure at sea level

        Returns:
        - lcl: LCL in meters
        """

        # Constants
        A = 2440
        B = 0.00029

        # Calculate Lifting Condensation Level using the Clausius-Clapeyron equation
        lcl = (A * w) / ((air_pressure_at_sea_level - w) * (1 - B * air_pressure_at_sea_level))

        return lcl

    def _calculate_transparency(
        self,
        humidity,
        temperature,
        cloud_cover,
        wind_speed,
        altitude,
        dew_point_temperature,
        air_pressure_at_sea_level,
        lifted_index,
        seeing,
    ):
        """
        The transparency of the atmosphere calculated by a weighted sum of conditions.

        Used by: magnitude degradation

        Args:
        - humidity: Humidity in Percent.
        - temperature: Surface temperature in Celsius.
        - cloud_cover: Cloud cover in Percent.
        - wind_speed: Wind speed in meters per second.
        - altitude: Altitude in meters.
        - dew_point_temperature: Dew point temperature in Celsius.
        - air_pressure_at_sea_level: Air pressure at sea level.
        - lifted_index: Lifted index in Celsius.
        - seeing: Seeing in Arcsecs.
        - w: Mixing ratio

        Returns:
        - transparency: In the range of 0 to 1
        """

        # Coefficients for the linear model (you can adjust these based on your requirements)
        temp_weight = 0.10
        humidity_weight = 0.10
        wind_weight = 0.10
        dew_point_weight = 0.10
        lifted_index_weight = 0.15
        seeing_weight = 0.15
        pressure_weight = 0.10
        cloud_cover_weight = 0.10
        altitude_weight = 0.10

        # Normalize values (optional)
        # Assuming typical temperature range from -10°C to 40°C
        temp_normalized = (temperature - (-10)) / (40 - (-10))
        humidity_normalized = humidity / 100.0
        # Assuming maximum typical wind speed as 20 m/s
        wind_normalized = wind_speed / 20.0
        # Assuming typical dew point range from -10°C to 30°C
        dew_point_normalized = (dew_point_temperature - (-10)) / (30 - (-10))
        # Assuming lifted index range from -8 to 8
        lifted_index_normalized = (lifted_index + 8) / 16.0
        # Assuming typical seeing conditions from 0 to 10 arcseconds
        seeing_normalized = (10 - seeing) / 10.0
        # Assuming typical pressure range from 900 to 1100 mb
        pressure_normalized = (air_pressure_at_sea_level - 900) / (1100 - 900)
        cloud_cover_normalized = cloud_cover / 100.0
        # Assuming typical altitude range from 0 to 5000 meters
        altitude_normalized = altitude / 5000.0

        transparency = 1 - (
            temp_weight * temp_normalized
            + humidity_weight * humidity_normalized
            + wind_weight * wind_normalized
            + dew_point_weight * dew_point_normalized
            + lifted_index_weight * lifted_index_normalized
            + seeing_weight * seeing_normalized
            + pressure_weight * pressure_normalized
            + cloud_cover_weight * cloud_cover_normalized
            + altitude_weight * altitude_normalized
        )

        # Ensure transparency is within the valid range [0, 1]
        transparency = max(0, min(1, transparency))

        return transparency

    def _transparency_to_magnitude_degradation(self, transparency):
        """
        The magnitude degradation based on the atmospheric transparency.

        Used by: magnitude degradation

        Args:
        - transparency: In the range of 0 to 1.

        Returns:
        - magniture_degradation: In magnitude.
        """

        if transparency == 0:
            return float(MAG_DEGRATION_MAX)
        magnitude_degradation = -MAG_DEGRATION_MAX * math.log(transparency)
        magnitude_degradation = max(0, min(MAG_DEGRATION_MAX, magnitude_degradation))

        return magnitude_degradation


class AstronomicalRoutines:
    """Calculate different astronomical objects."""

    def __init__(
        self,
        location_data,
        forecast_time=None,
    ):
        self._location_data = location_data
        self._test_mode = False

        _LOGGER.debug("Timezone: %s", self._location_data.timezone_info)
        if forecast_time is None:
            self._forecast_time = datetime.now(UTC).replace(tzinfo=UTC)
        else:
            self._forecast_time = forecast_time.replace(tzinfo=UTC)
            self._test_mode = True

        self._sun_observer = None
        self._sun_observer_nautical = None
        self._sun_observer_astro = None
        self._moon_observer = None
        self._sun = None
        self._moon = None
        self._sun_data = {}
        self._moon_data = {}
        self._darkness_data = {}

        # Internal only
        self._sun_previous_rising_astro = None
        self._sun_previous_setting_astro = None

    def _test_data(self, data, keys) -> bool:
        """Test that specific values in a dictionary are not None"""

        if not all(data[key] is not None for key in keys):
            return False
        return True

    def utc_to_local_diff(self):
        """Returns the UTC Offset."""

        # Get the current time in the specified timezone
        now = datetime.now(ZoneInfo(self._location_data.timezone_info))

        # Get the offset in seconds
        offset_seconds = now.utcoffset().total_seconds()

        # Convert the offset to hours
        return offset_seconds / 3600

    async def time_shift(self) -> int:
        """Returns the time_shift to UTC."""

        return int(self.utc_to_local_diff() * 3600)

    async def need_update(self, forecast_time=None):
        """Update Sun and Moon."""

        if forecast_time is not None:
            self._forecast_time = forecast_time.replace(tzinfo=UTC)

        _LOGGER.debug("Astronomical calculations updating")
        self._calculate_sun()
        self._calculate_moon()

    #
    # Observers
    #
    def _get_sun_observer(self, below_horizon=ASTRONOMICAL_DUSK_DAWN) -> ephem.Observer:
        """Retrieves the ephem sun observer for the current location."""

        observer = ephem.Observer()
        observer.lon = str(self._location_data.longitude)  # * degree
        observer.lat = str(self._location_data.latitude)  # * degree
        observer.elevation = self._location_data.elevation
        observer.horizon = below_horizon * degree
        observer.pressure = 0
        observer.epoch = datetime.now().strftime("%Y/%m/%d")
        return observer

    def _get_moon_observer(self) -> ephem.Observer:
        """Retrieves the ephem mon observer for the current location."""

        observer = ephem.Observer()
        observer.lon = str(self._location_data.longitude)  # * degree
        observer.lat = str(self._location_data.latitude)  # * degree
        observer.elevation = self._location_data.elevation
        # Naval Observatory Risings and Settings
        # Set horizon to minus 34 arcminutes
        # https://aa.usno.navy.mil/data/RS_OneDay
        observer.horizon = "-0:34"
        observer.pressure = 0
        observer.epoch = datetime.now().strftime("%Y/%m/%d")
        return observer

    # #########################################################################
    # Sun
    # #########################################################################
    async def sun_data(self) -> dict:
        """Returns sun data."""

        sd = SunDataModel(self._sun_data)
        try:

            return SunData(data=sd)
        except TypeError as ve:
            _LOGGER.error(f"Failed to parse Sun data: {self._sun_data}")
            _LOGGER.error(ve)
            return None

    async def sun_next_rising(self) -> datetime:
        """Returns sun next rising."""

        if (
            not self._test_data(
                self._sun_data,
                ["next_rising_astro", "next_rising_nautical", "next_rising_civil"],
            )
            or self._forecast_time > self._sun_data["next_rising_astro"]
            or self._forecast_time > self._sun_data["next_rising_nautical"]
            or self._forecast_time > self._sun_data["next_rising_civil"]
        ):
            _LOGGER.debug("Astronomical calculations updating sun_next_rising")
            self._calculate_sun()

        if self._sun_data.get("next_rising_astro", None) is not None:
            return self._sun_data["next_rising_astro"]
        if self._sun_data.get("next_rising_nautical", None) is not None:
            return self._sun_data["next_rising_nautical"]
        if self._sun_data.get("next_rising_civil", None) is not None:
            return self._sun_data["next_rising_civil"]

    async def sun_next_setting(self) -> datetime:
        """Returns sun next setting."""

        if (
            not self._test_data(
                self._sun_data,
                ["next_rising_astro", "next_rising_nautical", "next_rising_civil"],
            )
            or self._forecast_time > self._sun_data["next_setting_astro"]
            or self._forecast_time > self._sun_data["next_setting_nautical"]
            or self._forecast_time > self._sun_data["next_setting_civil"]
        ):
            _LOGGER.debug("Astronomical calculations updating sun_next_setting")
            self._calculate_sun()

        if self._sun_data.get("next_setting_astro", None) is not None:
            return self._sun_data["next_setting_astro"]
        if self._sun_data.get("next_setting_nautical", None) is not None:
            return self._sun_data["next_setting_nautical"]
        if self._sun_data.get("next_setting_civil", None) is not None:
            return self._sun_data["next_setting_civil"]

    def _calculate_sun(self):
        """Calculates sun risings and settings."""

        if self._sun_observer is None:
            self._sun_observer = self._get_sun_observer(CIVIL_DUSK_DAWN)
        if self._sun_observer_nautical is None:
            self._sun_observer_nautical = self._get_sun_observer(NAUTICAL_DUSK_DAWN)
        if self._sun_observer_astro is None:
            self._sun_observer_astro = self._get_sun_observer(ASTRONOMICAL_DUSK_DAWN)
        if self._sun is None:
            self._sun = ephem.Sun()

        self._calculate_sun_civil()
        self._calculate_sun_nautical()
        self._calculate_sun_astro()
        self._calculate_sun_altaz()

    def _calculate_sun_civil(self):
        # Rise and Setting (Civil)
        try:
            self._sun_data["next_rising_civil"] = (
                self._sun_observer.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next rising
            start = self._sun_observer.date.datetime()
            end = self._sun_observer.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer.date = timestamp
                try:
                    self._sun_data["next_rising_civil"] = self._sun_observer.next_rising(
                        ephem.Sun(), use_center=True
                    ).datetime()
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_data["next_setting_civil"] = (
                self._sun_observer.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next setting
            start = self._sun_observer.date.datetime()
            end = self._sun_observer.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer.date = timestamp
                try:
                    self._sun_data["next_setting_civil"] = self._sun_observer.next_setting(
                        ephem.Sun(), use_center=True
                    ).datetime()
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

    def _calculate_sun_nautical(self):
        # Rise and Setting (Nautical)
        self._sun_observer_nautical.date = self._forecast_time
        self._sun.compute(self._sun_observer_nautical)

        try:
            self._sun_data["next_rising_nautical"] = (
                self._sun_observer_nautical.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical rising
            start = self._sun_observer_nautical.date.datetime()
            end = self._sun_observer_nautical.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_nautical.date = timestamp
                try:
                    self._sun_data["next_rising_nautical"] = (
                        self._sun_observer_nautical.next_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_data["next_setting_nautical"] = (
                self._sun_observer_nautical.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical setting
            start = self._sun_observer_nautical.date.datetime()
            end = self._sun_observer_nautical.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_nautical.date = timestamp
                try:
                    self._sun_data["next_setting_nautical"] = (
                        self._sun_observer_nautical.next_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

    def _calculate_sun_astro(self):
        # Rise and Setting (Astronomical)
        self._sun_observer_astro.date = self._forecast_time
        self._sun.compute(self._sun_observer_astro)

        try:
            self._sun_data["next_rising_astro"] = (
                self._sun_observer_astro.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical rising
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_data["next_rising_astro"] = (
                        self._sun_observer_astro.next_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_data["previous_rising_astro"] = (
                self._sun_observer_astro.previous_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the previous astronomical rising
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() - timedelta(days=365)
            timestamp = start
            while timestamp > end:
                timestamp -= timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_data["previous_rising_astro"] = (
                        self._sun_observer_astro.previous_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_data["next_setting_astro"] = (
                self._sun_observer_astro.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical setting
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_data["next_setting_astro"] = (
                        self._sun_observer_astro.next_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_data["previous_setting_astro"] = (
                self._sun_observer_astro.previous_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the previous astronomical setting
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() - timedelta(days=365)
            timestamp = start
            while timestamp > end:
                timestamp -= timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_data["previous_setting_astro"] = (
                        self._sun_observer_astro.previous_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=UTC)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

    def _calculate_sun_altaz(self):
        """Calculates sun altitude and azimuth."""

        if self._sun_observer is None:
            self._sun_observer = self._get_sun_observer(CIVIL_DUSK_DAWN)
        if self._sun is None:
            self._sun = ephem.Sun()

        self._sun_observer.date = self._forecast_time
        self._sun.compute(self._sun_observer)

        # Sun Altitude
        self._sun_data["altitude"] = deg(float(self._sun.alt))

        # Sun Azimuth
        self._sun_data["azimuth"] = deg(float(self._sun.az))

    # #########################################################################
    # Moon
    # #########################################################################
    async def moon_data(self) -> dict:
        """Returns moon data."""

        md = MoonDataModel(self._moon_data)
        try:

            return MoonData(data=md)
        except TypeError as ve:
            _LOGGER.error(f"Failed to parse Sun data: {self._moon_data}")
            _LOGGER.error(ve)
            return None

    def _calculate_moon(self):
        """Calculates moon rising and setting."""

        if self._moon_observer is None:
            self._moon_observer = self._get_moon_observer()
        if self._moon is None:
            self._moon = ephem.Moon()

        # Rise and Setting
        self._moon_observer.date = self._forecast_time
        self._moon.compute(self._moon_observer)

        try:
            self._moon_data["next_rising"] = (
                self._moon_observer.next_rising(ephem.Moon()).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_data["next_setting"] = (
                self._moon_observer.next_setting(ephem.Moon()).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_data["previous_rising"] = (
                self._moon_observer.previous_rising(ephem.Moon()).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_data["previous_setting"] = (
                self._moon_observer.previous_setting(ephem.Moon()).datetime().replace(tzinfo=UTC)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        # self._moon_observer.date = self._forecast_time + timedelta(days=1)
        # self._moon.compute(self._moon_observer)

        # try:
        #     self._moon_day_after_next_rising = self._moon_observer.next_rising(ephem.Moon()).datetime().replace(tzinfo=UTC)
        # except (ephem.AlwaysUpError, ephem.NeverUpError):
        #     pass

        # try:
        #     self._moon_day_after_next_setting = self._moon_observer.next_setting(ephem.Moon()).datetime().replace(tzinfo=UTC)
        # except (ephem.AlwaysUpError, ephem.NeverUpError):
        #     pass

        # Next new Moon
        self._moon_data["next_new_moon"] = ephem.next_new_moon(self._forecast_time).datetime().replace(tzinfo=UTC)

        # Next full Moon
        self._moon_data["next_full_moon"] = ephem.next_full_moon(self._forecast_time).datetime().replace(tzinfo=UTC)

        # Moon phase
        self._moon_data["phase"] = self._moon.phase

        self._calculate_moon_altaz()
        self._calculate_moon_distance_size()

    def _calculate_moon_altaz(self):
        """Calculates moon altitude and azimuth."""

        if self._moon_observer is None:
            self._moon_observer = self._get_moon_observer()
        if self._moon is None:
            self._moon = ephem.Moon()

        self._moon_observer.date = self._forecast_time
        self._moon.compute(self._moon_observer)

        # Moon Altitude
        self._moon_data["altitude"] = deg(float(self._moon.alt))

        # Moon Azimuth
        self._moon_data["azimuth"] = deg(float(self._moon.az))

    def _calculate_moon_distance_size(self):
        """Calculate moon distance and relative size"""
        if self._moon_observer is None:
            self._moon_observer = self._get_moon_observer()
        if self._moon is None:
            self._moon = ephem.Moon()

        # Get the distance in Earth radii
        self._moon_data["distance"] = self._moon.earth_distance  # in AU (Astronomical Units)

        # Convert to kilometers
        self._moon_data["distance_km"] = self._moon_data["distance"] * 149597870.7  # 1 AU = 149597870.7 km

        # Get the Moon's angular size (in degrees)
        self._moon_data["angular_size"] = self._moon.radius * 2 * 57.29578  # 180 / pi

        # Average distance and angular size for comparison
        self._moon_data["avg_distance_km"] = 384400  # Average distance of the Moon from Earth in km
        self._moon_data["avg_angular_size"] = 0.5181  # Average angular size in degrees

        # Relative distance and size compared to average
        self._moon_data["relative_distance"] = self._moon_data["distance_km"] / self._moon_data["avg_distance_km"]
        self._moon_data["relative_size"] = self._moon_data["angular_size"] / self._moon_data["avg_angular_size"]

    # #########################################################################
    # Darkness
    # #########################################################################
    async def darkness_data(self) -> DarknessData:
        """Returns darkness data."""

        # if not self._test_data(
        #     self._moon_data, ["next_setting", "next_rising", "previous_setting"]
        # ):
        #     _LOGGER.debug("DSD: moon data missing")
        #     return False

        # if not self._test_data(
        #     self._sun_data,
        #     ["previous_setting_astro", "next_setting_astro", "next_rising_astro"],
        # ):
        #     _LOGGER.debug("DSD: sun data missing")
        #     return False

        self._darkness_data["deep_sky_darkness_moon_rises"] = self._deep_sky_darkness_moon_rises()
        self._darkness_data["deep_sky_darkness_moon_sets"] = self._deep_sky_darkness_moon_sets()
        self._darkness_data["deep_sky_darkness_moon_always_up"] = self._deep_sky_darkness_moon_always_up()
        self._darkness_data["deep_sky_darkness_moon_always_down"] = self._deep_sky_darkness_moon_always_down()
        self._darkness_data["deep_sky_darkness"] = self._deep_sky_darkness()

        dd = DarknessDataModel(self._darkness_data)
        try:

            return DarknessData(data=dd)
        except TypeError as ve:
            _LOGGER.error(f"Failed to parse darkness data: {self._darkness_data}")
            _LOGGER.error(ve)
            return None

    async def night_duration_astronomical(self) -> float:
        """Returns the remaining timespan of astronomical darkness."""

        start_timestamp = None

        # Are we already in darkness?
        if self._astronomical_darkness():
            start_timestamp = self._sun_data["previous_setting_astro"]
        else:
            start_timestamp = self._sun_data["next_setting_astro"]

        return (self._sun_data["next_rising_astro"] - start_timestamp).total_seconds()

    def _deep_sky_darkness(self) -> float:
        """Returns the remaining timespan of deep sky darkness."""

        dsd = timedelta(0)

        if self._astronomical_darkness():
            _LOGGER.debug("DSD: In astronomical darkness")
            if self._deep_sky_darkness_moon_rises():
                dsd = self._moon_data["next_rising"] - self._forecast_time
                _LOGGER.debug(f"DSD: Sun down, Moon rises {dsd}")

            if self._deep_sky_darkness_moon_sets():
                if self._moon_down():
                    dsd = self._sun_data["next_rising_astro"] - self._forecast_time
                    _LOGGER.debug(f"DSD: Sun down, Moon is down {dsd}")
                else:
                    dsd = self._sun_data["next_rising_astro"] - self._moon_data["next_setting"]
                    _LOGGER.debug(f"DSD: Sun down, Moon sets {dsd}")

            if self._deep_sky_darkness_moon_always_down():
                dsd = self._sun_data["next_rising_astro"] - self._forecast_time
                _LOGGER.debug(f"DSD: Moon always down {dsd}")
            else:
                _LOGGER.debug(f"DSD: Moon NOT always down {dsd}")

        if not self._astronomical_darkness():
            _LOGGER.debug("DSD: At sunlight")
            if self._deep_sky_darkness_moon_rises():
                dsd = self._moon_data["next_rising"] - self._sun_data["next_setting_astro"]
                _LOGGER.debug(f"DSD: Sun up, Moon rises {dsd}")

            if self._deep_sky_darkness_moon_sets():
                dsd = self._sun_data["next_rising_astro"] - self._moon_data["next_setting"]
                _LOGGER.debug(f"DSD: Sun up, Moon sets {dsd}")

            if self._deep_sky_darkness_moon_always_down():
                dsd = self._sun_data["next_rising_astro"] - self._sun_data["next_setting_astro"]
                _LOGGER.debug(f"DSD: Sun up, Moon down {dsd}")

        if self._deep_sky_darkness_moon_always_up():
            dsd = timedelta(0)
            _LOGGER.debug(f"DSD: Moon always up {dsd}")
        else:
            _LOGGER.debug(f"DSD: Moon NOT always up {dsd}")

        return dsd.total_seconds()

    def _astronomical_darkness(self) -> bool:
        """Returns true during astronomical night."""

        if self._sun_data["next_setting_astro"] > self._sun_data["next_rising_astro"]:
            return True
        return False

    def _moon_down(self) -> bool:
        """Returns true while moon is set-"""

        if self._moon_data["next_setting"] > self._moon_data["next_rising"]:
            return True
        return False

    def _deep_sky_darkness_moon_rises(self) -> bool:
        """Returns true if moon rises during astronomical night."""

        start_timestamp = None

        # Are we already in darkness?
        if self._astronomical_darkness():
            start_timestamp = self._sun_data["previous_setting_astro"]
        else:
            start_timestamp = self._sun_data["next_setting_astro"]

        if (
            self._moon_data["next_rising"] > start_timestamp
            and self._moon_data["next_rising"] < self._sun_data["next_rising_astro"]
        ):
            _LOGGER.debug("DSD: Moon rises during astronomical night")
            return True
        return False

    def _deep_sky_darkness_moon_sets(self) -> bool:
        """Returns true if moon sets during astronomical night."""

        start_timestamp = None

        # Are we already in darkness?
        if self._astronomical_darkness():
            start_timestamp = self._sun_data["previous_setting_astro"]
        else:
            start_timestamp = self._sun_data["next_setting_astro"]

        # Did Moon already set in darkness?
        if self._moon_down() and self._astronomical_darkness():
            start_timestamp_moon = self._moon_data["previous_setting"]
        else:
            start_timestamp_moon = self._moon_data["next_setting"]

        if start_timestamp_moon > start_timestamp and start_timestamp_moon < self._sun_data["next_rising_astro"]:
            _LOGGER.debug("DSD: Moon sets during astronomical night")
            return True
        return False

    def _deep_sky_darkness_moon_always_up(self) -> bool:
        """Returns true if moon is up during astronomical night."""

        start_timestamp = None

        # Are we already in darkness?
        if self._astronomical_darkness():
            start_timestamp = self._sun_data["previous_setting_astro"]
        else:
            start_timestamp = self._sun_data["next_setting_astro"]

        if (
            self._moon_data["next_rising"] < start_timestamp
            and self._moon_data["next_setting"] > self._sun_data["next_rising_astro"]
        ):
            _LOGGER.debug("DSD: Moon is up during astronomical night")
            return True
        return False

    def _deep_sky_darkness_moon_always_down(self) -> bool:
        """Returns true if moon is down during astronomical night."""

        start_timestamp = None

        # Are we already in darkness?
        if self._astronomical_darkness():
            start_timestamp = self._sun_data["previous_setting_astro"]
        else:
            start_timestamp = self._sun_data["next_setting_astro"]

        if (
            self._moon_data["previous_setting"] < start_timestamp
            and self._moon_data["next_rising"] > self._sun_data["next_rising_astro"]
        ):
            _LOGGER.debug("DSD: Moon is down during astronomical night")
            return True
        return False
