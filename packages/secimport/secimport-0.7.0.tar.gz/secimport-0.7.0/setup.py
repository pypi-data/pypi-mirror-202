# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secimport',
 'secimport.backends.bpftrace_backend',
 'secimport.backends.common',
 'secimport.backends.dtrace_backend']

package_data = \
{'': ['*'],
 'secimport': ['profiles/*'],
 'secimport.backends.bpftrace_backend': ['actions/*', 'filters/*', 'probes/*'],
 'secimport.backends.dtrace_backend': ['actions/*',
                                       'filters/*',
                                       'headers/*',
                                       'probes/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['secimport = secimport.cli:main']}

setup_kwargs = {
    'name': 'secimport',
    'version': '0.7.0',
    'description': 'A sandbox/supervisor for python modules.',
    'long_description': '# secimport\n\n`secimport` is a cross-platform sandbox toolkit that traces your Python application and enforces privileges per module in your code in runtime. It uses backends like bpftrace (eBPF) and dtrace under the hood.\n\n## Why It\'s Awesome\n\n- Trace which syscalls are called by each module in your code.\n  - `secimport` uses USDT (Userland Statically Defined Tracing) probes in the runtime (Python interpreter for example) using eBPF and dtrace instrumentation scripts.\n  - Audit the flow of your application at user-space/os/kernel level\n- Reduce supply chain attack and RCE vectors by restricting modules/packages inside your production environment.\n- No performance impact (see [Performance](https://github.com/avilum/secimport/wiki/Performance-Benchmarks)).\n- Don\'t change the way you code!\n- Supports `Python` at the moment\n  -  `Go` is under development\n\n\n## Installation\nFor evaluation, we highly recommend the QuickStart with <a href="#Docker">Docker</a> instead of self-installing.<br>\nIf you are not using Docker, follow <a href="https://github.com/avilum/secimport/wiki/Installation">Installation</a> to install eBPF or DTrace.\n- To install secimport from git clone: `python3 -m pip install -e .`\n- To install secimport from pypi (latest stable release): `python3 -m pip install secimport`\n\n\n## Docker\nThe quickest way to evaluate `secimport` is to use our [Docker container](docker/README.md), which includes `bpftrace` (`ebpf`) and other plug-and-play examples.\n\n## Quick Start - Using the CLI\nTo run an end-to-end interactive example:\n1. Build a docker with custom kernel that matches your existing OS kernel version\n    ```\n    ➜  secimport ✗ cd docker/\n    ➜  docker ✗ ./build.sh\n    ```\n2. Run the container\n    ```\n    ➜  docker ✗ ./run.sh\n    Running temporary container...\n\n    root@f05d2c33b0b3:/workspace#\n    ```\n3. Use the CLI\n    ```\n    root@f05d2c33b0b3:/workspace# secimport interactive\n\n    Let\'s create our first tailor-made sandbox with secimport!\n    - A python shell will be opened\n    - The behavior will be recorded.\n\n    OK? (y): y\n    >>> secimport trace\n\n    TRACING: [\'/workspace/secimport/profiles/trace.bt\', \'-c\', \'/workspace/Python-3.10.0/python\', \'-o\', \'trace.log\']\n\n                            Press CTRL+D/CTRL+C to stop the trace;\n\n    Python 3.10.0 (default, Apr  9 2023, 17:19:17) [GCC 9.4.0] on linux\n    Type "help", "copyright", "credits" or "license" for more information.\n    >>> import ...\n\n\n    ```\n## Sandbox Your Program (Using the CLI)\n`secimport trace` will start a bpftrace program that will log all the syscalls for all the modules in your application into a file.<br>\nOnce you covered the logic you would like to or sandbox and you\'re satisfied, hit `CTRL+C` or `CTRL+D` or wait for the program to finish.\n```\n$ secimport trace\n$ secimport trace -h\n$ secimport trace_pid 123\n$ secimport trace_pid -h\n```\n\nThen, build a sandbox from the trace using the `build` command:\n```\n# secimport build\n$ secimport build -h\n```\n\nFinally, run the sandbox with the `run` command:\n```\n$ secimport run\n$ secimport run --entrypoint my_custom_main.py\n$ secimport run --entrypoint my_custom_main.py --stop_on_violation=true\n$ secimport run --entrypoint my_custom_main.py --kill_on_violation=true\n$ secimport run --sandbox_executable /path/to/my_sandbox.bt --pid 2884\n$ secimport run --sandbox_executable /path/to/my_sandbox.bt --sandbox_logfile my_log.log\n$ secimport run -h\n```\n\nFor more detailed usage instructions, see the [Command-Line Usage](https://github.com/avilum/secimport/wiki/Command-Line-Usage) page.\n\n## Python API\n\nYou can also use `secimport` by replacing `import` with `secimport.secure_import` for selected modules. See the [Python Imports](examples/python_imports/) example for more details.\n\n## Examples\n\nThe [Sandbox Examples](https://github.com/avilum/secimport/wiki/Sandbox-Examples) page contains basic and advanced real-world examples.\n\n## Contributing\n\nFor information on how to contribute to `secimport`, see the [Contributing](https://github.com/avilum/secimport/blob/master/docs/CONTRIBUTING.md) guide.\n\n## Roadmap\n\nSee the [Roadmap](https://github.com/avilum/secimport/blob/master/docs/ROADMAP.md) for the planned features and development milestones.\n\n## Changelog\n\nSee the [Changelog](https://github.com/avilum/secimport/blob/master/docs/CHANGELOG.md) for development progress and existing features.\n',
    'author': 'Avi Lumelsky',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avilum/secimport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
