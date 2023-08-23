from tqdm import tqdm
from sklearn.metrics import mean_squared_error, mean_absolute_error
from qcqp_final import validate_detections
from mega_randomizer import randomize
import numpy as np
import pandas as pd
from utils.consts import COMPONENTS


def perform_experiment(distance=2, detections=10):
    randomize(distance=distance, detections=detections)
    validate_detections()
    static = pd.read_csv("data_generation/mega_static.csv")
    corrected = pd.read_csv("data_generation/qcqp.csv")
    corrected = corrected.rename(
        columns={"x": "x_corrected", "y": "y_corrected", "z": "z_corrected"}
    )
    merged = pd.merge(static, corrected, on=["name"])
    merged = merged.drop(columns=["parent", "distance_to_parent", "number"])
    # add mse for each row to column
    merged["mae"] = merged.apply(
        lambda row: mean_absolute_error(
            [row["x"], row["y"], row["z"]],
            [row["x_corrected"], row["y_corrected"], row["z_corrected"]],
        ),
        axis=1,
    )
    # print(merged)
    merged = merged.sort_values(by=["mae"], ascending=False)
    merged = merged.drop(columns=[x for x in merged.columns if x not in ["name", "mae"]])
    components = merged[merged["name"].isin(COMPONENTS)]
    components = components.reset_index(drop=True)
    # print(components)
    mean_mse = np.mean(merged["mae"])
    mean_component_mse = np.mean(components["mae"])
    # print(f"Mean mae: {mean_mse}")
    # print(f"Mean component mae: {mean_component_mse}")
    # print(merged)
    return merged, mean_mse, mean_component_mse

def prepare_csv(n_detections):
    for n_d in n_detections:
        with open(f"results/results_{n_d}.csv", "w") as f:
            f.write("distances,mae,component_mae\n")

def perform_loop():
    empty_df = pd.DataFrame(columns=["name", "mae"])
    distances = [i for i in range(1, 21)]
    n_detections = [3,5,8,10,15,20]
    prepare_csv(n_detections)
    for n_d in tqdm(n_detections):
        for distance in distances:
            mae_list = []
            component_mae_list = []
            for i in range(5):
                merged, mae, component_mae = perform_experiment(distance=distance, detections=n_d)
                empty_df = pd.concat([empty_df,merged])
                mae_list.append(mae)
                component_mae_list.append(component_mae)
            mae_mean = np.mean(mae_list)
            component_mae_mean = np.mean(component_mae_list)
            with open(f"results/results_{n_d}.csv", "a") as f:
                f.write(f"{distance},{mae_mean},{component_mae_mean}\n")
    
    empty_df = empty_df[empty_df["name"].isin(COMPONENTS)]
    empty_df = empty_df.groupby(["name"]).mean()
    empty_df = empty_df.sort_values(by=["mae"], ascending=False)
    print(empty_df)
    #save to csv
    empty_df.to_csv("results/mean_mae.csv")

            
def perform_once():
    merged, mae, component_mae = perform_experiment(distance=2, detections=10)
    print(merged)
    print(f"Mean mae: {mae}")
    print(f"Mean component mae: {component_mae}")

if __name__ == "__main__":
    perform_loop()
    # perform_once()