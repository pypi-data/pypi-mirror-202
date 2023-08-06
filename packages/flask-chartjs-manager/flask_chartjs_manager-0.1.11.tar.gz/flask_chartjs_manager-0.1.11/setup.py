# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_chartjs']

package_data = \
{'': ['*'], 'flask_chartjs': ['templates/*']}

install_requires = \
['flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'flask-chartjs-manager',
    'version': '0.1.11',
    'description': '',
    'long_description': '# Flask-ChartJS-Manager\n\nFlask-ChartJS-Manager _(from now on **FCM**)_ provides a simple interface to use ChartJS javascript library with Flask.\n\n```{warning}\n🚧 This package is under heavy development..\n```\n\n## Installation\n\nInstall the extension with pip:\n\n```bash\npip install flask-chartjs-manager\n```\n\nInstall with poetry:\n\n```bash\npoetry add flask-chartjs-manager\n```\n\n## Usage\n\nOnce installed the **FCM** is easy to use. Let\'s walk through setting up a basic application. Also please note that this is a very basic guide: we will be taking shortcuts here that you should never take in a real application.\n\nTo begin we\'ll set up a Flask app:\n\n```python\nfrom flask import Flask\n\napp = Flask(__name__)\n```\n\n### Setting up extension\n\n**FCM** works via a ChartJSManager object. To kick things off, we\'ll set up the `chartjs_manager` by instantiating it and telling it about our Flask app:\n\n```python\nfrom flask_chartjs import ChartJSManager\n\nchartjs_manager = ChartJSManager()\nchartjs_manager.init_app(app)\n```\n\nThis will make available the `chartjs` object into the templates context so you could load the javascript package easily, like this.\nyou can configure a `CHARTJS_LOCAL_PATH` to add a custom location for the package\n\n```html\n<head>\n  {{ chartjs.load() }}\n</head>\n```\n\n### Creating a chart\n\nNow we will construct a basic chart. For this you have to import `Chart` and `DataSet` objects in order to create a new chart.\n\n```python\nfrom flask_chartjs import Chart, DataSet\nfrom flask import render_template\n\n@app.get(\'/chart-example\')\ndef chart_example():\n\n    chart = Chart(\'income-outcome\', \'bar\') # Requires at least an ID and a chart type.\n\n    dataset_income = DataSet(\'Income\', [100,200,300])\n    dataset_outcome = DataSet(\'OutCome\', [50,100,150])\n\n    chart.data.add_labels(\'jan\', \'feb\', \'mar\')\n    chart.data.add_dataset(dataset_income)\n    chart.data.add_dataset(dataset_outcome)\n\n    return render_template(\'path/to/template.html\', my_chart=chart)\n\n```\n\n### Rendering the chart\n\nOnce created you can pass the `Chart` object to render_template and use it likewise.\n\n```html\n<!-- chartjs.load() must be called before this line -->\n<div class="my-classes">{{ chartjs.render(my_chart) }}</div>\n```\n\n## Changelog 0.1.11\n\nAdded new options to personalize using the full power of the ChartJS library. Now you can limit the python code to add the dataset itself and let\nthe configuration and further customization to the actual template level. See the next example.\nIf you add a `%` in front of a value its assumed to be a javascript variable.\nYou have the especial kwarg `datasets` to access directly to the datasets options, as you can observe in the next example. The key is the dataset index.\n\n```html\n<!-- load_chartjs() must be called before this line -->\n<script>\n  function addDollarSign(value, index, ticks) {\n    return "$" + value.toLocaleString();\n  }\n</script>\n<div class="my-classes">\n  {{ chartjs.render(chart, options={ \'datasets\': { \'line\': { \'tension\': 0.4,\n  \'fill\': true, } }, \'elements\': { \'point\': { \'pointStyle\': \'circle\', \'radius\':\n  5, \'hitRadius\': 5, \'hoverRadius\': 5, \'borderWidth\': 5, } }, \'scales\': { \'y\': {\n  \'ticks\': { \'callback\': \'%addDollarSign\' } } } }, datasets={ 0: {\n  \'borderColor\': \'rgba(20, 184, 166, 0.8)\', \'backgroundColor\': \'rgba(20, 184,\n  166, 0.4)\', }, 1: { \'borderColor\': \'rgba(239, 68, 68, 0.8)\',\n  \'backgroundColor\': \'rgba(239, 68, 68, 0.4)\', }, }) }}\n</div>\n```\n',
    'author': 'Sebastian Salinas',
    'author_email': 'seba.salinas.delrio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
