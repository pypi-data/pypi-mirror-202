# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['profyle',
 'profyle.database',
 'profyle.deps',
 'profyle.middleware',
 'profyle.models']

package_data = \
{'': ['*'], 'profyle': ['web/static/*', 'web/static/libs/*', 'web/templates/*']}

install_requires = \
['fastapi>=0.70.0',
 'jinja2>=3.1.2,<4.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'viztracer>=0.15.6,<0.16.0']

entry_points = \
{'console_scripts': ['profyle = profyle.main:app']}

setup_kwargs = {
    'name': 'profyle',
    'version': '0.0.13',
    'description': 'Profyle, a development tool for analysing and managing python traces',
    'long_description': '# Profyle\n### Development tool for analysing and managing python traces\n\n<a href="https://pypi.org/project/profyle" target="_blank">\n    <img src="https://img.shields.io/pypi/v/profyle" alt="Package version">\n</a>\n<a href="https://pypi.org/project/profyle" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/profyle.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n\n## Why do you need Profyle?\n### Bottlenecks\nWith Profyle you can easily detect where in your code you have a bottleneck, just analize the trace and see what function or operation is taking most of the request execution time\n\n### Enhance performace\nAnalize the traces and decide which parts of your code should be improved\n\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install profyle\n\n---> 100%\n```\n\n</div>\n\n## Example\n\n### 1. Implement\nIn order to track all your API requests you must implement the <code>ProfyleMiddleware</code>\n<details markdown="1">\n<summary>FastAPI</summary>\n\n```Python\nfrom fastapi import FastAPI\nfrom profyle.middleware.fastapi import ProfyleMiddleware\n\napp = FastAPI()\napp.add_middleware(ProfyleMiddleware)\n\n@app.get("/items/{item_id}")\nasync def read_item(item_id: int):\n    return {"item_id": item_id}\n```\n</details>\n\n<details markdown="1">\n<summary>Flask</summary>\n\n```Python\nfrom flask import Flask\nfrom profyle.middleware.flask import ProfyleMiddleware\n\napp = Flask(__name__)\n\napp.wsgi_app = ProfyleMiddleware(app.wsgi_app)\n\n@app.route("/")\ndef hello_world():\n    return "<p>Hello, World!</p>"\n```\n</details>\n\n<details markdown="1">\n<summary>Django</summary>\nSoon..\n</details>\n\n### 2. Run\n* Run the web server:\n\n<div class="termy">\n\n```console\n$ profyle start\n\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\nINFO:     Started reloader process [28720]\nINFO:     Started server process [28722]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\n```\n\n</div>\n\n### 3. List\n* List all requests tracing:\n\n![Alt text](https://github.com/vpcarlos/profyle/blob/main/docs/img/traces.png?raw=true "Traces")\n\n### 4. Analyze\n* Profyle stands on the shoulder of giants: <a href="https://github.com/gaogaotiantian/viztracer" class="external-link" target="_blank">Viztracer</a> and  <a href="https://github.com/google/perfetto" class="external-link" target="_blank">Perfetto</a>\n* Detailed function entry/exit information on timeline with source code\n* Super easy to use, no source code change for most features, no package dependency\n* Supports threading, multiprocessing, subprocess and async\n* Powerful front-end, able to render GB-level trace smoothly\n* Works on Linux/MacOS/Window\n\n![Alt text](https://github.com/vpcarlos/profyle/blob/main/docs/img/trace1.png?raw=true "Trace1")\n\n![Alt text](https://github.com/vpcarlos/profyle/blob/main/docs/img/trace2.png?raw=true "Trace2")\n\n\n\n## CLI Commands\n### start\n* Start the web server and view profile traces\n<div class="termy">\n\n```console\n$ profyle start\n\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\nINFO:     Started reloader process [28720]\nINFO:     Started server process [28722]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\n```\n\n</div>\n\n### clean\n* Delete all profile traces\n<div class="termy">\n\n```console\n$ profyle clean\n\n10 traces removed \n```\n\n</div>\n\n### check\n* Check traces DB size\n<div class="termy">\n\n```console\n$ profyle check\n\nDB size: 30MB\n```\n\n</div>',
    'author': 'Carlos Valdivia',
    'author_email': 'vpcarlos97@gmail.com',
    'maintainer': 'Carlos Valdivia',
    'maintainer_email': 'vpcarlos97@gmail.com',
    'url': 'https://github.com/vpcarlos/profyle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
