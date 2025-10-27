<h1 align="center">
  <img src="https://raw.githubusercontent.com/Yrrrrrf/some-asm/main/resources/img/static/img/chart.png" alt="Some Assembly" width="128">
  <div align="center">Some Assembly</div>
</h1>

<div align="center">

[![GitHub: Repo](https://img.shields.io/badge/some--asm-58A6FF?&logo=github)](https://github.com/Yrrrrrf/some-asm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

</div>

> A Python library for zero-configuration, OS-independent asset management.

`some-asm` is a Python library designed to automatically discover and provide an intuitive API to access project files, eliminating the need for hardcoded relative paths.

> **Note:** This library is part of the Prism ecosystem, designed to create a seamless bridge between your database and client applications.

## 🚦 Getting Started

### Installation
The preferred installation method is:
```bash
# Using uv as package manager
uv sync
```

#### Quick Start
Here's a minimal example to get you started:
```bash
# Using uv to run the main script
uv run src/main.py
```

## Considerations
- The project is currently in development, which means that some features might not be fully functional yet.
- The python files marked with `example_*.py` are from previous iterations of the tool. They are not currently active but remain available for reference or potential future integration.

## Setup
The current python version is `3.11.*`. It is recommended to use the same version to avoid any issues.

This project uses `uv` to manage the python environment.

- Create and activate the virtual environment
```bash
# Using uv as package manager
uv sync  # create the environment and install dependencies
```

- Run the project from the root directory
```bash
# Using uv to run the main script
uv run src/main.py  # run the main file
```

![sample](./resources/img/sample.png)

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

But it also uses [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) which have their own license.
- [PyQt6 License](https://www.riverbankcomputing.com/static/Docs/PyQt6/introduction.html#license) (GPLv3 License)

## Attributions
This project uses some icons from [flaticon.com](https://www.flaticon.com/). The individual attributions are in the [attributions.md](./resources/img/static/attributions.md) file.