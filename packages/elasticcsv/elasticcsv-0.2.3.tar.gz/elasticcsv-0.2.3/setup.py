# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elasticcsv']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'elasticsearch<8.0',
 'pandas>=2.0.0,<3.0.0',
 'python-box>=7.0.1,<8.0.0',
 'pytz>=2023.3,<2024.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'elasticcsv',
    'version': '0.2.3',
    'description': 'elasticsearch csv upload download utility',
    'long_description': '# Elastic CSV Loader\n\nThis command line utility loads csv file into an elasticsearch index, using a provided yaml config file.\n\n`load-csv` considerations:\n\n- CSV files MUST include a header with field names\n- Header field names will be used as elastic index fields\n- A `@timestamp` and `date`  fields will be added to all indexed docs\n  - A `date` logic date could be forced through command parameter.\n- Depending on `elastic_index.data_format.parent_data_object` value, all original csv header fields\n  will be arranged under a `data` parent object.\n\nIndexed data will use the same field names that\n\n`download-index` considerations:\n\n- If csv file is an existing file the download process will **append** data including headers\n- You have to rename or delete previous csv file if you want to start fresh.\n\n## Install\n\n### Dependencies\n\n- `Python` 3.8 or higher\n- `pip` package manager\n\n```shell\npip install --upgrade elasticcsv\n```\n\n## Run\n\n### Elastic Connection Config\n\nConnection configuration is based in a YAML text file (`connection.yaml`) that must be present in\ncommand directory.\n\nSample `connection.yaml`\n\n\n```yaml\nelastic_connection:\n  proxies:\n    http: "http://user:pass@proxy.url:8080"\n    https: "http://user:pass@proxy.url:8080"\n  user: myuser\n  password: mypassword\n  node: my.elastic.node\n  port: 9200\nelastic_index:\n  data_format:\n    parent_data_object: true\n```\n\n### Run command\n\n```text\n❯ python elasticcsv/csv2es.py load-csv --help\nUsage: csv2es.py load-csv [OPTIONS]\n\n  Loads csv to elastic index\n\nOptions:\n  --csv PATH               CSV File  [required]\n  --csv_offset INT         CSV File offset\n  --sep TEXT               CSV field sepator  [required]\n  --index TEXT             Elastic Index  [required]\n  --csv-date-format TEXT   date format for *_date columns as for ex:\n                           \'%Y-%m-%d\'\n  --logic_date [%Y-%m-%d]  Date reference for interfaces\n  -d, --delete-if-exists   Flag for deleting index before running load\n  --help                   Show this message and exit.\n\n```\n> Python date formats references: [String Format Time](https://www.geeksforgeeks.org/how-to-format-date-using-strftime-in-python/)\n\n```text\n❯ python elasticcsv/csv2es.py download-index --help\nUsage: csv2es.py download-index [OPTIONS]\n\n  Download index to csv file\n\nOptions:\n  --csv PATH              CSV File  [required]\n  --sep TEXT              CSV field sepator  [required]\n  --index TEXT            Elastic Index  [required]\n  -d, --delete-if-exists  Flag for deleting csv file before download\n  --help                  Show this message and exit.\n\n```\nExample:\n\n```text\ncsv2es load-csv --csv ./pathtomyfile/file.csv --index myindex --sep ";"\n\ncsv2es download-index --csv ./pathtomyfile/file.csv --index myindex --sep ";" -d\n```\n',
    'author': 'J. Andres Guerrero',
    'author_email': 'jaguerrero@caixabanktech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
