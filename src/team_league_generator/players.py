import random
import os
from .generics import IterableDataLoader, UniformGenerator
from .utils import (
    get_team_names_data_file, 
    get_leagues_divisions_data_file,
    get_first_names_data_file,
    get_last_names_data_file,
)


HERE = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(HERE, "data")


class FirstNameGeneratorBase(IterableDataLoader):
    def __init__(self, first_names_file=None, **kwargs):
        if first_names_file is None:
            first_names_file = get_first_names_data_file()
        if not os.path.exists(first_names_file):
            raise FileNotFoundError(
                f"Error: FirstNameGenerator passed a file that does not exist: {first_names_file}"
            )
        with open(first_names_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        super().__init__(data)


class FirstNameGenerator(FirstNameGeneratorBase, UniformGenerator):
    pass


class LastNameGeneratorBase(IterableDataLoader):
    def __init__(self, last_names_file=None, **kwargs):
        if last_names_file is None:
            last_names_file = get_last_names_data_file()
        if not os.path.exists(last_names_file):
            raise FileNotFoundError(
                f"Error: LastNameGenerator passed a file that does not exist: {last_names_file}"
            )
        with open(last_names_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        super().__init__(data)


class LastNameGenerator(LastNameGeneratorBase, UniformGenerator):
    pass


class NameGenerator(object):
    def __init__(self, **kwargs):
        self.fng = FirstNameGenerator(**kwargs)
        self.lng = LastNameGenerator(**kwargs)

    def generate(self, size=1, alliteration_rate=0.1):
        if size < 1:
            raise InvalidSizeRequestError(f"Error: Invalid size passed to NameGenerator: {size}")
        names = []
        for i in range(size):
            alliterate = random.random() < alliteration_rate
            first = self.fng.generate()[0]
            last = self.lng.generate()[0]
            if alliterate:
                while last[0] != first[0]:
                    last = self.lng.generate()[0]
            name = first + " " + last
            names.append(name)
        return names
