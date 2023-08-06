from .torchvault import TorchVault
import click

"""
Logging Functions
"""


def log(model, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.log_model(model)


def log_scheduler(scheduler, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.log_scheduler(scheduler)


def log_optimizer(optimizer, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.log_optimizer(optimizer)


def diff(sha1="", index1=-1, sha2="", index2=-1, out=False, ask_gpt=False, log_dir="./model_log"):
    # def diff(self, sha1="", index1=-1, sha2="", index2=-1, out=False, ask_gpt=False)
    vault = TorchVault(log_dir)
    vault.diff(sha1, index1, sha2, index2, out, ask_gpt)


def add_tag(tag="", sha="", log_dir="./model_log"):
    vault = TorchVault(log_dir)
    vault.add_tag(sha, tag)


def add_result(result=0, sha="", log_dir="./model_log"):
    vault = TorchVault(log_dir)
    vault.add_result(sha, result)


def log_all(model, tag="", result=-1, optimizer=None, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.log_model(model)
    if optimizer is not None:
        vault.log_optimizer(optimizer)
    if tag is not "":
        vault.add_tag("", tag)
    if result is not -1:
        vault.add_result("", result)


"""
Other utils
"""


def find(log_dir="./model_log", model_dir="./", condition="hash", hash="", tag="", min=0, max=100):
    vault = TorchVault(log_dir, model_dir)
    target_models = vault.find(condition, hash, tag, min, max)
    vault.show_result(target_models)


"""
cli utils
"""


@click.command()
@click.option("--find_flag", is_flag=True, default=False, help="tvault cli for tvault.find")
@click.option("--diff_flag", is_flag=True, default=False, help="tvault cli for tvault.diff")
# options for find
@click.option("--log_dir", type=str, default="./model_log")
@click.option("--model_dir", type=str, default="./")
@click.option("--condition", type=str, default="hash")
@click.option("--hash", type=str, default="")
@click.option("--tag", type=str, default="")
@click.option("--min", type=int, default=0)
@click.option("--max", type=int, default=100)
# options for diff
@click.option("--sha1", type=str, default="")
@click.option("--index1", type=str, default="")
@click.option("--sha2", type=str, default="")
@click.option("--index2", type=str, default="")
def cli_main(
    find_flag,
    diff_flag,
    log_dir,
    model_dir,
    condition,
    hash,
    tag,
    min,
    max,
    sha1,
    index1,
    sha2,
    index2,
):
    if find_flag:
        find(log_dir, model_dir, condition, hash, tag, min, max)
    elif diff_flag:
        diff(sha1, index1, sha2, index2, out=False, ask_gpt=False, log_dir=log_dir)
    else:
        print("tvault: not implemented")
