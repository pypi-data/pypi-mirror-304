from setuptools import setup, find_packages

readme = open('README.md').read()


setup(
    name='fancy-title',
    version='0.0.1',
    description='Evaluation metrics for your title.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Shaobo Cui',
    author_email='shaobo.cui@epfl.ch',
    url='https://github.com/cui-shaobo/fancy-title',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'transformers',
        'tqdm',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
