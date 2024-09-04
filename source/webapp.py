import os
import json
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

template_folder = os.path.join(app.root_path, 'templates')
env = Environment(loader=FileSystemLoader(template_folder))
env.globals['zip'] = zip
env.globals['url_for'] = app.jinja_env.globals.get('url_for')
app.jinja_env = env

def load_data():
    data = {}
    results_dir = os.path.join(app.root_path, 'results')
    for filename in os.listdir(results_dir):
        if filename.endswith('.json'):
            region = os.path.splitext(filename)[0]
            file_path = os.path.join(results_dir, filename)
            with open(file_path, 'r') as file:
                data[region] = json.load(file)
    return data


def get_all_instance_types(data):
    all_instance_types = set()
    for region_data in data.values():
        all_instance_types.update(region_data.keys())
    return all_instance_types


@app.route('/')
def index():
    data = load_data()
    all_instance_types = get_all_instance_types(data)
    regions = list(data.keys())
    instance_type_data = []

    for instance_type in all_instance_types:
        prices = []
        for region in regions:
            price = data[region].get(instance_type, '-')
            prices.append(price)
        instance_type_data.append({
            'instance_type': instance_type,
            'prices': prices
        })

    return render_template('index.html', instance_type_data=instance_type_data, regions=regions)


if __name__ == '__main__':
    app.run(debug=True)
