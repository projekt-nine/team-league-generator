import random
import unittest
from team_league_generator.utils import get_city_country_codes, get_state_country_codes
from team_league_generator.errors import CountryCodeError
from team_league_generator.geography import (
    StatesGeneratorBase,
    StatesGenerator,
    BigStatesGenerator,
    SmallStatesGenerator,
    CitiesGeneratorBase,
    CitiesGenerator,
    BigCitiesGenerator,
    SmallTownsGenerator,
)


class TestGeography(unittest.TestCase):
    def test_states_generator_base(self):
        sg = StatesGeneratorBase(country_code="usa")
        # Calling generate_nonunique() should fail
        with self.assertRaises(AttributeError):
            sg.generate_nonunique(size=50)

    def test_states_generator(self):
        sg = StatesGenerator(country_code="usa")

        random.seed(420)
        res = sg.generate(size=10)
        self.assertIn("Texas", res)

        random.seed(420)
        res2 = sg.generate_nonunique(size=10)
        self.assertIn("Texas", res2)

    def test_states_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = StatesGenerator(country_code="blah-blah-blah")

    def test_small_states_generator(self):
        ssg = SmallStatesGenerator(country_code="usa")

        random.seed(420)
        res = ssg.generate(size=10)
        self.assertIn("Wyoming", res)

        random.seed(420)
        res2 = ssg.generate_nonunique(size=10)
        self.assertIn("Wyoming", res2)

    def test_small_states_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = SmallStatesGenerator(country_code="blah-blah-blah")

    def test_big_states_generator(self):
        bsg = BigStatesGenerator(country_code="usa")

        random.seed(420)
        res = bsg.generate(size=10)
        self.assertIn("California", res)

        random.seed(420)
        res2 = bsg.generate_nonunique(size=10)
        self.assertIn("California", res2)

    def test_big_states_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = BigStatesGenerator(country_code="blah-blah-blah")

    def test_cities_generator(self):
        cg = CitiesGenerator(country_code="usa")

        random.seed(420)
        res = cg.generate(size=10)
        self.assertIn("Scranton", res)

        random.seed(420)
        res2 = cg.generate_nonunique(size=10)
        self.assertIn("Danbury", res2)

    def test_cities_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = CitiesGenerator(country_code="blah-blah-blah")

    def test_small_towns_generator(self):
        cg = SmallTownsGenerator(country_code="usa")

        random.seed(420)
        res = cg.generate(size=10)
        self.assertIn("Cold Spring Harbor", res)

        random.seed(420)
        res2 = cg.generate_nonunique(size=10)
        self.assertIn("Cold Spring Harbor", res2)

    def test_small_towns_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = SmallTownsGenerator(country_code="blah-blah-blah")

    def test_big_cities_generator(self):
        cg = BigCitiesGenerator(country_code="usa")

        random.seed(420)
        res = cg.generate_nonunique(size=10)
        self.assertIn("Anchorage", res)

        random.seed(420)
        res2 = cg.generate(size=10)
        self.assertIn("Anchorage", res2)

    def test_big_cities_generator_errors(self):
        with self.assertRaises(CountryCodeError):
            sg = BigCitiesGenerator(country_code="blah-blah-blah")

    def test_city_country_codes(self):
        country_codes = get_city_country_codes()
        for country_code in country_codes:
            CitiesGenerator(country_code=country_code)
            BigCitiesGenerator(country_code=country_code)
            SmallTownsGenerator(country_code=country_code)

        invalid_country_codes = ["nope", "narnia", "blahblahblah", "notlistening"]
        for country_code in invalid_country_codes:
            with self.assertRaises(CountryCodeError):
                CitiesGenerator(country_code=country_code)
                BigCitiesGenerator(country_code=country_code)
                SmallTownsGenerator(country_code=country_code)

    def test_state_country_codes(self):
        country_codes = get_state_country_codes()
        for country_code in country_codes:
            StatesGenerator(country_code=country_code)
            BigStatesGenerator(country_code=country_code)
            SmallStatesGenerator(country_code=country_code)

        invalid_country_codes = ["nope", "narnia", "blahblahblah", "notlistening"]
        for country_code in invalid_country_codes:
            with self.assertRaises(CountryCodeError):
                StatesGenerator(country_code=country_code)
                BigStatesGenerator(country_code=country_code)
                SmallStatesGenerator(country_code=country_code)
