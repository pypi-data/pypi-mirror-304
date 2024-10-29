from imputegap.tools.evaluator import comprehensive_evaluation

#datasets = ["eeg-test"]
v1_datasets = ["chlorine"]
#v2_datasets = ["chlorine", "drift", "climate"]
#v3_datasets = ["climate"]

opti_1 = {"optimizer": "bayesian", "options": {"n_calls": 5, "n_random_starts": 50, "acq_func": "gp_hedge", "selected_metrics":"RMSE"}}
optimizers = [opti_1]

#algorithms = ["cdrec", "stmvl"]
algorithms = ["mean", "cdrec", "stmvl", "iim", "mrnn"]

scenarios = ["mcar"]
#scenarios = ["mcar", "missing_percentage"]

#x_axis = [0.05]
x_axis = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
#x_axis = [0.05, 0.1, 0.2]

comprehensive_evaluation(datasets=v1_datasets, optimizers=optimizers, algorithms=algorithms, scenarios=scenarios, x_axis=x_axis)

