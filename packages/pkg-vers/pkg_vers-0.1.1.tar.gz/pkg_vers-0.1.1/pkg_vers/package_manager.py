import importlib
import re
import subprocess
import sys
import nbformat
from pkg_vers.utils import _run_subprocess
from pkg_vers.utils import get_files
from stdlib_list import stdlib_list

def _get_excluded_module_names():
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    standard_modules = stdlib_list(python_version)
    return sorted(standard_modules)

IGNORED_LIB_MODULES = _get_excluded_module_names() 
PACKAGE_NAME_EXCEPTIONS = {'pillow': 'PIL', 'scikit-learn' : 'sklearn'}

import_pattern_string = r'^\s*import\s+(\S+)'
from_import_pattern_string = r'^\s*from\s+(\S+)\s+import'

def get_pkg_vers(paths):
    if isinstance(paths, str):
        paths = [paths]
    
    """Get package versions from given files or directories."""
    all_files = get_files(paths)

    installed_packages = _get_installed_packages()
    imported_packages = set()

    for file in all_files:
        if file.endswith('.py'):
            imported_packages.update(_get_imported_top_level_packages([file]))
        elif file.endswith('.ipynb'):
            imported_packages.update(_get_imported_top_level_packages_from_ipynb(file))

    packages_with_versions = _get_package_versions(imported_packages, installed_packages)
    return packages_with_versions

def install_packages(packages):
    if isinstance(packages, dict):
        package_list = [f"{pkg}=={ver}" if ver else pkg for pkg, ver in packages.items()]
    elif isinstance(packages, (list, tuple)):
        package_list = packages
    else:
        raise TypeError("packages must be a dictionary, list, or tuple")

    package_format = re.compile(r'^[a-zA-Z0-9_-]+(==\d+(\.\d+)*)?$')
    
    inv_map = {v: k for k, v in PACKAGE_NAME_EXCEPTIONS.items()}

    for pkg in package_list:
        if '==' in pkg:
            pkg_name, version = pkg.split('==')
        else:
            pkg_name, version = pkg, ''

        updated_pkg = inv_map[pkg_name] if pkg_name in inv_map.keys() else pkg_name 

        pkg = updated_pkg if version == '' else f"{updated_pkg}=={version}"
        if not isinstance(pkg, str):
            raise TypeError(f"Each package must be a string, not {type(pkg)}")
        
        if not package_format.match(pkg):
            raise ValueError(f"Invalid package format: {pkg}. Expected format: 'package' or 'package==version'")
        
        try:
            print(f"Attempting to install {pkg} with Mamba...")
            subprocess.run(["mamba", "install", "-y", pkg], check=True)
        except subprocess.CalledProcessError:
            print(f"Mamba installation failed for {pkg_name}. Attempting pip install...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)
            except subprocess.CalledProcessError:
                raise ValueError(f"Failed to install {pkg} with both Mamba and pip.")
        print(f"Successfully installed {pkg_name}")

def _get_imported_top_level_packages_from_ipynb(path):
    try:
        # Read the notebook file
        with open(path, 'r') as file:
            notebook = nbformat.read(file, as_version=4)

        # Regular expression patterns to match import statements
        import_pattern = re.compile(import_pattern_string)
        from_import_pattern = re.compile(from_import_pattern_string)

        # Initialize a set to hold unique imports
        imports = set()

        # Iterate over each cell in the notebook
        for cell in notebook.cells:
            # Check if the cell is a code cell
            if cell.cell_type == 'code':
                # Get the cell's source code
                source = cell.source

                # Split the source code into lines
                lines = source.split('\n')

                # Iterate over each line and look for import statements
                for line in lines:
                    import_match = import_pattern.match(line)
                    from_import_match = from_import_pattern.match(line)
                    if import_match:
                        import_name = import_match.group(1).split('.')[0]
                        if import_name:
                            imports.add(import_name)
                        
                    elif from_import_match:
                        import_name = from_import_match.group(1).split('.')[0]
                        if import_name:
                            imports.add(import_name)

        return imports
    except Exception as e:
        print(f"Error reading notebook {path}: {e}")
        return set()

def _get_imported_top_level_packages(files):
    imported_packages = set()
    import_pattern = re.compile(import_pattern_string)
    from_import_pattern = re.compile(from_import_pattern_string)

    for file in files:
        with open(file, 'r') as f:
            for line in f:
                import_match = import_pattern.match(line)
                from_import_match = from_import_pattern.match(line)
                if import_match:
                    imported_packages.add(import_match.group(1).split('.')[0])
                elif from_import_match:
                    imported_packages.add(from_import_match.group(1).split('.')[0])

    return imported_packages

import json

def _get_mamba_installed_packages():
    packages = {}
    try:
        # Run 'mamba list' and capture its JSON output
        result = subprocess.run(["mamba", "list", "--json"], capture_output=True, text=True, check=True)
        mamba_packages = json.loads(result.stdout)
        
        for package_info in mamba_packages:
            package = package_info['name']
            version = package_info['version']
            packages[_package_version_key(package)] = version
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error getting Mamba packages: {e}")
    
    return packages

def _get_pip_installed_packages():
    packages = {}
    
    # Get packages installed with pip
    freeze_lines = _run_subprocess([sys.executable, '-m', 'pip', 'freeze'])
    for line in freeze_lines:
        parts = line.split('==')
        if len(parts) == 2:
            package, version = parts
            packages[_package_version_key(package)] = version

    pip_lines = _run_subprocess([sys.executable, '-m', 'pip', 'list'])
    for line in pip_lines:
        parts = re.split(r'\s+', line)
        if len(parts) >= 2:
            package, version = parts[0], parts[1]
            packages[_package_version_key(package)] = version

    return packages

def _get_installed_packages():
    packages = {}
    
    # Get packages installed with Mamba
    mamba_packages = _get_mamba_installed_packages()
    packages.update(mamba_packages)

    # Get packages installed with pip
    pip_packages = _get_pip_installed_packages()
    packages.update(pip_packages)

    return packages

def _get_package_version(package):
    try:
        module = importlib.import_module(package)
        return getattr(module, '__version__', '')
    except ImportError:
        return ''
    
def _package_version_key(package):
    return PACKAGE_NAME_EXCEPTIONS[package] if package in PACKAGE_NAME_EXCEPTIONS.keys() else package

def _get_package_versions(imported_packages, installed_packages):
    specific_versions = {}
    for package in imported_packages:
        if package in IGNORED_LIB_MODULES:
            continue
        version = installed_packages.get(package) or installed_packages.get(package.replace("_", "-"), "")

        if not version:  # if version is empty, try to get it from module.__version__
            version = _get_package_version(package)

        specific_versions[package] = version
    return specific_versions
