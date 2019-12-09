import re
import os
import glob
import subprocess
from colorama import init, Fore, Back, Style
init()

# import semver

# p = re.compile(r'(?<=release\/v)(.+)')
# m = p.search("release/v1.0.9")

# if m:
#     version = m.group()

#     print(f'str {version}')

#     ver = semver.parse(version)

#     print(version)

str = "pos-mamba-3rdparty-siclos-theos"
str2 = "pos-mamba-3rdparty-siclos-sistem-glass"
repos = ["pos-mamba-3rdparty-siclos-theos", "pos-mamba-3rdparty-siclos-sistem-glass",
         "pos-mamba-3rdparty-siclos-saude", "pos-mamba-3rdparty-siclos-pacto", "pos-mamba-3rdparty-siclos-livance"]


def is_empty(any_structure):
    if any_structure:
        print('Structure is not empty.')
        return False
    else:
        print('Structure is empty.')
        return True


def detectAppFolder():
    result = []

    for path in repos:
        p = re.compile(r'(?<=3rdparty-siclos\-)[a-zA-Z_0-9_-]*')
        m = p.search(path)

        repo_title = m.group()
        reg_compile = re.compile(repo_title)
        full_path = f'./temp/{path}'
        # test_paths = (
        #    repo_title, f'{"|".join(repo_title.split("-"))}|{repo_title}')[repo_title.find('-') != -1]
        test_paths = repo_title.split("-")
        for dirpath, dirnames, filenames in os.walk(full_path):
            for test in dirnames:
                if test in test_paths:
                    result = result + [f'{dirpath}/{test}']

                    break
    return result


apps = detectAppFolder()


print(Fore.WHITE + Back.BLACK + 'Building Apps...')
print(Style.RESET_ALL)

for app in apps:
    cd = subprocess.getstatusoutput(
        'cd ${pwd}./temp/pos-mamba-3rdparty-siclos-sistem-glass/glass && npm i && npm run build')
    if cd:
        print(cd[1])
        print(Fore.WHITE + Back.BLACK + f'.PPK of {app} as completed.')
    else:
        print(Back.GREEN + 'and with a green background')

# npm = subprocess.check_call('npm --help', shell=True)
#  & cd[1].split('\n')
