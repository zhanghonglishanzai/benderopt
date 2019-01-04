import numpy as np
from benderopt.minimizer import minimize


optimization_problem = [
    {
        "name": "x1",
        "category": "uniform",
        "search_space": {
            "low": 0,
            "high": 10,
        }
    },
    {
        "name": "x1_step",
        "category": "uniform",
        "search_space": {
            "low": 0,
            "high": 10,
            "step": 1
        }
    },
    {
        "name": "x2",
        "category": "loguniform",
        "search_space": {
            "low": 1e4,
            "high": 1e6,
            "base": 10,
        }
    },
    {
        "name": "x2_step",
        "category": "loguniform",
        "search_space": {
            "low": 1e4,
            "high": 1e6,
            "step": 1e3,
            "base": 10,
        }
    },
    {
        "name": "x3",
        "category": "normal",
        "search_space": {
            "mu": 8,
            "sigma": 4,
            "low": 0,
            "high": 10,
        }
    },
    {
        "name": "x3_step",
        "category": "normal",
        "search_space": {
            "mu": 8,
            "sigma": 4,
            "low": 0,
            "high": 10,
            "step": 0.2,
        }
    },
    {
        "name": "x4",
        "category": "lognormal",
        "search_space": {
            "mu": 1e-5,
            "sigma": 1e1,
            "low": 1e-7,
            "high": 1e-3,
            "base": 10,
        }
    },
    {
        "name": "x4_step",
        "category": "lognormal",
        "search_space": {
            "mu": 1e-5,
            "sigma": 1e1,
            "low": 1e-8,
            "high": 1e-3,
            "step": 1e-8,
            "base": 10,
        }
    },
    {
        "name": "x5",
        "category": "categorical",
        "search_space": {
            "values": ["a", "b", "c", "d"],
        }
    },
]


def function_to_optimize(x1,
                         x1_step,
                         x2,
                         x2_step,
                         x3,
                         x3_step,
                         x4,
                         x4_step,
                         x5):
    loss = 0
    loss += ((x1 - 5.5) / 5.5) ** 2
    loss += ((x1_step - 5) / 5) ** 2
    loss += ((x2 - 3.75e4) / 3.75e4) ** 2
    loss += ((x2_step - 9.2e4) / 9.2e4) ** 2
    loss += ((x3 - 8.1447) / 8.1447) ** 2
    loss += ((x3_step - 8) / 8) ** 2
    loss += ((x4 - 1.33e-5) / 1.33e-5) ** 2
    loss += ((x4_step - 1.456e-5) / 1.456e-5) ** 2
    loss += (["a", "b", "c", "d"].index(x5) / (3 + 2 + 1 + 0))
    return loss


best_sample = {
    "x1": 5.5,
    "x1_step": 5,
    "x2": 3.75e4,
    "x2_step": 9.2e4,
    "x3": 8.1447,
    "x3_step": 8,
    "x4": 1.33e-5,
    "x4_step": 1.456e-5,
    "x5": "a"
}


np.random.seed(0)
seeds = np.random.randint(low=0, high=2 ** 31 - 1, size=5)
methods = ["parzen_estimator", "random"]
number_of_trials = [30, 50, 100, 200, 500]
trials = {
    method: {
        n: []
        for n in number_of_trials
    }
    for method in methods
}
for seed in seeds:
    for n in number_of_trials:
        for method in methods:
            print("N: {}".format(n))
            np.random.seed(seed)
            best = minimize(function_to_optimize,
                            optimization_problem,
                            optimizer_type=method,
                            number_of_evaluation=n)
            trials[method][n].append(function_to_optimize(**best))
        # print(trials)
results = {
    method: {
        n: {
            "mean": np.mean(values),
            "std": np.std(values),
        }
        for n, values in ns.items()
    }
    for method, ns in trials.items()
}

for n in number_of_trials:
    print("\nN:{}\n".format(n))
    print("Random: {}/{}".format(results["random"][n]["mean"], results["random"][n]["std"]))
    print("parzen: {}/{}".format(results["parzen_estimator"][n]["mean"], results["parzen_estimator"][n]["std"]))
