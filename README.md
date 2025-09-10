<h1 align="center">
    <img src=".\resources\img\static\production.png" alt="Project Assembly" width="128">
    <div align="center">Some Assembly</div>
</h1>

Simplify your project management with "Some Assembly", a user-friendly tool designed to assist in the efficient assembly and management of various projects. Ensure **organized and trackable project progress** with built-in documentation tools for an enhanced project oversight.

## Considerations
- The project is currently in development, which means that some features might not be fully functional yet.
- The python files marked with `example_*.py` are from previous iterations of the tool. They are not currently active but remain available for reference or potential future integration.

## Setup
The current python version is `3.11.*`. It is recommended to use the same version to avoid any issues.  

The project is still on development, so the **setup is not automated yet**.

- Create and activate the virtual environment
```bash
# Using venv std module as package manager
python -m venv .venv  # create the environment
source .venv/bin/activate  # activate on linux
.venv\Scripts\activate  # activate on windows
pip install -r requirements.txt # install dependencies

# Using conda (or mamba) as package manager
conda env create -f environment.yml  # create the environment
conda activate cv  # activate the environment
```

- Run the project from the root directory
```bash
python src/main.py  # run the main file
```

## Test the project
To be sure that everything is working as expected, run the tests.
```bash
python -m unittest discover -s src/tests -p test_*.py  # run all tests in src/tests
```

![sample](./resources/img/sample.png)

## [License](./LICENSE)

This project is licensed under the [MIT License](./LICENSE).

But it also uses [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) and [OpenCV](https://opencv.org/) which have their own licenses.
- [PyQt6 License](https://www.riverbankcomputing.com/static/Docs/PyQt6/introduction.html#license) (GPLv3 License)

## Attributions
This project uses some icons from [flaticon.com](https://www.flaticon.com/). The individual attributions are in the [attributions.md](./resources/img/static/attributions.md) file.
