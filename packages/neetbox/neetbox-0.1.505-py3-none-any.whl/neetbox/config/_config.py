import collections
from neetbox.utils.utils import patch


def _default_none():
    return None


DEFAULT_CONFIG = collections.defaultdict(_default_none)
DEFAULT_CONFIG.update({"logging": {"logdir": None}, "integrations": {}})

WORKSPACE_CONFIG: dict = DEFAULT_CONFIG.copy()


def _update(cfg: dict):
    def _update_dict_recursively(self: dict, the_other: dict):
        for _k, _v in the_other.items():
            if type(_v) is dict:  # currently resolving a dict child
                if _k in self:  # dfs merge
                    _update_dict_recursively(self=self[_k], the_other=the_other[_k])
                else:
                    self[_k] = the_other[_k]
            else:  # not a dict, overwriting
                self[_k] = the_other[_k]

    global WORKSPACE_CONFIG
    _update_dict_recursively(WORKSPACE_CONFIG, cfg)


def _get():
    global WORKSPACE_CONFIG
    return WORKSPACE_CONFIG
