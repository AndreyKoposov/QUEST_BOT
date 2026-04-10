import argparse
import json
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).parent

def main():
    parser = argparse.ArgumentParser(description="Project manager CLI")
    parser.add_argument("command", nargs=1, type=str, help="Command name")
    parser.add_argument("service", nargs=1, type=str, help="Service name")
    args = parser.parse_args()

    if args.command[0] == 'build':
        build(args.service[0])

def build(service: str):
    service_dir = BASE_DIR / service
    build_file = service_dir / 'build.json'
    build_dir = service_dir / 'build'

    for item in build_dir.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        else:
            shutil.rmtree(item)
    return
    shutil.rmtree('d')
    shutil.copytree(service_dir/'src', build_dir/'src', dirs_exist_ok=True)
    shutil.copyfile(service_dir/'__init__.py', build_dir/'__init__.py')
    shutil.copyfile(service_dir/'__main__.py', build_dir/'__main__.py')
    shutil.copyfile(service_dir/'requirements.txt', build_dir/'requirements.txt')

    with open(build_file, 'r', encoding='utf-8') as file:
        content = file.read()
    content = json.loads(content)


if __name__ == '__main__':
    main()
