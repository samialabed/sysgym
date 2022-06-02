# Contributing

## Development installation
To get the development installation with all the necessary dependencies for linting, testing, and building the documentation, run the following:
```bash
git clone git@github.com:samialabed/sysgym.git
cd sysgym
pip install -e .[dev]
```

## Development process

### Project.toml
We use `project.toml` to manage the build files and standardize the code style across all packages. You can read more on it [here](https://snarky.ca/what-the-heck-is-pyproject-toml/)

### Code style

We standardize the code style across the package using strict code style rules. 
To make it easier to use these tools we provide a file: `watchers.xml` which you can import into [pycharm](https://www.jetbrains.com/pycharm/) to ensure you are using them. 

#### 1. Black
We use `black` to ensure formatted python. 
You can integrate it in your PyCharm setup: [Instructions](https://black.readthedocs.io/en/stable/editor_integration.html)

#### 2. isort

#### 3. pylint and flake8 




