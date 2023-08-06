from .torchvault import TorchVault


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


def diff(sha1, sha2, log_dir="./model_log"):
    vault = TorchVault(log_dir)
    vault.diff(sha1, sha2)


def add_tag(tag="", sha="", log_dir="./model_log"):
    vault = TorchVault(log_dir)
    vault.add_tag(sha, tag)


def add_result(result=0, sha="", log_dir="./model_log"):
    vault = TorchVault(log_dir)
    vault.add_result(sha, result)


def log_all(model, tag="", result=0, log_dir="./model_log", model_dir="./"):
    vault = TorchVault(log_dir, model_dir)
    vault.log_model(model)
    vault.add_tag("", tag)
    vault.add_result("", result)


"""
Other utils
"""


def find(log_dir="./model_log", model_dir="./", condition="hash", hash="", tag="", min=0, max=100):
    vault = TorchVault(log_dir, model_dir)
    vault.find(condition, hash, tag, min, max)
    vault.show_result(hash)
