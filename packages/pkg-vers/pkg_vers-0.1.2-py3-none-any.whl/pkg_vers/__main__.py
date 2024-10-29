import argparse
from pkg_vers.package_manager import get_pkg_vers, install_packages

def get_versions(paths):
    packages = get_pkg_vers(paths)
    for name, version in packages.items():
        print(f"{name}: {version}")

def main():
    parser = argparse.ArgumentParser(description='Package Version Manager CLI')
    subparsers = parser.add_subparsers(dest='command')

    get_versions_parser = subparsers.add_parser('get_versions', help='Get installed package versions')
    get_versions_parser.add_argument('paths', nargs='*', help='File paths, list of file paths, or folder path')

    install_packages_parser = subparsers.add_parser('install_packages', help='Install packages with Mamba, falling back to pip if necessary')
    install_packages_parser.add_argument('packages', nargs='+', help='List of packages to install (e.g., matplotlib==3.8.4 fastai==2.7.14)')

    args = parser.parse_args()

    if args.command == 'get_versions':
        get_versions(args.paths)
    elif args.command == 'install_packages':
        install_packages(args.packages)

if __name__ == "__main__":
    main()
