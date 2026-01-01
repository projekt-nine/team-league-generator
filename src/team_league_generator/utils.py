import os
from glob import glob
from .constants import HERE, DATA, GEO
from .errors import CountryCodeError


def get_city_country_codes():
    """Return a sorted list of country codes"""
    country_codes = set()
    for fpath in sorted(glob(GEO + "/*.txt")):
        fname = os.path.basename(fpath)
        if "states" in fname:
            continue
        country_code = fname.split(".")[0]
        country_codes.add(country_code)
    return sorted(list(country_codes))


def get_state_country_codes():
    country_codes = set()
    for fpath in sorted(glob(GEO + "/*_states.txt")):
        fname = os.path.basename(fpath)
        country_code = fname.split("_")[0]
        country_codes.add(country_code)
    return sorted(list(country_codes))


def country_code_to_english(cc):
    fname = get_abbr_key_file()
    with open(fname, 'r') as f:
        lines = f.readlines()
    lines = [s.strip() for s in lines]
    for line in lines:
        split = line.split(" ")
        if split[0].lower() == cc.lower():
            return " ".join(split[1:])

    raise CountryCodeError(f"Error: country code {cc} not found in abbreviations key file!")


def get_cities_data_file_from_country_code(country_code):
    fname = country_code + ".txt"
    return os.path.join(GEO, fname)


def get_states_data_file_from_country_code(country_code):
    fname = country_code + "_states.txt"
    return os.path.join(GEO, fname)


def get_abbr_key_file():
    fname = "_ABBR_KEY"
    return os.path.join(GEO, fname)


def get_team_names_data_file():
    fname = "team_names.txt"
    return os.path.join(DATA, fname)


def get_leagues_divisions_data_file():
    fname = "leagues_divisions.txt"
    return os.path.join(DATA, fname)

def get_first_names_data_file():
    fname = "first_names.txt"
    return os.path.join(DATA, fname)

def get_last_names_data_file():
    fname = "last_names.txt"
    return os.path.join(DATA, fname)

def get_cities_count(country_code):
    city_fname = f"{country_code}.txt"
    city_fpath = os.path.join(GEO, city_fname)
    if not os.path.exists(city_fpath):
        raise CountryCodeError(
            f"Error: could not run get_city_count(): invalid country code {country_code} for cities"
        )
    with open(city_fpath, "r") as f:
        data = f.readlines()
    data = [j.strip() for j in data if len(j.strip()) > 0]
    return len(data)


def get_states_count(country_code):
    st_fname = f"{country_code}_states.txt"
    st_fpath = os.path.join(GEO, st_fname)
    if not os.path.exists(st_fpath):
        raise CountrryCodeError(
            f"Error: could not run get_state_count(): invalid country code {country_code} for states"
        )
    with open(st_fpath, "r") as f:
        data = f.readlines()
    data = [j.strip() for j in data if len(j.strip()) > 0]
    return len(data)
