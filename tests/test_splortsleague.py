import random
import unittest
from team_league_generator.splortsleague import SplortsLeagueGenerator


class TestSplortsLeague(unittest.TestCase):
    def test_splorts_league_generator(self):
        random.seed(420)
        slg = SplortsLeagueGenerator()

        random.seed(420)
        res = slg.generate()

        league_names = ["Aleatoric", "Epistemic"]
        division_names = ["Peanut", "Raspberry"]
        for league_name in league_names:
            self.assertIn(league_name, res.keys())
            for division_name in division_names:
                self.assertIn(division_name, res[league_name])

        self.assertIn("Jersey City Neutron Equations", res[league_names[0]][division_names[0]])

    def test_extract_leagues_divisions_teams_sim(self):
        league = {
            "Hot": {
                "Island": ["Aye Ones", "Bye Twos", "Cee Threes", "Dee Fours"],
                "Volcano": ["Eee Fives", "Fff Sixes", "Grr Sevens", "Hey Eights"],
            },
            "Cold": {
                "Island": ["I Nines", "Jay Tens", "Kay Elevens", "El Twelves"],
                "Volcano": [
                    "Em Thirteens",
                    "En Fourteens",
                    "Oh Fifteens",
                    "Pee Sixteens",
                ],
            },
        }
        (
            league_names,
            division_names,
            team_names,
        ) = SplortsLeagueGenerator.extract_leagues_divisions_teams(league)
        self.assertIn("Hot", league_names)
        self.assertIn("Cold", league_names)
        self.assertIn("Island", division_names)
        self.assertIn("Volcano", division_names)
        self.assertIn("Aye Ones", team_names)
        self.assertIn("Eee Fives", team_names)
        self.assertIn("El Twelves", team_names)

    def test_extract_leagues_divisions_teams_real(self):
        random.seed(420)
        slg = SplortsLeagueGenerator()

        random.seed(420)
        res = slg.generate()

        (
            league_names,
            division_names,
            team_names,
        ) = SplortsLeagueGenerator.extract_leagues_divisions_teams(res)
        self.assertIn("Aleatoric", league_names)
        self.assertIn("Epistemic", league_names)
        self.assertIn("Peanut", division_names)
        self.assertIn("Raspberry", division_names)
        self.assertIn("Albany Flying Scots", team_names)

    def test_league_geo_type(self):
        # -----
        # Default (cities)
        random.seed(420)
        slg = SplortsLeagueGenerator(country_code="rus")

        random.seed(420)
        res = slg.generate()
        (
            league_names,
            division_names,
            team_names,
        ) = SplortsLeagueGenerator.extract_leagues_divisions_teams(res)
        self.assertIn('Aleatoric', league_names)
        self.assertIn('Epistemic', league_names)
        self.assertIn('Peanut', division_names)
        self.assertIn('Raspberry', division_names)
        self.assertIn('Avtury Flying Scots', team_names)
        self.assertIn('Podolsk Pharynges', team_names)
        self.assertIn('Saratov Dogcatchers', team_names)

        # -----
        # States
        random.seed(420)
        slg = SplortsLeagueGenerator(country_code="rus", geo="states")

        random.seed(420)
        res2 = slg.generate(nleagues=4, ndivisions=4, teams_per_division=3)
        (
            league_names2,
            division_names2,
            team_names2,
        ) = SplortsLeagueGenerator.extract_leagues_divisions_teams(res2)
        self.assertIn('Alpha', league_names2)
        self.assertIn('Bravo', league_names2)
        self.assertIn('Apricot', division_names2)
        self.assertIn('Lime', division_names2)
        self.assertIn('Altai Krai Spartans', team_names2)
        self.assertIn('Khabarovsk Necessities', team_names2)
        self.assertIn('Tomsk Purple Quokkas', team_names2)

        # -----
        # Failure
        with self.assertRaises(Exception):
            SplortsLeagueGenerator(country_code="blah-blah-blah")

        with self.assertRaises(Exception):
            SplortsLeagueGenerator(geo="blah-blah-blah")

        gen = SplortsLeagueGenerator()
        with self.assertRaises(Exception):
            gen.generate(nleagues=1000)
            gen.generate(ndivisions=1000)
            gen.generate(nleagues=1000, ndivisions=1000)

