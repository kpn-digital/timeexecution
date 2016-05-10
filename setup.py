
from setuptools import setup
setup(**{'name': 'timeexecution', 'author': 'Niels Lensink', 'author_email': 'niels@elements.nl', 'include_package_data': True, 'long_description': 'Time Execution\n==============\n\n.. image:: https://secure.travis-ci.org/kpn-digital/py-timeexecution.svg?branch=master\n    :target:  http://travis-ci.org/kpn-digital/py-timeexecution?branch=master\n\n.. image:: https://img.shields.io/codecov/c/github/kpn-digital/py-timeexecution/master.svg\n    :target: http://codecov.io/github/kpn-digital/py-timeexecution?branch=master\n\n.. image:: https://img.shields.io/pypi/v/timeexecution.svg\n    :target: https://pypi.python.org/pypi/timeexecution\n\n.. image:: https://readthedocs.org/projects/py-timeexecution/badge/?version=latest\n    :target: http://py-timeexecution.readthedocs.org/en/latest/?badge=latest\n\n\nThis package is designed to record metrics of the application into a backend.\nWith the help of grafana_ you can easily create dashboards with them\n\n\nFeatures\n--------\n\n- Sending data to multiple backends\n- Custom backends\n- Hooks\n\nBackends\n--------\n\n- InfluxDB 0.8\n- Elasticsearch 2.1\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ pip install timeexecution\n\nUsage\n-----\n\nTo use this package you decorate the functions you want to time its execution.\nEvery wrapped function will create a metric consisting of 3 default values:\n\n- `name` - The name of the series the metric will be stored in\n- `value` - The time it took in ms for the wrapped function to complete\n- `hostname` - The hostname of the machine the code is running on\n\nSee the following example\n\n.. code-block:: python\n\n    from time_execution import configure, time_execution\n    from time_execution.backends.influxdb import InfluxBackend\n    from time_execution.backends.elasticsearch import ElasticsearchBackend\n\n    # Setup the desired backend\n    influx = InfluxBackend(host=\'influx\', database=\'metrics\', use_udp=False)\n    elasticsearch = ElasticsearchBackend(\'elasticsearch\', index=\'metrics\')\n\n    # Configure the time_execution decorator\n    configure(backends=[influx, elasticsearch])\n\n    # Wrap the methods where u want the metrics\n    @time_execution\n    def hello():\n        return \'World\'\n\n    # Now when we call hello() and we will get metrics in our backends\n    hello()\n\nThis will result in an entry in the influxdb\n\n.. code-block:: json\n\n    [\n        {\n            "name": "__main__.hello",\n            "columns": [\n                "time",\n                "sequence_number",\n                "value",\n                "hostname",\n            ],\n            "points": [\n                [\n                    1449739813939,\n                    1111950001,\n                    312,\n                    "machine.name",\n                ]\n            ]\n        }\n    ]\n\nAnd the following in Elasticsearch\n\n.. code-block:: json\n\n    [\n        {\n            "_index": "metrics-2016.01.28",\n            "_type": "metric",\n            "_id": "AVKIp9DpnPWamvqEzFB3",\n            "_score": null,\n            "_source": {\n                "timestamp": "2016-01-28T14:34:05.416968",\n                "hostname": "dfaa4928109f",\n                "name": "__main__.hello",\n                "value": 312\n            },\n            "sort": [\n                1453991645416\n            ]\n        }\n    ]\n\n\nHooks\n-----\n\n`time_execution` supports hooks where you can change the metric before its\nbeing send to the backend.\n\nWith a hook you can add additional and change existing fields. This can be\nuseful for cases where you would like to add a column to the metric based on\nthe response of the wrapped function.\n\nA hook will always get 3 arguments:\n\n- `response` - The returned value of the wrapped function\n- `exception` - The raised exception of the wrapped function\n- `metric` - A dict containing the data to be send to the backend\n- `func_args` - Original args received by the wrapped function.\n- `func_kwargs` - Original kwargs received by the wrapped function.\n\nFrom within a hook you can change the `name` if you want the metrics to be split\ninto multiple series.\n\nSee the following example how to setup hooks.\n\n.. code-block:: python\n\n    # Now lets create a hook\n    def my_hook(response, exception, metric, func_args, func_kwargs):\n        status_code = getattr(response, \'status_code\', None)\n        if status_code:\n            return dict(\n                name=\'{}.{}\'.format(metric[\'name\'], status_code),\n                extra_field=\'foo bar\'\n            )\n\n    # Configure the time_execution decorator, but now with hooks\n    configure(backends=[backend], hooks=[my_hook])\n\nManually sending metrics\n------------------------\n\nYou can also send any metric you have manually to the backend. These will not\nadd the default values and will not hit the hooks.\n\nSee the following example.\n\n.. code-block:: python\n\n    loadavg = os.getloadavg()\n    write_metric(\'cpu.load.1m\', value=loadavg[0])\n    write_metric(\'cpu.load.5m\', value=loadavg[1])\n    write_metric(\'cpu.load.15m\', value=loadavg[2])\n\n.. _grafana: http://grafana.org/\n\n\nCustom Backend\n--------------\n\nWriting a custom backend is very simple, all you need to do is create a class\nwith a `write` method. It is not required to extend `BaseMetricsBackend`\nbut in order to easily upgrade I recommend u do.\n\n.. code-block:: python\n\n    from time_execution.backends.base import BaseMetricsBackend\n\n\n    class MetricsPrinter(BaseMetricsBackend):\n        def write(self, name, **data):\n            print(name, data)\n\n\nContribute\n----------\n\nYou have something to contribute ? Great !\nA few things that may come in handy.\n\nTesting in this project is done via docker. There is a docker-compose to easily\nget all the required containers up and running.\n\nThere is a Makefile with a few targets that we use often:\n\n- `make test`\n- `make isort`\n- `make lint`\n- `make build`\n- `make setup.py`\n\nAll of these make targets can be prefixed by `docker/`. This will execute\nthe target inside the docker container instead of on your local machine.\nFor example `make docker/build`.\n', 'url': 'https://github.com/kpn-digital/py-timeexecution', 'version': '1.3.0+6.g92b53db', 'zip_safe': False, 'install_requires': ['influxdb>=2.11', 'elasticsearch>=2.2.0', 'pkgsettings>=0.9.2'], 'packages': ['time_execution', 'time_execution.backends'], 'classifiers': ['Development Status :: 5 - Production/Stable', 'Environment :: Web Environment', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.5', 'Topic :: Internet :: WWW/HTTP', 'Topic :: Software Development :: Libraries :: Python Modules'], 'tests_require': ['tox'], 'description': 'Python project'})