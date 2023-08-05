from setuptools import setup
from setuptools import find_packages

with open(file = "README.md", mode = "r", encoding = "utf-8") as file:
    long_description = file.read()

setup(
    name = "hds-stats",
    
    version = "0.1.0",
    
    author = "HelloDataScience",
    
    author_email = "hellodatasciencekorea@gmail.com",
    
    description = "Useful functions for Statistics and Machine Learning",
    
    long_description = long_description,
    
    long_description_content_type = "text/markdown",
    
    url = "https://github.com/HelloDataScience/hds-stats",
    
    license = "MIT",
    
    py_modules = ['hds_plot', 'hds_stat'],
    
    project_urls = {
        "Bug Tracker": "https://github.com/HelloDataScience/hds-stats/issues",
    },
    
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires = ">=3.6",
    
    packages = find_packages(),
    
    install_requires = ['numpy', 'pandas', 'scipy', 'seaborn', 'matplotlib', 'statsmodels', 'scikit-learn'],
    
    # package_dir = {"": "src"},
)