import pandas as pd
import json
import os
import numpy as np


def csv_to_multiple_json_files(input_csv_file, output_root):
    # Read the CSV file
    df = pd.read_csv(input_csv_file)

    # Extract the first float value from the strings in the "NearOOD AUROC" and "FarOOD AUROC" columns
    df["ID Accuracy Mean"] = df["ID Accuracy"].str.extract(r"(\d+\.\d+)", expand=False)
    df["Near-OOD AUROC Mean"] = df["Near-OOD AUROC"].str.extract(r"(\d+\.\d+)", expand=False)
    df["Far-OOD AUROC Mean"] = df["Far-OOD AUROC"].str.extract(r"(\d+\.\d+)", expand=False)

    # Set up saving directory
    dataset = input_csv_file.split('/')[-1].split('.')[0]
    saving_dir = os.path.join(output_root, dataset)
    os.makedirs(saving_dir, exist_ok=True)

    for i in range(len(df)):
        training = df.iloc[i]["Training"]
        postproc = df.iloc[i]["Postprocessor"]
        extra_desc = df.iloc[i]["Additional Description"]
        output_filename = f"{training}_{postproc}"
        if not np.isnan(extra_desc):
            output_filename += f"_{extra_desc}"
        output_filename += ".json"
        json_data = df.iloc[i:i+1].to_dict("records")

        # Write the JSON object to a file, one record per line
        with open(os.path.join(saving_dir, output_filename), "w") as file:
            for record in json_data:
                file.write(json.dumps(record, indent=2) + "\n")

        print(f"Created {os.path.join(saving_dir, output_filename)}")


if __name__ == "__main__":
    file_id = "cifar10"

    input_csv_file = f"../results/{file_id}.csv"
    output_root = "../model_info"
    csv_to_multiple_json_files(input_csv_file, output_root)