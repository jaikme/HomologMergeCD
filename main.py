import os
import gitlab
import re
from git import Repo
import shutil
import unicodedata
import json
# from multiprocessing import Process
import time
import threading
# import semver


# define the name of the directory to be created
path = "./tmp"
gl = gitlab.Gitlab.from_config('posgitlab', ['.gitlab.cfg'])

# try:
#     os.mkdir(path)
# except OSError:
#     print("Creation of the directory %s failed" % path)
# else:
#     print("Successfully created the directory %s " % path)

# if __name__ == '__main__':
#     group = gl.groups.get('stone-payments')
#     for mr in group.mergerequests.list():
#         print(mr.web_url.search("3rdparty.+?\/"))

# state = "opened"
# merge_status = "can_be_merged"
# target_branch = "homolog"
# source_branch = "release/v1.0.9"
# web_url = "http://posgitlab.stone.com.br/stone-payments/pos-mamba-3rdparty-sistem-glass/merge_requests/1"
# # p = re.compile(r'(?<=3rdparty\-)[a-zA-Z_0-9_-]*')
# p = re.compile(r'pos-mamba-3rdparty\-[a-zA-Z_0-9_-]*')
# m = p.search(web_url)
# # print(m.group(0).replace("/", ""))
# print(m)
# print(m.group())
# repo_title = m.group()
# clone_url = f'https://posgitlab.stone.com.br/stone-payments/{repo_title}.git'
# print(clone_url)


# # project = gl.projects.get(86)
# # print(project.http_url_to_repo)
# # print(project)

# project_path = f'./temp/{repo_title}'

# if os.path.isdir(project_path):
#     shutil.rmtree(project_path)

# repo = Repo.clone_from(
#     clone_url,
#     project_path,
#     branch=source_branch
# )

temp = "./temp"
lock = f"{temp}/homolog.lock.json"
mrs = None
paths = []

# TODO Dont work with multiple Merge Requests


def cloneRepoOf(url, name, source_branch):
    # p = re.compile(r'pos-mamba-3rdparty\-[a-zA-Z_0-9_-]*')
    # m = p.search(web_url)
    # repo_title = m.group()
    # clone_url = f'https://posgitlab.stone.com.br/stone-payments/{repo_title}.git'
    project_path = f'./temp/{name}'
    if os.path.isdir(project_path):
        shutil.rmtree(project_path)
    print(f"Clone URL -> {url}")
    print(f"Project Path -> {project_path}")
    print(f"Source branch -> {source_branch}\n")
    if not source_branch == "develop":
        global paths
        paths.append(project_path)
        Repo.clone_from(url, project_path, branch=source_branch)


def total(arr):
    length = len(arr)
    return length


def runPreCheck():
    if not os.path.isdir(temp):
        shutil.rmtree(temp)
        os.mkdir(temp)

# TODO Dont work with multiple Merge Requests


def get_merge_requests():
    runPreCheck()
    # if os.path.isfile(lock):
    #     with open(lock) as json_file:
    #         mrs = json.load(json_file)
    #         length = total(mrs)
    #         print(f"Total project to homolog: {length}")
    #         for mr in mrs:
    #             createThread(mr).start()
    # else:
    # print("No lock file found. Refreshing Merge Requests ...")
    group = gl.groups.get('stone-payments')
    global mrs
    mrs = []
    for mr in group.mergerequests.list(state='opened', order_by='updated_at'):
        if mr.merge_status == 'can_be_merged':
            p = re.compile(r'(?<=release\/v)(.+)')
            m = p.search(mr.source_branch)
            if m:
                mrs.append(mr.__dict__['_attrs'])


def createThread(mr):
    project = gl.projects.get(mr['project_id'])
    url = project.http_url_to_repo.replace("http", "https")
    return threading.Thread(target=cloneRepoOf,
                            args=(url, project.name, mr['source_branch'],))


def main(cb=None):
    thread = threading.Thread(target=get_merge_requests)
    thread.start()

    # wait here for the result to be available before continuing
    thread.join()
    length = total(mrs)
    print(f"Total project to homolog: {length}")

    threads = []

    for mr in mrs:
        threads.append(createThread(mr))

    for x in threads:
        x.start()

    for x in threads:
        x.join()

    if cb:
        cb()

    with open(lock, 'w') as outfile:
        json.dump(mrs, outfile, indent=3)


def processPaths():
    print(paths)


if __name__ == '__main__':
    main(processPaths)
