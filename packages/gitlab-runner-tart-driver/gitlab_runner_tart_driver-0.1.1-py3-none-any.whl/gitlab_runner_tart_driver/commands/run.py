import os
import sys

import click
from paramiko import MissingHostKeyPolicy
from paramiko import SSHClient

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart


@click.command()
@click.option(
    "--default-ssh-username", default="admin", required=False, type=str, help="username to login to a tart vm"
)
@click.option(
    "--default-ssh-password", default="admin", required=False, type=str, help="passowrd to login to a tart vm"
)
@click.option(
    "-x",
    "--tart-executable",
    required=False,
    default="tart",
    type=str,
    help="Path to the tart executable.",
)
@click.option(
    "--shell",
    required=False,
    default="/bin/zsh",
    type=str,
    help="Path to the shell to be used for commands over ssh.",
)
@click.argument("script")
@click.argument("stage")
def run(default_ssh_username, default_ssh_password, tart_executable, shell, script, stage):
    """Run commands."""
    p = GitLabCustomCommandConfig()

    if not p.tart_ssh_username:
        p.tart_ssh_username = default_ssh_username
    if not p.tart_ssh_password:
        p.tart_ssh_password = default_ssh_password

    ######################################################################
    # Connect to VM
    ######################################################################
    tart = Tart(exec_path=tart_executable)
    tart_vm_name = p.vm_name()
    tart_ip = tart.ip(tart_vm_name, timeout=30)
    click.echo(f"[INFO] Establishing SSH conntection to '{p.tart_ssh_username}@{tart_ip}'")

    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(MissingHostKeyPolicy())
    ssh_client.connect(tart_ip, username=p.tart_ssh_username, password=p.tart_ssh_password)

    click.echo("[INFO] Preparing workspace'")
    remote_build_dir = "/opt/build/"
    remote_script_dir = "/opt/temp"
    remote_cache_dir = "/opt/cache"
    exec_ssh_command(
        ssh_client,
        f"sudo mkdir -p {remote_build_dir} && sudo chown {p.tart_ssh_username}:{p.tart_ssh_username} {remote_build_dir}",
    )
    exec_ssh_command(
        ssh_client,
        f"sudo mkdir -p {remote_script_dir} && sudo chown {p.tart_ssh_username}:{p.tart_ssh_username} {remote_script_dir}",
    )
    exec_ssh_command(
        ssh_client,
        f"sudo mkdir -p {remote_cache_dir} && sudo chown {p.tart_ssh_username}:{p.tart_ssh_username} {remote_cache_dir}",
    )

    script_name = os.path.basename(script)
    remote_script_path = os.path.join(remote_script_dir, stage + "-" + script_name)

    sftp = ssh_client.open_sftp()
    sftp.put(script, remote_script_path)
    sftp.close()

    exec_ssh_command(ssh_client, f"cd {remote_build_dir}")
    script_exit_code = exec_ssh_command(ssh_client, f"{shell} -l {remote_script_path}", get_pty=True)

    sys.exit(script_exit_code)


def exec_ssh_command(ssh_client, command, get_pty=True):
    """Executes an ssh command and prints it's output continously to stdout/stderr"""
    _, stdout, stderr = ssh_client.exec_command(command, get_pty=get_pty)
    for line in iter(stdout.readline, ""):
        click.echo(line, nl=False)
    for line in iter(stderr.readline, ""):
        click.echo(line, nl=False, err=True)

    return stdout.channel.recv_exit_status()
