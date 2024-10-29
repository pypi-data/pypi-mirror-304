import time
from imputegap.tools import utils
from imputegap.recovery.imputation import Imputation
from imputegap.recovery.manager import TimeSeries

import os
import matplotlib.pyplot as plt


def generate_plots(runs_plots_scores, save_dir="./report"):
    """
    Generate and save plots for each metric and scenario based on provided scores.

    Parameters
    ----------
    runs_plots_scores : dict
        Dictionary containing scores and timing information for each dataset, scenario, and algorithm.
    save_dir : str, optional
        Directory to save generated plots (default is "./report").

    Returns
    -------
    None

    Notes
    -----
    Saves generated plots in `save_dir`, categorized by dataset, scenario, and metric.
    """
    os.makedirs(save_dir, exist_ok=True)

    for dataset, scenario_data in runs_plots_scores.items():
        for scenario, algo_data in scenario_data.items():
            # Iterate over each metric, generating separate plots
            for metric in ["RMSE", "MAE", "MI", "CORRELATION", "imputation_time"]:
                plt.figure()
                has_data = False  # Flag to check if any data is added to the plot

                # Iterate over each algorithm and plot them in the same figure
                for algorithm, optimizer_data in algo_data.items():
                    x_vals = []
                    y_vals = []
                    for optimizer, x_data in optimizer_data.items():
                        for x, values in x_data.items():
                            # Differentiate between score metrics and "imputation" time
                            if metric == "imputation_time":
                                # Collect "imputation" time data
                                if "imputation" in values["times"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["times"]["imputation"])
                            else:
                                # Collect score metrics data
                                if metric in values["scores"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["scores"][metric])

                    # Only plot if there are values to plot
                    if x_vals and y_vals:
                        # Normalize score metrics (skip for imputation time)
                        if metric != "imputation_time":
                            y_min, y_max = min(y_vals), max(y_vals)
                            y_vals = [(y - y_min) / (y_max - y_min) if y_max != y_min else 0.5 for y in y_vals]

                        # Sort x and y values by x for correct spacing
                        sorted_pairs = sorted(zip(x_vals, y_vals))
                        x_vals, y_vals = zip(*sorted_pairs)

                        # Plot each algorithm as a line with scattered points
                        plt.plot(x_vals, y_vals, label=f"{algorithm}")
                        plt.scatter(x_vals, y_vals)
                        has_data = True

                # Save plot only if there is data to display
                if has_data:
                    # Set plot titles and labels
                    title_metric = "Imputation Time" if metric == "imputation_time" else f"Normalized {metric}"
                    ylabel_metric = "Imputation Time (seconds)" if metric == "imputation_time" else f"Normalized {metric}"

                    plt.title(f"{dataset} | {scenario} | {title_metric}")
                    plt.xlabel(f"{scenario} rate of missing values and missing series")
                    plt.ylabel(ylabel_metric)
                    plt.xlim(0.0, 0.85)

                    # Customize x-axis ticks
                    x_points = [0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
                    plt.xticks(x_points, [f"{int(tick * 100)}%" for tick in x_points])
                    plt.grid(True, zorder=0)
                    plt.legend()

                    # Define a unique filename
                    metric_name = "imputation_time" if metric == "imputation_time" else metric
                    filename = f"{dataset}_{scenario}_{metric_name}.jpg"
                    filepath = os.path.join(save_dir, filename)

                    # Save the figure
                    plt.savefig(filepath)
                plt.close()  # Close to avoid memory issues

    print("\nAll plots recorded in", save_dir)


def generate_reports(runs_plots_scores, save_dir="./report"):
    """
    Generate and save a text report of metrics and timing for each dataset, algorithm, and scenario.

    Parameters
    ----------
    runs_plots_scores : dict
        Dictionary containing scores and timing information for each dataset, scenario, and algorithm.
    save_dir : str, optional
        Directory to save the report file (default is "./report").

    Returns
    -------
    None

    Notes
    -----
    The report is saved in a "report.txt" file in `save_dir`, organized in tabular format.
    """

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "report.txt")
    with open(save_path, "w") as file:
        # Define header with time columns included
        header = "| dataset_value | algorithm_value | optimizer_value | scenario_value | x_value | RMSE | MAE | MI | CORRELATION | time_contamination | time_optimization | time_imputation |\n"
        file.write(header)

        for dataset, algo_data in runs_plots_scores.items():
            for algorithm, opt_data in algo_data.items():
                for optimizer, scenario_data in opt_data.items():
                    for scenario, x_data in scenario_data.items():
                        for x, values in x_data.items():
                            metrics = values["scores"]
                            times = values["times"]

                            # Retrieve each timing value, defaulting to None if absent
                            contamination_time = times.get("contamination", None)
                            optimization_time = times.get("optimization", None)
                            imputation_time = times.get("imputation", None)

                            # Create a report line with timing details
                            line = (
                                f"| {dataset} | {algorithm} | {optimizer} | {scenario} | {x} "
                                f"| {metrics.get('RMSE')} | {metrics.get('MAE')} | {metrics.get('MI')} "
                                f"| {metrics.get('CORRELATION')} | {contamination_time} sec | {optimization_time} sec"
                                f"| {imputation_time} sec |\n"
                            )
                            file.write(line)

    print("\nReport recorded in", save_path)


