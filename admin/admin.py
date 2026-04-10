import argparse
import json
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).parent
src: str = 'src'
__init__py: str = '__init__.py'
__main__py: str = '__main__.py'
requirements_txt: str = 'requirements.txt'
build: str = 'build'
build_json: str = 'build.json'
dockerignore: str = '.dockerignore'

def main():
    parser = argparse.ArgumentParser(description="Project manager CLI")
    parser.add_argument("command", nargs=1, type=str, help="Command name")
    parser.add_argument("service", nargs=1, type=str, help="Service name")
    args = parser.parse_args()

    if args.command[0] == 'build':
        build_service(args.service[0])

def build_service(service: str):
    service_dir = BASE_DIR/service
    build_file = service_dir/build_json
    build_dir = service_dir/build

    requirements: str = f"### {service} ###\n"

    # clear
    if build_dir.exists():
        for item in build_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            else:
                shutil.rmtree(item)

    # copy service
    shutil.copytree(service_dir/src, build_dir/service/src, dirs_exist_ok=True)
    shutil.copyfile(service_dir/__init__py, build_dir/service/__init__py)
    shutil.copyfile(service_dir/__main__py, build_dir/service/__main__py)

    # read reqs
    with open(service_dir/requirements_txt, 'r', encoding='utf-8') as file:
        requirements += file.read()

    # copy modules
    with open(build_file, 'r', encoding='utf-8') as file:
        content = file.read()
    reqs: dict[str, list[str]] = json.loads(content)

    for package, modules in reqs.items():
        package_dir = BASE_DIR / package
        (build_dir/package).mkdir()
        shutil.copyfile(package_dir/__init__py, build_dir/package/__init__py)
        for module in modules:
            with open(package_dir/module/requirements_txt, 'r', encoding='utf-8') as file:
                requirements += f'\n### {module} ###\n' + file.read()
            shutil.copytree(package_dir/module, build_dir/package/module, dirs_exist_ok=True)

    with open(build_dir/requirements_txt, 'w', encoding='utf-8') as file:
        file.write(requirements)

if __name__ == '__main__':
    print('run')
