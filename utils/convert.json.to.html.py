import os
import json
from jinja2 import Environment, FileSystemLoader

def read_json_files(folder):
    models_by_folder = {}
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            models = []
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".json"):
                    filepath = os.path.join(subfolder_path, filename)
                    with open(filepath, "r") as file:
                        model = json.load(file)
                        models.append(model)
            models_by_folder[subfolder] = models
    return models_by_folder

def render_template(models, folder, template_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)

    # Sort the models based on the "Rank" column in ascending order
    sorted_models = sorted(models, key=lambda x: x['Rank'])

    rendered_html = template.render(models=sorted_models, dataset=folder)

    output_file = f"{folder}.html"
    output_file_path = os.path.join(output_folder, output_file)
    with open(output_file_path, "w") as file:
        file.write(rendered_html)

if __name__ == "__main__":
    models_folder = "/home/hz271/Research/OpenOOD.github.io/model_info"
    models_by_folder = read_json_files(models_folder)

    template_file = "table_template.html.j2"
    output_folder = "/home/hz271/Research/OpenOOD.github.io/output"

    for folder, models in models_by_folder.items():
        render_template(models, folder, template_file, output_folder)

# convert.json.to.html
# 1. 读取model_info里的数据集文件夹
# 2. 对每一个数据集，生成一个将所有json文件整合的html (里面只有table)，以数据集命名

# index.html会自动去找到这个html table放到网页的leaderboard container里面