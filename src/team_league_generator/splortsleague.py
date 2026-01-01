import random
from .teams import (
    TeamNameGenerator,
    LeagueNameGenerator,
    DivisionNameGenerator,
)
from .geography import (
    CitiesGenerator,
    BigCitiesGenerator,
    SmallTownsGenerator,
    StatesGenerator,
    BigStatesGenerator,
    SmallStatesGenerator,
)


MAX_LEAGUES_DIVISIONS = 24


class SplortsLeagueGenerator(object):
    """
    Use various generators to assemble a league of splorts teams.
    """

    def __init__(self, geo="bigcities", country_code="usa", **kwargs):
        kwargs['country_code'] = country_code
        self.geo_type_map = {
            "cities": CitiesGenerator,
            "bigcities": BigCitiesGenerator,
            "smalltowns": SmallTownsGenerator,
            "states": StatesGenerator,
            "bigstates": BigStatesGenerator,
            "smallstates": SmallStatesGenerator,
        }
        if geo not in self.geo_type_map.keys():
            valid_keys = ", ".join(self.geo_type_map.keys())
            raise Exception(
                f"Error: Invalid geo parameter {geo} passed, should be in {valid_keys}"
            )
        GeoGen = self.geo_type_map[geo]

        self.geo = GeoGen(**kwargs)
        self.team = TeamNameGenerator(**kwargs)
        self.lea = LeagueNameGenerator(**kwargs)
        self.div = DivisionNameGenerator(**kwargs)

    def generate(
        self, nleagues=2, ndivisions=2, teams_per_division=4, geo=None, **kwargs
    ):
        if (nleagues < 0 or ndivisions < 0) or (
            nleagues > MAX_LEAGUES_DIVISIONS or ndivisions > MAX_LEAGUES_DIVISIONS
        ):
            raise KeywordError(
                f"Error: number of leagues {nleagues} or divisions {ndivisions} was invalid"
            )

        league_names = self.lea.generate(size=nleagues)
        # League and division names should have no overlap
        ntries = 0
        division_names = self.div.generate(size=nleagues)
        while len(set(division_names).intersection(set(league_names))) > 0:
            division_names = self.div.generate(size=nleagues)

        # Generate all teams at once
        all_locs = sorted(self.geo.generate(size=nleagues*ndivisions*teams_per_division))
        random.shuffle(all_locs)

        all_teams = sorted(self.team.generate(size=nleagues*ndivisions*teams_per_division))
        random.shuffle(all_teams)

        final = {}
        for iL, league_name in enumerate(sorted(league_names)):
            league = {}
            for iD, division_name in enumerate(sorted(division_names)):
                division = []
                div_locs, all_locs = all_locs[:teams_per_division], all_locs[teams_per_division:]
                div_teams, all_teams = all_teams[:teams_per_division], all_teams[teams_per_division:]
                for location_name, team_name in zip(div_locs, div_teams):
                    division.append(" ".join([location_name, team_name]))
                league[division_name] = division
            final[league_name] = league

        return final

    @staticmethod
    def extract_leagues_divisions_teams(league_dict):
        leagues = set(league_dict.keys())
        divs = set()
        teams = set()
        for league_name, div_dict in league_dict.items():
            [divs.add(j) for j in div_dict.keys()]
            for div_name, team_list in div_dict.items():
                [teams.add(j) for j in team_list]
        return sorted(list(leagues)), sorted(list(divs)), sorted(list(teams))
