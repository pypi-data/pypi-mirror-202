# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slice_finder',
 'slice_finder.data_connectors',
 'slice_finder.data_structures',
 'slice_finder.slice_finders']

package_data = \
{'': ['*']}

install_requires = \
['deap>=1.3,<2.0',
 'lightgbm>=3.0.0,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.5,<2.0.0']

setup_kwargs = {
    'name': 'slice-finder',
    'version': '0.0.22',
    'description': 'Slice Finder: A Framework for Slice Discovery',
    'long_description': '# Slice Finder: A Framework for Slice Discovery\n\nSlice Finder is a versatile and highly configurable framework designed for the discovery of explainable, anomalous data subsets, which exhibit substantially divergent metric values in comparison to the entire dataset.\n\n> To illustrate, imagine that you have developed a model for identifying fraudulent transactions. The model\'s overall accuracy across the entire dataset is 0.95. However, when transactions occur more than 100 km away from the previous transaction and involve cash (2 filters), the model\'s accuracy drops significantly to 0.54.\n\nSlice Finder is a crucial investigative instrument, as it enables data scientists to identify regions where their models demonstrate over- or under-performance.\n\n## Algorithmic achievements\n* Tackling data quantization can be complex, particularly when transforming continuous values into discrete space. Slice Finder overcomes this challenge by fitting an LGBM model to the data and extracting the appropriate splits.\n* As the number of filters, columns, and values increases, so does the combinatorial search space. Slice Finder addresses this issue in two ways:\n    * By fitting an LGBM model to the data, the most critical fields and values for splitting are identified, significantly reducing the search space.\n    * Incorporating Genetic Algorithm heuristics to converge towards global minima/maxima, which outperforms both the time-consuming "try-it-all" approach and uniform filter sampling in terms of efficiency and results.\n\n## Engineering achievements\nBy separating data connectors, data structures, and slice finders, SliceFinder offers a flexible framework that enables seamless modifications and replacement of components. Furthermore, by detaching metric mechanism from the system, SliceFinder supports any custom logic metrics.\n\n## Demo\n![GA search for anomalous subset with high MSE](./examples/demo.gif)\n\n## Installation\nInstall Slice Finder via pip:\n```python\npip install slice_finder\n```\n\n# Quick Start\n```python\nimport pandas as pd\nfrom sklearn import metrics\nfrom slice_finder import GAMuPlusLambdaSliceFinder, FlattenedLGBMDataStructure, PandasDataConnector\n\n# Load data\ndf = pd.read_csv(\'your_data.csv\')\n\n# Initialize Genetic Algorithm Slice Finder with desired data connector and data structure\nslice_finder = GAMuPlusLambdaSliceFinder(\n    data_connector=PandasDataConnector(\n        df=df,\n        X_cols=df.drop([\'pred\', \'target\'], axis=1).columns,\n        y_col=\'target\',\n        pred_col=\'pred\',\n    ),\n    data_structure=FlattenedLGBMDataStructure(),\n    verbose=True,\n    random_state=42,\n)\n\n# Find anomalous slice\nextreme = slice_finder.find_extreme(\n    metric=lambda df: metrics.mean_absolute_error(df[\'target\'], df[\'pred\']),\n    n_filters=3,\n    maximize=True,\n)\nextreme[0]\n```\n\n## Data Connectors\nBuilt in:\n* `PandasDataConnector` - allow you to use Pandas\n\nBase Classes:\n* `DataConnector` - Base data connector\n\nMore connectors will be added as demand grows.\n\nYou can create your custom data connector by extending the base class and implementing the necessary methods.\n\n## Data Structures\nBuilt in:\n* `FlattenedLGBMDataStructure` - Utilizes LightGBM decision trees to quantize and partition the data.\nNote: Currently, `FlattenedLGBMDataStructure` must work with `PandasDataConnector` because of LGBM constraints. Moreover, this data structure is coupled to pandas connector because categorical values must be modified to `pd.Categorical` class.\n\nBase classes:\n* `DataStructure` - Base data structure\n* `LGBMDataStructure` - Handles the fitting and partitioning the LGBM trees\n\nMore data structures will be added as demand grows.\n\nYou can create your custom data structure by extending the base classes and implementing the necessary methods.\n\n## Slice Finders\nBuilt in:\n* `GAMuPlusLambdaSliceFinder` - Utilizes `eaMuPlusLambda` evolutionary algorithm to search for the most anomalous slice\n* `UniformSliceFinder` - Utilizes uniform sampling out of the data structure\n\nBase classes:\n* `SliceFinder` - Base slice finder\n* `GASliceFinder` - Extends `SliceFinder` and enables the use of genetic algorithms as search heuristics\n\nMore algorithms will be added based on demand. \n\nYou can create your custom data structure by extending the base class and implementing the necessary methods.\n\n## Metrics\nMetrics are passed as functions to the `find_extreme` method, allowing you to use any metric or implement your custom logic.\n\n## Neat things to implement\n* Calculation parallelism\n* More search algorithms. Ant colony optimization?\n\n## License\nThis project is licensed under the MIT License.\n\n## Contributing\nContributions are welcome!\nClone the repo, run `poetry install` and start hacking.\n\n## Support\nFor any questions, bug reports, or feature requests, please open an issue.',
    'author': 'Igal Leikin',
    'author_email': 'igaloly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/igaloly/slice_finder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
