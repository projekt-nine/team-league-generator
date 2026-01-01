import os
import random
import tempfile
import unittest
from team_league_generator.players import (
    FirstNameGeneratorBase,
    FirstNameGenerator,
    LastNameGeneratorBase,
    LastNameGenerator,
    NameGenerator,
)


class TestPlayers(unittest.TestCase):
    fake_names = [
        "Asdf",
        "Qwerty",
        "Zxcvb",
        "Yuiop",
        "Ghjkl",
        "Bnm",
        "Rtyu"
    ]

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.tmp = cls.tmpdir.name
        if not os.path.exists(cls.tmp):
            os.mkdir(cls.tmp)

    def test_first_name_generator_base(self):
        fng = FirstNameGeneratorBase()
        with self.assertRaises(Exception):
            fng.generate()

    def test_last_name_generator_base(self):
        fng = LastNameGeneratorBase()
        with self.assertRaises(Exception):
            fng.generate()

    def test_first_name_generator(self):
        fng = FirstNameGenerator()
        random.seed(420)
        res = fng.generate(size=4)
        self.assertIn("Parker", res)

    def test_last_name_generator(self):
        fng = LastNameGenerator()
        random.seed(420)
        res = fng.generate(size=4)
        self.assertIn("Bates", res)

    def test_name_generator(self):
        ng = NameGenerator()
        random.seed(420)
        res = ng.generate(size=4)
        self.assertIn("Parker Pangreaser", res)

    def test_first_name_generator_data_file(self):
        fnames = self.fake_names
        fnfile = os.path.join(self.tmp, 'first_names.txt')
        with open(fnfile, 'w') as f:
            f.write("\n".join(fnames))

        fng = FirstNameGenerator(first_names_file=fnfile)
        random.seed(420)
        res = fng.generate(size=4)
        self.assertIn("Asdf", res)

    def test_last_name_generator_data_file(self):
        lnames = self.fake_names
        lnfile = os.path.join(self.tmp, 'last_names.txt')
        with open(lnfile, 'w') as f:
            f.write("\n".join(lnames))

        lng = LastNameGenerator(last_names_file=lnfile)
        random.seed(420)
        res = lng.generate(size=4)
        self.assertIn("Bnm", res)

    def test_name_generator(self):
        fnames = self.fake_names
        fnfile = os.path.join(self.tmp, 'first_names.txt')
        with open(fnfile, 'w') as f:
            f.write("\n".join(fnames))

        lnames = self.fake_names
        lnfile = os.path.join(self.tmp, 'last_names.txt')
        with open(lnfile, 'w') as f:
            f.write("\n".join(lnames))

        ng = NameGenerator(first_names_file=fnfile, last_names_file=lnfile)
        random.seed(420)
        res = ng.generate(size=4)
        self.assertIn('Zxcvb Asdf', res)
        self.assertIn('Rtyu Rtyu', res)

    @classmethod
    def tearDownClass(cls):
        del cls.tmpdir
