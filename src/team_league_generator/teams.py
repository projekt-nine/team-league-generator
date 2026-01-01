import random
import os
from .generics import IterableDataLoader, UniformGenerator
from .utils import get_team_names_data_file, get_leagues_divisions_data_file


HERE = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(HERE, "data")


class TeamNameGeneratorBase(IterableDataLoader):
    def __init__(self, team_names_file=None, **kwargs):
        if team_names_file is None:
            team_names_file = get_team_names_data_file()
        if not os.path.exists(team_names_file):
            raise FileNotFoundError(
                f"{self.__class__.__name__}: Error: specified teams file does not exist: {team_names_file}"
            )
        with open(team_names_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        super().__init__(data)


class TeamNameGenerator(TeamNameGeneratorBase, UniformGenerator):
    pass


class LeagueDivisionNameGeneratorBase(IterableDataLoader):
    def __init__(self, leagues_divisions_file=None, **kwargs):
        if leagues_divisions_file is None:
            leagues_divisions_file = get_leagues_divisions_data_file()
        if not os.path.exists(leagues_divisions_file):
            raise FileNotFoundError(
                f"{self.__class__.__name__}: Error: specified leagues/divisions file does not exist: {leagues_divisions_file}"
            )
        with open(leagues_divisions_file, "r") as f:
            data = f.readlines()
        data = [j.strip() for j in data if len(j.strip()) > 0]
        data = [[k.strip().title() for k in j.split(",")] for j in data]
        self.max_len = max([len(j) for j in data])
        super().__init__(data)

    def generate(self, size=1, reverse=False):
        if size > self.max_len:
            raise InvalidSizeRequestError(f"{self.__class__.__name__}: Error: specified size exceeded maximum length {max_len}")
        elif size < 1:
            raise InvalidSizeRequestError(f"{self.__class__.__name__}: Error: size parameter {size} was too small")

        valid_data = [j for j in self.data if len(j) >= size]
        choice = random.choice(valid_data)[:]
        return choice[:size]


class LeagueNameGenerator(LeagueDivisionNameGeneratorBase, UniformGenerator):
    pass


class DivisionNameGenerator(LeagueDivisionNameGeneratorBase, UniformGenerator):
    pass