def config_optimization(opti_mean, ts_test, scenario, algorithm):
    """
    Configure and execute optimization for selected imputation algorithm and scenario.

    Parameters
    ----------
    opti_mean : float
        Mean parameter for contamination.
    ts_test : TimeSeries
        TimeSeries object containing dataset.
    scenario : str
        Type of contamination scenario (e.g., "mcar", "mp", "blackout").
    algorithm : str
        Imputation algorithm to use.

    Returns
    -------
    BaseImputer
        Configured imputer instance with optimal parameters.
    """

    if scenario == "mcar":
        infected_matrix_opti = ts_test.Contaminate.mcar(ts=ts_test.data, series_impacted=opti_mean, missing_rate=opti_mean, use_seed=True, seed=42)
    elif scenario == "mp":
        infected_matrix_opti = ts_test.Contaminate.missing_percentage(ts=ts_test.data, series_impacted=opti_mean, missing_rate=opti_mean)
    else:
        infected_matrix_opti = ts_test.Contaminate.blackout(ts=ts_test.data, missing_rate=opti_mean)

    if algorithm == "cdrec":
        i_opti = Imputation.MatrixCompletion.CDRec(infected_matrix_opti)
    elif algorithm == "stmvl":
        i_opti = Imputation.PatternSearch.STMVL(infected_matrix_opti)
    elif algorithm == "iim":
        i_opti = Imputation.Statistics.IIM(infected_matrix_opti)
    elif algorithm == "mrnn":
        i_opti = Imputation.DeepLearning.MRNN(infected_matrix_opti)
    elif algorithm == "mean":
        i_opti = Imputation.Statistics.MeanImpute(infected_matrix_opti)

    return i_opti


