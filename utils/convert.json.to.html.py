import os
import json
from jinja2 import Environment, FileSystemLoader

def read_json_files(folder):
    models = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r") as file:
                model = json.load(file)
                models.append(model)
    return models

def render_template(models, template_file, output_file):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)

    rendered_html = template.render(models=models)

    with open(output_file, "w") as file:
        file.write(rendered_html)

if __name__ == "__main__":
    models_folder = "/home/hz271/Research/OpenOOD.github.io/model_info"
    models = read_json_files(models_folder)

    template_file = "table_template.html.j2"
    output_file = "/home/hz271/Research/OpenOOD.github.io/output.html"
    render_template(models, template_file, output_file)
