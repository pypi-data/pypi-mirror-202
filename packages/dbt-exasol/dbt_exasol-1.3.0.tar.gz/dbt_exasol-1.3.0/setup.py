# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt',
 'dbt.adapters',
 'dbt.adapters.exasol',
 'dbt.include',
 'dbt.include.exasol',
 'tests',
 'tests.functional',
 'tests.functional.adapter',
 'tests.functional.adapter.utils',
 'tests.functional.adapter.utils.data_types']

package_data = \
{'': ['*'],
 'dbt.include.exasol': ['macros/*',
                        'macros/materializations/*',
                        'macros/utils/*']}

install_requires = \
['dbt-core>=1.3,<1.4',
 'dbt-tests-adapter>=1.3,<1.4',
 'pyexasol>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'dbt-exasol',
    'version': '1.3.0',
    'description': 'Adapter to dbt-core for warehouse Exasol',
    'long_description': "# dbt-exasol\n**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.\n\nPlease see the dbt documentation on **[Exasol setup](https://docs.getdbt.com/reference/warehouse-setups/exasol-setup)** for more information on how to start using the Exasol adapter.\n\n# Current profile.yml settings\n<File name='profiles.yml'>\n\n```yaml\ndbt-exasol:\n  target: dev\n  outputs:\n    dev:\n      type: exasol\n      threads: 1\n      dsn: HOST:PORT\n      user: USERNAME\n      password: PASSWORD\n      dbname: db\n      schema: SCHEMA\n```\n\n#### Optional parameters\n<ul>\n  <li><strong>connection_timeout</strong>: defaults to pyexasol default</li>\n  <li><strong>socket_timeout</strong>: defaults to pyexasol default</li>\n  <li><strong>query_timeout</strong>: defaults to pyexasol default</li>\n  <li><strong>compression</strong>: default: False</li>\n  <li><strong>encryption</strong>: default: False</li>\n  <li><strong>protocol_version</strong>: default: v3</li>\n  <li><strong>row_separator</strong>: default: CRLF for windows - LF otherwise</li>\n  <li><strong>timestamp_format</strong>: default: YYYY-MM-DDTHH:MI:SS.FF6</li>\n</ul>\n\n# Known isues\n\n## >=1.3 Python model not yet supported - WIP\n- Please follow [this pull request](https://github.com/tglunde/dbt-exasol/pull/59) \n\n## Breaking changes with release 1.2.2\n- Timestamp format defaults to YYYY-MM-DDTHH:MI:SS.FF6\n\n## SQL functions compatibility\n\n### split_part\nThere is no equivalent SQL function in Exasol for split_part.\n\n### listagg part_num\nThe SQL function listagg in Exasol does not support the num_part parameter.\n\n## Utilities shim package\nIn order to support packages like dbt-utils and dbt-audit-helper, we needed to create the [shim package exasol-utils](https://github.com/tglunde/exasol-utils). In this shim package we need to adapt to parts of the SQL functionality that is not compatible with Exasol - e.g. when 'final' is being used which is a keyword in Exasol. Please visit [Adaopter dispatch documentation](https://docs.getdbt.com/guides/advanced/adapter-development/3-building-a-new-adapter#adapter-dispatch) of dbt-labs for more information. \n# Reporting bugs and contributing code\n- Please report bugs using the issues\n\n# Releases\n\n[GitHub Releases](https://github.com/tglunde/dbt-exasol/releases)\n",
    'author': 'Torsten Glunde',
    'author_email': 'torsten.glunde@alligator-company.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://alligatorcompany.gitlab.io/dbt-exasol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
