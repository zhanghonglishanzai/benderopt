import numpy as np


def validate_normal(search_space):
    # error = "Expected a type dict with mandatory keys : [mu, sigma] and optional key log  or step"
    if type(search_space) != dict:
        raise ValueError("Search space must be a dict.")

    search_space = search_space.copy()

    if "mu" not in search_space.keys() or type(search_space["mu"]) not in (int, float):
        print(search_space)
        raise ValueError

    if "sigma" not in search_space.keys() or type(search_space["sigma"]) not in (int, float):
        raise ValueError

    if "step" in search_space.keys():
        if search_space["step"] and type(search_space["step"]) not in (int, float):
            raise ValueError

    if "low" in search_space.keys():
        if type(search_space["low"]) not in (int, float):
            raise ValueError

    if "high" in search_space.keys():
        if type(search_space["high"]) not in (int, float):
            raise ValueError

    if "high" in search_space.keys() and "low" in search_space.keys():
        if search_space["high"] <= search_space["low"]:
            raise ValueError("low <= high")

    search_space.setdefault("low", -np.inf)
    search_space.setdefault("high", -np.inf)

    search_space.setdefault("step", None)

    return search_space


def validate_normal_value(value, low, high, **kwargs):
    test = True
    if value < low:
        test = False
    elif value > high:
        test = False
    return test