import getpass
import os
import subprocess
import sys

import click
import dotenv

# def install(package, extra_url = ''):
#     if extra_url == '':
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#     else:
#         #--extra-index-url https://shared:HF6w0RbukY@packages.allegro.ai/repository/allegroai/simple allegroai
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "--extra-index-url", package])


def install_allegro(pipcommand: str):
    if pipcommand.startswith("pip install"):
        subprocess.call(pipcommand.split(" "))
    else:
        raise ValueError(
            "you need to specify your clearml pip install command from the clearml interface"
        )


def run_allegro_init():
    subprocess.call(["allegroai-init"])


def get_val(name, default, hide=False):
    if name in os.environ:
        if hide:
            return f"{''.join(['*']*5)}{os.environ[name][-5:]}"
        else:
            return os.environ[name]
    return default


def collect_param(prompt_name, env_var_name, sensitive=False, passPrompt=False):
    if passPrompt:
        newval = getpass.getpass(
            f"{prompt_name} [{get_val(env_var_name,'',sensitive)}]: "
        )
    else:
        newval = input(f"{prompt_name} [{get_val(env_var_name,'',sensitive)}]: ")
    if newval == "":
        newval = get_val(env_var_name, "", False)
    return newval


@click.group()
def cli():
    pass


@cli.command()
def init_chem():
    # List of packages to install
    packages = [
        "torch-scatter==2.1.0",
        "torch-sparse==0.6.16",
        "torch-geometric==2.2.0",
        "torch-spline-conv==1.2.1",
        "torch-cluster==1.6.0",
        "git+https://github.com/pyg-team/pyg-lib.git",
    ]

    # Loop through packages and install each one
    cmd = ["pip", "install"]
    cmd.extend(packages)
    subprocess.check_call(cmd)


@cli.command()
def init():
    albert_config_dir = os.path.join(os.path.expanduser("~"), ".albert/")
    if not os.path.isdir(albert_config_dir):
        os.makedirs(albert_config_dir)

    if os.path.exists(os.path.join(albert_config_dir, "config")):
        dotenv.load_dotenv(os.path.join(albert_config_dir, "config"))
    # if os.path.exists(".env"):
    #    dotenv.load_dotenv(".env")

    token = collect_param("Albert JWT", "ALBERT_TOKEN", True)
    devtoken = collect_param(
        "Albert Staging/Dev JWT [blank for None]", "ALBERT_TOKEN_DEV", True
    )
    print("Albert Warehouse Configuration:")
    dbhost = collect_param("Host", "DB_HOST", False)
    dbport = collect_param("Port", "DB_PORT", False)
    dbuser = collect_param("Username", "DB_USER", False)
    dbpassword = collect_param("Password", "DB_PASSWORD", True, True)
    dbdatabase = collect_param("Default Database", "DB_DATABASE", False)

    with open(os.path.join(albert_config_dir, "config"), "w") as f:
        f.write(f'ALBERT_TOKEN="{token}"\n')
        f.write(f'ALBERT_TOKEN_DEV="{devtoken}"\n')
        f.write(f'DB_HOST="{dbhost}"\n')
        f.write(f'DB_PORT="{dbport}"\n')
        f.write(f'DB_USER="{dbuser}"\n')
        f.write(f'DB_PASSWORD="{dbpassword}"\n')
        f.write(f'DB_DATABASE="{dbdatabase}"\n')

    clearml = input("Will you be using ClearML integrations (default No)? [Y/n]:")
    while clearml.lower() not in ["y", "n", "yes", "no", ""]:
        clearml = input("Will you be using ClearML integrations? [Y/n]")
    if clearml.lower() in ["y", "yes"]:
        pipcmd = input(
            "Paste the pip install command as found in your clearml setup instance here: "
        )
        install_allegro(pipcmd)
        run_allegro_init()


if __name__ == "__main__":
    init()
