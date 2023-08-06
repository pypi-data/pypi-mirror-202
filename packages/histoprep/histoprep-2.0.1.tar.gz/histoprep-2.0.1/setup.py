# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['histoprep', 'histoprep.functional', 'histoprep.utils']

package_data = \
{'': ['*']}

install_requires = \
['aicspylibczi>=3,<4',
 'matplotlib',
 'mpire>=2.6,<3.0',
 'numpy',
 'opencv-python-headless>=4,<5',
 'openslide-python>=1.2,<2.0',
 'pillow>=9,<10',
 'polars>=0.16,<0.17',
 'rich-click>=1.6,<2.0',
 'scikit-learn>=1,<2',
 'tqdm']

entry_points = \
{'console_scripts': ['HistoPrep = histoprep._cli:cut_slides']}

setup_kwargs = {
    'name': 'histoprep',
    'version': '2.0.1',
    'description': 'Read and process histological slide images with python!',
    'long_description': '<div align="center">\n\n# HistoPrep\nPreprocessing large medical images for machine learning made easy!\n\n<p align="center">\n  <a href="#description">Description</a> •\n  <a href="#installation">Installation</a> •\n  <a href="#usage">Usage</a> •\n  <a href="https://jopo666.github.io/HistoPrep/">API Documentation</a> •\n  <a href="#citation">Citation</a>\n</p>\n\n</div>\n\n## Description\n\n`HistoPrep` makes is easy to prepare your histological slide images for deep\nlearning models. You can easily cut large slide images into smaller tiles and then\npreprocess those tiles (remove tiles with shitty tissue, finger  marks etc).\n\n## Installation \n\nInstall [`OpenSlide`](https://openslide.org/download/) on your system and then install histoprep with `pip`!\n\n```bash\npip install histoprep\n```\n\n## Usage\n\nTypical workflow for training deep learning models with histological images is the\nfollowing:\n\n1. Cut each slide image into smaller tile images.\n2. Preprocess smaller tile images by removing tiles with bad tissue, staining artifacts.\n3. Overfit a pretrained ResNet50 model, report 100% validation accuracy and publish it\n   in [Nature](https://www.nature.com) like everyone else. \n\nWith `HistoPrep`, steps 1. and 2. are as easy as accidentally drinking too much at the\nresearch group christmas party and proceeding to work remotely until June.\n\nLet\'s start by cutting a slide from the\n[PANDA](https://www.kaggle.com/c/prostate-cancer-grade-assessment) kaggle challenge into\nsmall tiles. \n\n```python\nfrom histoprep import SlideReader\n\n# Read slide image.\nreader = SlideReader("./slides/slide_with_ink.jpeg")\n# Detect tissue.\nthreshold, tissue_mask = reader.get_tissue_mask(level=-1)\n# Extract overlapping tile coordinates with less than 50% background.\ntile_coordinates = reader.get_tile_coordinates(\n    tissue_mask, width=512, overlap=0.5, max_background=0.5\n)\n# Save tile images with image metrics for preprocessing.\ntile_metadata = reader.save_regions(\n    "./train_tiles/", tile_coordinates, threshold=threshold, save_metrics=True\n)\n```\n```\nslide_with_ink: 100%|██████████| 390/390 [00:01<00:00, 295.90it/s]\n```\n\nLet\'s take a look at the output and visualise the thumbnails.\n\n```bash\njopo666@~$ tree train_tiles\ntrain_tiles\n└── slide_with_ink\n    ├── metadata.parquet       # tile metadata\n    ├── properties.json        # tile properties\n    ├── thumbnail.jpeg         # thumbnail image\n    ├── thumbnail_tiles.jpeg   # thumbnail with tiles\n    ├── thumbnail_tissue.jpeg  # thumbnail of the tissue mask\n    └── tiles [390 entries exceeds filelimit, not opening dir]\n```\n\n![Prostate biopsy sample](images/thumbnail.jpeg)\n![Tissue mask](images/thumbnail_tissue.jpeg)\n![Thumbnail with tiles](images/thumbnail_tiles.jpeg)\n\nThat was easy, but it can be annoying to whip up a new python script every time you want\nto cut slides, and thus it is recommended to use the `HistoPrep` CLI program!\n\n```bash\n# Repeat the above code for all images in the PANDA dataset!\njopo666@~$ HistoPrep --input \'./train_images/*.tiff\' --output ./tiles --width 512 --overlap 0.5 --max-background 0.5\n```\n\nAs we can see from the above images, histological slide images often contain areas that\nwe would not like to include into our training data. Might seem like a daunting task but\nlet\'s try it out!\n\n\n```python\nfrom histoprep.utils import OutlierDetector\n\n# Let\'s wrap the tile metadata with a helper class.\ndetector = OutlierDetector(tile_metadata)\n# Cluster tiles based on image metrics.\nclusters = detector.cluster_kmeans(num_clusters=4, random_state=666)\n# Visualise first cluster.\nreader.get_annotated_thumbnail(\n    image=reader.read_level(-1), coordinates=detector.coordinates[clusters == 0]\n)\n```\n![Tiles in cluster 0](images/thumbnail_blue.jpeg)\n\nI said it was gonna be easy! Now we can mark tiles in cluster `0` as outliers and\nstart overfitting our neural network! This was a simple example but the same code can be\nused to cluster all several _million_ tiles extracted from the `PANDA` dataset and discard\noutliers simultaneously!\n\n## Citation\n\nIf you use `HistoPrep` to process the images for your publication, please cite the github repository.\n\n```\n@misc{histoprep,\n  author = {Pohjonen, Joona and Ariotta, Valeria},\n  title = {HistoPrep: Preprocessing large medical images for machine learning made easy!},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {https://github.com/jopo666/HistoPrep},\n}\n```\n',
    'author': 'jopo666',
    'author_email': 'jopo@birdlover.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
