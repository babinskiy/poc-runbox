from .celery import app

from git import Repo
from urllib.parse import quote
from pathlib import Path
import json

import ansible_runner

repos_dir = '/data'

@app.task
def add(x, y):
    return x + y

@app.task
def repo_clone(repo_name, repo_url):
    repo_path = Path(repos_dir, repo_name)
    if repo_path.exists():
        if repo_path.is_dir():
            repo_path.rmdir()
        else:
            repo_path.unlink()

    repo = Repo.clone_from(
        url = repo_url,
        to_path = repo_path
    )
    return {"status": 'OK'}

@app.task
def repo_checkout(repo_name, version):
    repo_path = Path(repos_dir, repo_name)
    repo = Repo(repo_path)
    log = []
    log.append(repo.git.fetch())
    log.append(repo.git.checkout(version))
    log.append(repo.git.pull())
    return json.dumps({"status":'OK', "log": log})

@app.task
def run_ansible_module(home, host='localhost', module='setup', module_args=None):
    work_dir = Path(repos_dir, home)
    private_dir = Path(repos_dir, 'tmp', home)
    r = ansible_runner.run(
            private_data_dir=private_dir,
            host_pattern=host,
            module = module,
            module_args = module_args
        )

    return {"state": r.status, "rc": r.rc, "stats": r.stats, "stdout": r.stdout.read(), "stderr": r.stderr.read()}


@app.task
def run_ansible_playbook(home, playbook, inventory, extravars=None, ssh_key=None, passwords=None):
    work_dir = Path(repos_dir, home, 'ansible')
    private_dir = Path(repos_dir, 'tmp', home)
    private_dir.mkdir(parents=True, exist_ok=True)
    r = ansible_runner.run(
            private_data_dir=str(private_dir),
            project_dir = str(work_dir),
            playbook=playbook,
            inventory=inventory,
            roles_path='./roles/',
            extravars = extravars,
            ssh_key = ssh_key,
            passwords = passwords
            )

    return {"some": dir(r), "state": r.status, "rc": r.rc, "stats": r.stats, "stdout": r.stdout.read(), "stderr": r.stderr.read()}
