from omegaconf import ListConfig
import torch

_TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_gpu_list_from_cfg(cfg):

    if _TORCH_DEVICE == "cpu":
        gpus = 0
    elif isinstance(cfg.training.gpu_id, list):
        gpus = cfg.training.gpu_id
    elif isinstance(cfg.training.gpu_id, ListConfig):
        gpus = list(cfg.training.gpu_id)
    elif isinstance(cfg.training.gpu_id, int):
        gpus = [cfg.training.gpu_id]
    else:
        raise NotImplementedError(
            "training.gpu_id must be list or int, not {}".format(
                type(cfg.training.gpu_id)
            )
        )
    return gpus


def pretty_print_str(string: str, symbol: str = "-") -> None:
    str_length = len(string)
    print(symbol * str_length)
    print(string)
    print(symbol * str_length)
