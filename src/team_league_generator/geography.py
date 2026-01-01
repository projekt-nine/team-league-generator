from collections.abc import Iterable
import random
import os
from .utils import (
    get_city_country_codes,
    get_state_country_codes,
    get_cities_data_file_from_country_code,
    get_states_data_file_from_country_code,
    country_code_to_english,
    get_cities_count,
    get_states_count,
)
from .generics import (
    IterableDataLoader,
    UniformGenerator,
    LinearBiasedGenerator,
    ReversedLinearBiasedGenerator,
)
from .errors import (
    InvalidSizeRequestError,
    GeographyError,
    CountryCodeError,
)


class CitiesGeneratorBase(IterableDataLoader):
    """
    Base class that loads cities for a given country code
    """

    def __init__(self, **kwargs):
        if "country_code" not in kwargs:
            raise KeywordError("Error: country_code is a required keyword argument")
        else:
            country_code = kwargs["country_code"]
        if country_code not in get_city_country_codes():
            raise CountryCodeError(
                "Error: invalid country code {country_code} passed to {cls.__name__}"
            )
        self.country_code = country_code
        cities_file = get_cities_data_file_from_country_code(country_code)
        with open(cities_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        super().__init__(data)


class CitiesGenerator(CitiesGeneratorBase, UniformGenerator):
    """
    Generate random cities uniformly
    """

    def generate(self, *args, **kwargs):
        try:
            return super().generate(*args, **kwargs)
        except InvalidSizeRequestError:
            country_name = country_code_to_english(self.country_code)
            err = f"{self.__class__.__name__}: Error: {kwargs['size']} cities requested, only {len(self.data)} exist "
            err += f"for country {country_name} ({country_code})"
            raise GeographyError(err)


class BigCitiesGenerator(CitiesGeneratorBase, LinearBiasedGenerator):
    """
    Generate random cities with a log bias for big cities
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # reduce list to first 1/3 in list
        index = len(self.data) // 3
        self.data = self.data[:index]


class SmallTownsGenerator(CitiesGeneratorBase, ReversedLinearBiasedGenerator):
    """
    Generate random cities with a linear bias for small towns
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # reduce list to last 2/3 in list
        index = len(self.data) // 3
        self.data = self.data[index:]


class StatesGeneratorBase(IterableDataLoader):
    """
    Base class that loads states for a given country code
    """

    def __init__(self, **kwargs):
        if "country_code" not in kwargs:
            raise KeywordError("Error: country_code is a required keyword argument")
        else:
            country_code = kwargs["country_code"]
        if country_code not in get_state_country_codes():
            raise CountryCodeError(
                "Error: invalid country code {country_code} passed to {cls.__name__}"
            )
        self.country_code = country_code
        states_file = get_states_data_file_from_country_code(country_code)
        with open(states_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        super().__init__(data)


class StatesGenerator(StatesGeneratorBase, UniformGenerator):
    """
    Generate random states uniformly
    """

    def generate(self, *args, **kwargs):
        try:
            return super().generate(*args, **kwargs)
        except InvalidSizeRequestError:
            country_name = country_code_to_english(self.country_code)
            err = f"{self.__class__.__name__}: Error: {kwargs['size']} states requested, only {len(self.data)} exist "
            err += f"for country {country_name} ({country_code})"
            raise GeographyError(err)


class BigStatesGenerator(StatesGeneratorBase, LinearBiasedGenerator):
    """
    Generate random states with a linear bias for big states
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # reduce list to first 1/2 in list
        index = len(self.data) // 2
        self.data = self.data[:index]


class SmallStatesGenerator(StatesGeneratorBase, ReversedLinearBiasedGenerator):
    """
    Generate random states with a linear bias for small states
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # reduce list to last 1/2 in list
        index = len(self.data) // 2
        self.data = self.data[index:]
