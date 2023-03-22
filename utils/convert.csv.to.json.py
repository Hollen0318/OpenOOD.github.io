import pandas as pd
import json
import os

def csv_to_multiple_json_files(input_csv_file, output_path):
    # Read the CSV file
    df = pd.read_csv(input_csv_file)

    # Extract the first float value from the strings in the "NearOOD AUROC" and "FarOOD AUROC" columns
    df["In-Distribution Accuracy Mean"] = df["In-Distribution Accuracy"].str.extract(r"(\d+\.\d+)", expand=False)
    df["NearOOD AUROC Mean"] = df["NearOOD AUROC"].str.extract(r"(\d+\.\d+)", expand=False)
    df["FarOOD AUROC Mean"] = df["FarOOD AUROC"].str.extract(r"(\d+\.\d+)", expand=False)

    # Iterate through the DataFrame, creating a JSON file for each unique combination of 'Paper' and 'Alias' values
    for _, group in df.groupby(["Paper", "Alias"]):
        # Get the 'Paper' and 'Alias' values and use them as the filename
        paper = group.iloc[0]["Paper"]
        alias = group.iloc[0]["Alias"]
        output_json_file = f"{paper}_{alias}.json"

        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Join the output path with the output JSON file name
        output_file_path = os.path.join(output_path, output_json_file)

        # Drop the 'Paper' and 'Alias' columns and convert the remaining DataFrame to a JSON object
        # group = group.drop(["Paper", "Alias"], axis=1)
        json_data = group.to_dict(orient="records")

        # Write the JSON object to a file, one record per line
        with open(output_file_path, "w") as file:
            for record in json_data:
                file.write(json.dumps(record, indent=2) + "\n")

        print(f"Created {output_file_path}")

if __name__ == "__main__":
    input_csv_file = "input.csv"
    output_path = "/home/hz271/Research/OpenOOD.github.io/model_info"
    csv_to_multiple_json_files(input_csv_file, output_path)
