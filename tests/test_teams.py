import os
import random
import tempfile
import unittest
from team_league_generator.teams import (
    TeamNameGeneratorBase,
    TeamNameGenerator,
    LeagueDivisionNameGeneratorBase,
    LeagueNameGenerator,
    DivisionNameGenerator,
)


class TestTeams(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.tmp = cls.tmpdir.name
        if not os.path.exists(cls.tmp):
            os.mkdir(cls.tmp)

    def test_team_name_generator_base(self):
        tg = TeamNameGeneratorBase()
        with self.assertRaises(Exception):
            tg.generate()

    def test_team_name_generator(self):
        tg = TeamNameGenerator()
        random.seed(420)
        res = tg.generate(size=4)
        self.assertIn("Ritualists", res)

    def test_team_name_generator_data_file(self):
        teams = [
            "Ones",
            "Twos",
            "Threes",
            "Fours",
            "Fives",
            "Sixes",
            "Sevens",
            "Eights",
        ]

        # Write teams to temp data file
        tmpteams = os.path.join(self.tmp, "teams.txt")
        if not os.path.exists(self.tmp):
            raise Exception("Well this is stupid")
        with open(tmpteams, "w") as f:
            f.write("\n".join(teams))

        tg = TeamNameGenerator(team_names_file=tmpteams)
        
        random.seed(420)
        
        res = tg.generate(size=4)
        self.assertIn('Ones', res)
        self.assertIn('Fives', res)
        self.assertIn('Sixes', res)

    @classmethod
    def tearDownClass(cls):
        del cls.tmpdir


class LeagueDivisionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.tmp = cls.tmpdir.name

    def test_league_division_name_generator_base(self):
        LeagueDivisionNameGeneratorBase()

    def test_league_name_generator(self):
        lg = LeagueNameGenerator()

        random.seed(420)

        res = lg.generate(size=4)
        self.assertIn("Alpha", res)
        self.assertIn("Bravo", res)

        res2 = lg.generate(size=16)
        self.assertIn("Beryl", res2)
        self.assertIn("Amber", res2)

    def test_division_name_generator(self):
        dg = DivisionNameGenerator()

        random.seed(420)

        res = dg.generate(size=4)
        self.assertIn("Alpha", res)
        self.assertIn("Bravo", res)

        res2 = dg.generate(size=16)
        self.assertIn("Beryl", res2)
        self.assertIn("Amber", res2)

    def test_league_division_generator_data_file(self):
        leagues_divisions = [
            "Zabba,Babba,Cabba,Dabba",
            "Fabba,Gabba,Habba,Jabba",
            "Kabba,Labba,Mabba,Nabba",
            "Pabba,Qabba,Rabba,Sabba",
        ]
        tempfile = os.path.join(self.tmp, 'leagues_divisions.txt')
        with open(tempfile, 'w') as f:
            f.write('\n'.join(leagues_divisions))

        lg = LeagueNameGenerator(leagues_divisions_file=tempfile)

        random.seed(420)
        res = lg.generate(size=2)
        self.assertIn('Zabba', res)
        self.assertIn('Babba', res)

        res = lg.generate(size=2)
        self.assertIn('Kabba', res)
        self.assertIn('Labba', res)

    @classmethod
    def tearDownClass(cls):
        del cls.tmpdir
