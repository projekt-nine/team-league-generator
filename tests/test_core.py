import unittest
from team_league_generator.utils import (
    get_city_country_codes,
    get_state_country_codes
)


class TestCore(unittest.TestCase):
    def test_country_codes(self):
        get_city_country_codes()
        get_state_country_codes()
