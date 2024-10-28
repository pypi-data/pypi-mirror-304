
# pkg_vers

`pkg_vers` is a utility that helps you determine the versions of packages imported in your Python scripts or Jupyter notebooks.

- Use the `get_versions(files)` function to get the versions of all top-level packages imported in a list of Python scripts (.py) and Jupyter notebooks (.ipynb).
- Use the `install_packages(files)` function to install all top-level packages imported in the specified Python scripts or Jupyter notebooks.
- Use the CLI to quickly get package versions and install packages from the command line.

## Features

- Extract top-level imported packages from Python scripts and Jupyter notebooks.
- Retrieve installed package versions using `pip` and `mamba`.
- Install imported packages.
- Provide a mapping of imported packages to their installed versions.
- Command Line Interface (CLI) for quick access to package version information and package installation.

## Installation

Make sure you have `pkg_vers` installed. If not, you can install it using pip:

```sh
pip install pkg_vers
```

## Usage

### Get Package Versions

To get the versions of all top-level packages imported in your Python scripts and Jupyter notebooks, use the `get_versions(files)` function.

**Example:**

```python
from pkg_vers import get_versions

files = ['script1.py', 'notebook.ipynb']
package_versions = get_versions(files)
print(package_versions)
```

### Get Package Versions from a Folder
To get the versions of all top-level packages imported in all `.py` and `.ipynb` files within a folder, use the `get_versions(folder)` function.

**Example:**

```python
from pkg_vers import get_versions

folder_path = 'path/to/your/folder'
package_versions = get_versions(folder_path)
print(package_versions)
```

### Install Packages

To install all top-level packages imported in your Python scripts and Jupyter notebooks, use the `install_packages(files)` function.

**Example:**

```python
from pkg_vers import install_packages

files = ['script1.py', 'notebook.ipynb']
install_packages(files)
```

### Install Packages from a Folder

To install all top-level packages imported in all `.py` and `.ipynb` files within a folder, use the `install_packages(folder)` function.

**Example:**

```python
from pkg_vers import install_packages

folder_path = 'path/to/your/folder'
install_packages(folder_path)
```

## Command Line Interface (CLI)

You can use `pkg_vers` directly from the command line to get the versions of packages imported in your scripts, notebooks, or all files within a folder.

### Get Package Versions

To use the CLI, simply run:

```sh
python -m pkg_vers get_versions <file1> <file2> ...
```

Replace `<file1>`, `<file2>`, etc., with the paths to your Python scripts or Jupyter notebooks.

**Example:**

```sh
python -m pkg_vers get_versions script1.py notebook.ipynb
```

### Get Package Versions from a folder

To process all `.py` and `.ipynb` files within a folder, run:

```sh
python -m pkg_vers get_versions path/to/your/folder
```

This will output the versions of all top-level packages imported in the specified files or all files within the specified folder.

### Install Packages

To use the CLI to install packages, run:

```sh
python -m pkg_vers install_packages <file1> <file2> ...
```

Replace `<file1>`, `<file2>`, etc., with the paths to your Python scripts or Jupyter notebooks.

**Example:**

```sh
python -m pkg_vers install_packages script1.py notebook.ipynb
```

### Install Packages from a Folder

To use the CLI to install packages, run:

```sh
python -m pkg_vers pkg_vers install_packages path/to/your/folder
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.