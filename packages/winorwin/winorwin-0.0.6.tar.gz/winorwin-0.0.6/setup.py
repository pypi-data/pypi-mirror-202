import pathlib
from setuptools import setup, find_packages

# The directory containing this file
dir = pathlib.Path(__file__).parent

# README file
README = (dir / "README.md").read_text()

# Dependencies
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='winorwin',
    version="0.0.06",
    packages=["rsxr"],
    author="Walid Ghariani",
    author_email="walid11ghariani@gmail.com",
    description=("winorwin: do stuff"),
    long_description=README,
    license="MIT",
    keywords="machine-learning, GIS, spatial",
    url="https://github.com/WalidGharianiEAGLE/winorwin",

    package_data={'rsxr': ['./lc_samples/*.geojson', './sentinel2_dataset/*.tif', 'trained_models/*.sav']},
    include_package_data=True,

    # Dependencies
    install_requires = requirements,
    python_requires='>=3.9',
 
    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    # testing
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
