import pandas as pd
import json
import os
import numpy as np


temp = pd.read_csv("./papers.csv")
temp = temp.set_index("Alias")
paper_dict = temp.to_dict("index")


def csv_to_multiple_json_files(input_csv_file, output_root):
    # Read the CSV file
    df = pd.read_csv(input_csv_file)

    # Extract the first float value from the strings in the "NearOOD AUROC" and "FarOOD AUROC" columns
    df["ID_Accuracy_Mean"] = df["ID_Accuracy"].str.extract(r"(\d+\.\d+)", expand=False)
    df["Near-OOD_AUROC_Mean"] = df["Near-OOD_AUROC"].str.extract(r"(\d+\.\d+)", expand=False)
    df["Far-OOD_AUROC_Mean"] = df["Far-OOD_AUROC"].str.extract(r"(\d+\.\d+)", expand=False)

    # Rank methods according to NearOOD AUROC by default
    df["Rank"] = df["Near-OOD_AUROC_Mean"].rank(ascending=False, method='first').astype(int)

    # Set up saving directory
    dataset = input_csv_file.split('/')[-1].split('.')[0]
    saving_dir = os.path.join(output_root, dataset)
    os.makedirs(saving_dir, exist_ok=True)

    for i in range(len(df)):
        training = df.iloc[i]["Training"]
        postproc = df.iloc[i]["Postprocessor"]
        extra_desc = df.iloc[i]["Additional_Description"]
        output_filename = f"{training}_{postproc}"
        if not np.isnan(extra_desc):
            output_filename += f"_{extra_desc}"
        output_filename += ".json"
        json_data = df.iloc[i:i+1].to_dict("records")
        json_data[0]["Training_Link"] = paper_dict[training]["Link"] if training in paper_dict else ""
        json_data[0]["PP_Link"] = paper_dict[postproc]["Link"]
        if np.isnan(extra_desc):
            json_data[0]["Additional_Description"] = ""

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