def comprehensive_evaluation(datasets=[], optimizers=[], algorithms=[], scenarios=[], x_axis=[], save_dir="./report", already_optimized=False):
    """
    Execute a comprehensive evaluation of imputation algorithms over multiple datasets and scenarios.

    Parameters
    ----------
    datasets : list of str
        List of dataset names to evaluate.
    optimizers : list of dict
        List of optimizers with their configurations.
    algorithms : list of str
        List of imputation algorithms to test.
    scenarios : list of str
        List of contamination scenarios to apply.
    x_axis : list of float
        List of missing rates for contamination.
    save_dir : str, optional
        Directory to save reports and plots (default is "./report").
    already_optimized : bool, optional
        If True, skip parameter optimization (default is False).

    Returns
    -------
    None

    Notes
    -----
    Runs contamination, imputation, and evaluation, then generates plots and a summary report.
    """

    print("initialization of the comprehensive evaluation. It can take time...\n")

    for dataset in datasets:

        runs_plots_scores = {}

        print("1. evaluation launch for", dataset, "\n")
        ts_test = TimeSeries()

        header = False
        if dataset == "eeg":
            header = True

        ts_test.load_timeseries(data=utils.search_path(dataset), header=header)
        start_time_opti = 0
        end_time_opti = 0

        for scenario in scenarios:
            print("2. contamination of", dataset, "with scenario", scenario, "\n")

            for algorithm in algorithms:
                has_been_optimized = False
                print("3. algorithm selected", algorithm, "\n")

                for x in x_axis:
                    print("4. missing values (series&values) set to", x, "for x_axis\n")

                    start_time_contamination = time.time()  # Record start time
                    if scenario == "mcar":
                        infected_matrix = ts_test.Contaminate.mcar(ts=ts_test.data, series_impacted=x, missing_rate=x, use_seed=True, seed=42)
                    elif scenario == "mp":
                        infected_matrix = ts_test.Contaminate.missing_percentage(ts=ts_test.data, series_impacted=x, missing_rate=x)
                    else:
                        infected_matrix = ts_test.Contaminate.blackout(ts=ts_test.data, missing_rate=x)
                    end_time_contamination = time.time()

                    for optimizer in optimizers:
                        optimizer_gt = {"ground_truth": ts_test.data, **optimizer}

                        if algorithm == "cdrec":
                            algo = Imputation.MatrixCompletion.CDRec(infected_matrix)
                        elif algorithm == "stmvl":
                            algo = Imputation.PatternSearch.STMVL(infected_matrix)
                        elif algorithm == "iim":
                            algo = Imputation.Statistics.IIM(infected_matrix)
                        elif algorithm == "mrnn":
                            algo = Imputation.DeepLearning.MRNN(infected_matrix)
                        elif algorithm == "mean":
                            algo = Imputation.Statistics.MeanImpute(infected_matrix)

                        if not has_been_optimized and not already_optimized and algorithm != "mean":
                            print("5. AutoML to set the parameters", optimizer, "\n")
                            start_time_opti = time.time()  # Record start time
                            i_opti = config_optimization(0.35, ts_test, scenario, algorithm)
                            i_opti.impute(user_defined=False, params=optimizer_gt)
                            utils.save_optimization(optimal_params=i_opti.parameters, algorithm=algorithm, dataset=dataset, optimizer="e")
                            has_been_optimized = True
                            end_time_opti = time.time()

                        if algorithm != "mean":
                            opti_params = utils.load_parameters(query="optimal", algorithm=algorithm, dataset=dataset, optimizer="e")
                            print("6. imputation", algorithm, "with optimal parameters", *opti_params)

                        else :
                            opti_params = None

                        start_time_imputation = time.time()  # Record start time
                        algo.impute(params=opti_params)
                        end_time_imputation = time.time()

                        algo.score(raw_matrix=ts_test.data, imputed_matrix=algo.imputed_matrix)

                        time_contamination = end_time_contamination - start_time_contamination
                        time_opti = end_time_opti - start_time_opti
                        time_imputation = end_time_imputation - start_time_imputation

                        dic_timing = {"contamination": time_contamination, "optimization": time_opti, "imputation": time_imputation}

                        dataset_s = dataset
                        if "-" in dataset:
                            dataset_s = dataset.replace("-", "")

                        optimizer_value = optimizer.get('optimizer')  # or optimizer['optimizer']

                        runs_plots_scores.setdefault(str(dataset_s), {}).setdefault(str(scenario), {}).setdefault(
                            str(algorithm), {}).setdefault(str(optimizer_value), {})[str(x)] = {
                            "scores": algo.metrics,
                            "times": dic_timing
                        }

                        print("runs_plots_scores", runs_plots_scores)

    print("runs_plots_scores", runs_plots_scores)
    generate_plots(runs_plots_scores, save_dir)
    generate_reports(runs_plots_scores, save_dir)
