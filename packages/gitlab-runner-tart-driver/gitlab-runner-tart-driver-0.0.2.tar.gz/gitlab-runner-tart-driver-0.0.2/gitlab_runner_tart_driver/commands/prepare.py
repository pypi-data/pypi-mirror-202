import sys

import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart
from gitlab_runner_tart_driver.modules.utils import get_host_spec
from gitlab_runner_tart_driver.modules.utils import print_host_spec


@click.command()
@click.option(
    "--pull-policy",
    default="if-not-present",
    type=click.Choice(["always", "if-not-present", "never"]),
    help="define how runners pull tart images from registries",
)
@click.option("--oci-username", required=False, default=None, type=str, help="username to login to a oci registry")
@click.option("--oci-password", required=False, default=None, type=str, help="passowrd to login to a oci registry")
@click.option("--oci-host", required=False, default=None, type=str, help="username to login to a oci registry")
@click.option("--cpu", required=False, default=None, type=int, help="Number of CPUs associated to VM")
@click.option("--memory", required=False, default=None, type=int, help="VM memory size in megabytes associated to VM")
@click.option(
    "--display",
    required=False,
    default=None,
    type=str,
    help="VM display resolution in a format of <width>x<height>. For example, 1200x800",
)
@click.option(
    "--auto-resources/--no-auto-resources",
    required=False,
    default=True,
    is_flag=True,
    type=bool,
    help="If enabled, the driver will divide system resources equally to the concurrent VMs.",
)
@click.option(
    "--concurrency",
    required=False,
    default=1,
    type=int,
    help="Number of concurrent processes that are supported. ATTENTION tart currently only support two concurrent VMs",
)
@click.option("-x", "--tart-executable", required=False, default="tart", type=str, help="Path to the tart executable.")
def prepare(
    oci_username,
    oci_password,
    oci_host,
    cpu,
    memory,
    display,
    pull_policy,
    auto_resources,
    concurrency,
    tart_executable,
):
    """Prepare the environment and start the tart VM."""

    print_host_spec()

    p = GitLabCustomCommandConfig()

    tart = Tart(exec_path=tart_executable)
    tart_images = tart.list()
    tart_vm_map = {}
    for i in tart_images:
        tart_vm_map[i.name] = i

    # for k,v in os.environ.items():
    #     click.echo(f'{k}={v}')

    ######################################################################
    # OCI LOGIN
    ######################################################################
    if oci_username and oci_password and oci_host:
        click.echo(f"[INFO] Logging into OCI Registry '{oci_host}'")
        tart.login(username=oci_username, password=oci_password, host=oci_host)

    if p.tart_oci_username and p.tart_oci_password and p.tart_oci_host:
        click.echo(f"[INFO] Logging into OCI Registry '{p.tart_oci_host}'")
        tart.login(username=p.tart_oci_username, password=p.tart_oci_password, host=p.tart_oci_host)

    ######################################################################
    # PULL
    ######################################################################
    if (
        (pull_policy == "always")
        or (p.ci_job_image not in tart_vm_map and pull_policy != "never")
        or (p.ci_job_image not in tart_vm_map and pull_policy == "if-not-present")
    ):
        click.echo(f"[INFO] Pulling '{p.ci_job_image}' [pull_policy={pull_policy}]")
        tart.pull(p.ci_job_image)
    else:
        click.echo(f"[INFO] Skipping '{p.ci_job_image}' [pull_policy={pull_policy}]")

    ######################################################################
    # Create VM
    ######################################################################
    tart_vm_name = p.vm_name()
    if tart_vm_name in tart_vm_map:
        if tart_vm_map[tart_vm_name].running:
            click.echo(f"[INFO] Found running VM '{tart_vm_name}'. Going to stop it...")
            tart.stop(tart_vm_name)
        click.echo(f"[INFO] Found VM '{tart_vm_name}'. Going to delete it...")
        tart.delete(tart_vm_name)

    click.echo(f"[INFO] Cloning VM instance '{tart_vm_name}' from '{p.ci_job_image}'")
    tart.clone(p.ci_job_image, tart_vm_name)

    if cpu or memory or display:
        click.echo(f"[INFO] Configuring instance '{tart_vm_name}' from '{p.ci_job_image}'")
        click.echo(
            f"[INFO] {tart_vm_name} [cpu={cpu if cpu else 'default'}, memory={memory if memory else 'default'}, display={display if display else 'default'}]"
        )
        tart.set(tart_vm_name, cpu=cpu, memory=memory, display=display)
    elif auto_resources:
        click.echo("[INFO] Auto resource-disribution enabled.")
        host_spec = get_host_spec()
        tart.set(tart_vm_name, cpu=int(host_spec.cpu_count / concurrency), memory=int(host_spec.memory / concurrency))

    click.echo(f"[INFO] Starting VM instance '{tart_vm_name}'")

    tart.run(tart_vm_name)
    tart.ip(tart_vm_name, timeout=30)
    tart.print_spec(tart_vm_name)

    sys.exit(0)
