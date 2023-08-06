# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pt_datasets', 'pt_datasets.datasets']

package_data = \
{'': ['*']}

install_requires = \
['gdown>=4.7.1,<5.0.0',
 'imbalanced-learn>=0.10.1,<0.11.0',
 'nltk>=3.8.1,<4.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'opentsne>=0.7.1,<0.8.0',
 'pymagnitude-lite>=0.1.143,<0.2.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'spacy>=3.5.1,<4.0.0',
 'torch>=2.0.0,<3.0.0',
 'torchvision>=0.15.1,<0.16.0',
 'umap-learn>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'pt-datasets',
    'version': '0.19.19',
    'description': 'Library for loading PyTorch datasets and data loaders.',
    'long_description': '# PyTorch Datasets\n\n[![PyPI version](https://badge.fury.io/py/pt-datasets.svg)](https://badge.fury.io/py/pt-datasets)\n[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)\n[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-377/)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-382/)\n\n![](assets/term.png)\n\n## Overview\n\nThis repository is meant for easier and faster access to commonly used\nbenchmark datasets. Using this repository, one can load the datasets in a\nready-to-use fashion for PyTorch models. Additionally, this can be used to load\nthe low-dimensional features of the aforementioned datasets, encoded using PCA,\nt-SNE, or UMAP.\n\n## Datasets\n\n- MNIST\n- Fashion-MNIST\n- EMNIST-Balanced\n- CIFAR10\n- SVHN\n- MalImg\n- AG News\n- IMDB\n- Yelp\n- 20 Newsgroups\n- KMNIST\n- Wisconsin Diagnostic Breast Cancer\n- [COVID19 binary classification](https://github.com/lindawangg/COVID-Net)\n- [COVID19 multi-classification](https://github.com/lindawangg/COVID-Net)\n\n_Note on COVID19 datasets: Training models on this is not intended to produce\nmodels for direct clinical diagnosis. Please do not use the model output for\nself-diagnosis, and seek help from your local health authorities._\n\n## Usage\n\nIt is recommended to use a virtual environment to isolate the project dependencies.\n\n```shell script\n$ virtualenv env --python=python3  # we use python 3\n$ pip install pt-datasets  # install the package\n```\n\nWe use the [`tsnecuda`](https://github.com/CannyLab/tsne-cuda) library for the\nCUDA-accelerated t-SNE encoder, which can be installed by following the\n[instructions](https://github.com/CannyLab/tsne-cuda/wiki/Installation) in its wiki.\n\nBut there is also a provided script for installing `tsne-cuda` from source.\n\n```shell script\n$ bash setup/install_tsnecuda\n```\n\nDo note that this script has only been tested on an Ubuntu 20.04 LTS system\nwith Nvidia GTX960M GPU.\n\nWe can then use this package for loading ready-to-use data loaders,\n\n```python\nfrom pt_datasets import load_dataset, create_dataloader\n\n# load the training and test data\ntrain_data, test_data = load_dataset(name="cifar10")\n\n# create a data loader for the training data\ntrain_loader = create_dataloader(\n    dataset=train_data, batch_size=64, shuffle=True, num_workers=1\n)\n\n...\n\n# use the data loader for training\nmodel.fit(train_loader, epochs=10)\n```\n\nWe can also encode the dataset features to a lower-dimensional space,\n\n```python\nimport seaborn as sns\nimport matplotlib.pyplot as plt\nfrom pt_datasets import load_dataset, encode_features\n\n# load the training and test data\ntrain_data, test_data = load_dataset(name="fashion_mnist")\n\n# get the numpy array of the features\n# the encoders can only accept np.ndarray types\ntrain_features = train_data.data.numpy()\n\n# flatten the tensors\ntrain_features = train_features.reshape(\n    train_features.shape[0], -1\n)\n\n# get the labels\ntrain_labels = train_data.targets.numpy()\n\n# get the class names\nclasses = train_data.classes\n\n# encode training features using t-SNE\nencoded_train_features = encode_features(\n    features=train_features,\n    seed=1024,\n    encoder="tsne"\n)\n\n# use seaborn styling\nsns.set_style("darkgrid")\n\n# scatter plot each feature w.r.t class\nfor index in range(len(classes)):\n    plt.scatter(\n        encoded_train_features[train_labels == index, 0],\n        encoded_train_features[train_labels == index, 1],\n        label=classes[index],\n        edgecolors="black"\n    )\nplt.legend(loc="upper center", title="Fashion-MNIST classes", ncol=5)\nplt.show()\n```\n\n![](assets/tsne_fashion_mnist.png)\n\n## Citation\n\nWhen using the Malware Image classification dataset, kindly use the following\ncitations,\n\n- BibTex\n\n```\n@article{agarap2017towards,\n    title={Towards building an intelligent anti-malware system: a deep learning approach using support vector machine (SVM) for malware classification},\n    author={Agarap, Abien Fred},\n    journal={arXiv preprint arXiv:1801.00318},\n    year={2017}\n}\n```\n\n- MLA\n\n```\nAgarap, Abien Fred. "Towards building an intelligent anti-malware system: a\ndeep learning approach using support vector machine (svm) for malware\nclassification." arXiv preprint arXiv:1801.00318 (2017).\n```\n\nIf you use this library, kindly cite it as,\n\n```\n@misc{agarap2020pytorch,\n    author       = "Abien Fred Agarap",\n    title        = "{PyTorch} datasets",\n    howpublished = "\\url{https://gitlab.com/afagarap/pt-datasets}",\n    note         = "Accessed: 20xx-xx-xx"\n}\n```\n\n## License\n\n```\nPyTorch Datasets utility repository\nCopyright (C) 2020-2021  Abien Fred Agarap\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as published\nby the Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n```\n',
    'author': 'Abien Fred Agarap',
    'author_email': 'abienfred.agarap@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
