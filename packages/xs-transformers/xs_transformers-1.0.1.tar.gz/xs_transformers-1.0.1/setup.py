from setuptools import setup, find_packages

setup(name='xs_transformers',
version='1.0.1',
description='xs transformers from transformers',
python_requires='>=3',
package_dir={"": "xs_transformers"},
packages=find_packages(where="xs_transformers")
)
