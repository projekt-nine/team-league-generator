import os
import random
import unittest
from team_league_generator.constants import DATA, GEO
from team_league_generator.utils import (
    get_city_country_codes,
    get_state_country_codes,
    get_cities_data_file_from_country_code,
    get_states_data_file_from_country_code,
    country_code_to_english,
    get_abbr_key_file,
    get_team_names_data_file,
    get_leagues_divisions_data_file,
    get_cities_count,
    get_states_count,
)

class TestUtils(unittest.TestCase):
    cc = ['usa', 'rus', 'fra', 'ger', 'can', 'mex', 'chi', 'chi', 'jpn', 'phi', 'ind', 'idn']

    def test_get_city_country_codes(self):
        all_ccc = get_city_country_codes()
        ccc = self.cc
        for cc in ccc:
            self.assertIn(cc, all_ccc)

    def test_get_state_country_codes(self):
        all_scc = get_state_country_codes()
        scc = self.cc
        for cc in scc:
            self.assertIn(cc, all_scc)

    def test_get_states_data_file_from_country_code(self):
        for cc in self.cc:
            our_path = os.path.join(GEO, f'{cc}_states.txt')
            their_path = get_states_data_file_from_country_code(cc)
            self.assertEqual(our_path, their_path)

    def test_get_cities_data_file_from_country_code(self):
        for cc in self.cc:
            our_path = os.path.join(GEO, f'{cc}.txt')
            their_path = get_cities_data_file_from_country_code(cc)
            self.assertEqual(our_path, their_path)

    def test_country_code_to_english(self):
        gold = {
            'rus': 'Russia',
            'usa': 'United States',
            'Chi': 'Chile',
            'CAN': 'Canada'
        }
        for country_code, country_name in gold.items():
            self.assertEqual(country_code_to_english(country_code), country_name)

    def test_get_abbr_key_file(self):
        our_path = os.path.join(GEO, '_ABBR_KEY')
        their_path = get_abbr_key_file()
        self.assertEqual(our_path, their_path)

    def test_get_team_names_data_file(self):
        our_path = os.path.join(DATA, f'team_names.txt')
        their_path = get_team_names_data_file()
        self.assertEqual(our_path, their_path)

    def test_get_leagues_divisions_data_file(self):
        our_path = os.path.join(DATA, f'leagues_divisions.txt')
        their_path = get_leagues_divisions_data_file()
        self.assertEqual(our_path, their_path)

    def test_cities_count(self):
        counts = {
            'usa': 14895,
            'rus': 4589,
            'fra': 9022,
            'ger': 7525,
            'can': 1181,
        }
        for cc in counts:
            count = get_cities_count(cc)
            self.assertEqual(counts[cc], count)

    def test_states_count(self):
        counts = {
            'usa': 51,
            'rus': 83,
            'fra': 22,
            'ger': 16,
            'can': 13,
        }
        for cc in counts:
            count = get_states_count(cc)
            self.assertEqual(counts[cc], count)
