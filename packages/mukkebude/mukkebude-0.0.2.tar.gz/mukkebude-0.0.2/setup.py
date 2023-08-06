# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mukkeBude', 'mukkeBude.model']

package_data = \
{'': ['*'], 'mukkeBude': ['songs/*']}

install_requires = \
['keras-nlp==0.4.1',
 'matplotlib>=3.7.1,<4.0.0',
 'music21>=8.1.0,<9.0.0',
 'sacremoses==0.0.53',
 'tensorflow-text==2.10.0',
 'tensorflow>=2.10.0,<2.11.0']

setup_kwargs = {
    'name': 'mukkebude',
    'version': '0.0.2',
    'description': "A music generation library with transformer and lstm models',",
    'long_description': '# Komposition-eines-Musikstuecks-mittels-Neuronaler-Netze\nZiel der Studienarbeit ist die Komposition eines kleinen Musikstücks. Die Komposition erfolgt mittels eines Neuronalen Netzes.\n\n# Usage\nHier wird beschrieben wir man das Projekt verwendet.\n\n## Installation\nUm die unter [demos](./demos/) bereitgestellten jupyter-notebook verwenden zu können, muss das Projekt mittels pip installiert werden.\nHierfür gibt es folgende Möglichkeiten:\n\n**GitHub Repo**\n```bash\n# Clone das Repo\ngit clone git@github.com:DHBW-FN-TIT20/Komposition-eines-Musikstuecks-mittels-Neuronaler-Netze.git mukkeBude\ncd mukkeBude\n\n# Installieren mittels pip\npip install .\n```\n\n**PyPi**\n```bash\npip install mukkeBude\n```\n\nFür die Verwendung der **Jupyter-Notebooks** muss jupyter-lab zusätzlich installiert werden!\n```bash\npip install jupyterlab\n``` \n\n## Verwendung\nNach einer erfolgreichen installtion kann das modul mittels `import mukkeBude` verwendet werden. Entsprechende Beispiele sind unter [demos](./demos/) zu finden.\n\n# Developing\n\nHier wird beschrieben, wie man seine Entwicklungsumgebung entsprechend vorbereitet, um an dem Projekt zu entwicklen.\nEmpfohlen ist die Verwendung von **Conda**, da hier die Verwendung von der GPU deutlich einfach ist. Bei der Verwendung der anderen Methoden müssen \nunter Umständen weitere Schritte unternommen werden, um die GPU zu verwenden.\n\n## Conda\nInstallation mithilfe von conda:\n\n```bash\nconda env create -f environment.yml\nconda activate tf-gpu\n\n# Enable GPU support on Linux (need to be done in every new shell)\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/\n```\n\n## Pip\nOhne venv:\n\n```bash\npip install -r requirements-dev.txt\n```\n\nMit venv:\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\n\npip install -r requirements-dev.txt\n```\n\n## Poetry\n```bash\npoetry install --with=dev\npoetry shell\n```',
    'author': 'Florian Glaser',
    'author_email': 'Florian.Glaser@ifm.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DHBW-FN-TIT20/Komposition-eines-Musikstuecks-mittels-Neuronaler-Netze',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
