"""Key-value 相关工具"""

from functools import singledispatch
from itertools import chain
from pathlib import Path
from typing import Any, OrderedDict

from zyplib.utils.fs import read_json, read_yaml
from zyplib.utils.print import print_error


def collect_key_path(target: dict | str | Path, key: str):
    """获取 一个字典中所有制定 key 的对象，并返回其压缩后的对象 {路径: value}

    >>> dic = {
        'loss': 1,
        'avg': { 'loss': 1.2 },
        'Exp': { 'Round0': { 'loss': 2 }, 'Round1': { 'loss': 1 } }
    }
    >>> collect_key_paths(dic, 'loss')
    {'loss': 1, 'avg.loss': 1.2, 'Exp.Round0.loss': 2, 'Exp.Round1.loss': 1}

    - 输入参数可以为 dict 对象：对对象进行检索
    - 也可以为一个路径：检索路径下所有 yml 和 json 文件内的 key，并返回汇总结果
    """
    if isinstance(target, dict):
        return _collect_key_path_core(target, key)
    elif isinstance(target, (str, Path)):
        return _collect_key_path_files(target, key)
    else:
        raise TypeError(f'Invalid target: {target}')


def _collect_key_path_core(target: dict, key: str) -> dict[str, Any]:
    """处理字典类型的输入"""
    result = {}

    def recurse(sub_dict: dict, parent_key: str = ''):
        # 遍历当前字典的键值对
        for k, v in sub_dict.items():
            # 更新路径信息
            new_key = f'{parent_key}.{k}' if parent_key else k
            # 如果当前键等于目标键，保存值
            if k == key:
                result[new_key] = v
            # 如果值是字典，递归调用
            if isinstance(v, dict):
                recurse(v, new_key)

    # 从根字典开始递归
    recurse(target)
    return result


def _collect_key_path_files(
    target: str | Path, key: str
) -> OrderedDict[str, dict[str, Any]]:
    """处理目录路径类型的输入"""
    path = Path(target)
    result = OrderedDict()

    # 递归查看目录中的所有 YAML/JSON 文件
    all_files = chain(path.rglob('*.yaml'), path.rglob('*.yml'), path.rglob('*.json'))
    for fpath in all_files:
        content: dict = {}
        try:
            if fpath.suffix in ('.yaml', '.yml'):
                content = read_yaml(fpath)
            elif fpath.suffix == '.json':
                content = read_json(fpath)
            else:
                continue

            # 提取key-value对
            key_paths = _collect_key_path_core(content, key)
            if key_paths:  # 只保留非空的结果
                result[str(fpath)] = key_paths

        except Exception as e:
            print_error(f'Error reading {fpath}: {repr(e)}')

    return result


class DottableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_nested_dicts()

    def _convert_nested_dicts(self):
        for key, value in list(self.items()):
            if isinstance(value, dict) and not isinstance(value, DottableDict):
                super().__setitem__(key, DottableDict(value))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DottableDict' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def _process_nested_key(self, key):
        """处理可能包含点号的键

        Returns:
            tuple: (is_nested, keys)
                - is_nested: 是否是嵌套的键
                - keys: 键的列表
        """
        if not isinstance(key, str):
            return False, None
        if '.' not in key:
            return False, None
        return True, key.split('.')

    def __getitem__(self, key):
        is_nested, keys = self._process_nested_key(key)
        if not is_nested:
            return super().__getitem__(key)

        d = self
        for k in keys:
            d = d[k]
        return d

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, DottableDict):
            value = DottableDict(value)

        is_nested, keys = self._process_nested_key(key)
        if not is_nested:
            super().__setitem__(key, value)
            return

        d = self
        for k in keys[:-1]:
            if k not in d:
                d[k] = DottableDict()
            d = d[k]
        d[keys[-1]] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DottableDict' object has no attribute '{key}'")

    def __delitem__(self, key):
        is_nested, keys = self._process_nested_key(key)
        if not is_nested:
            super().__delitem__(key)
            return

        d = self
        for k in keys[:-1]:
            if k not in d:
                raise KeyError(key)
            d = d[k]
        del d[keys[-1]]

    def __contains__(self, key):
        is_nested, keys = self._process_nested_key(key)
        if not is_nested:
            return super().__contains__(key)

        try:
            d = self
            for k in keys:
                d = d[k]
            return True
        except (KeyError, TypeError):
            return False

    def update(self, other=None, **kwargs):
        if other is not None:
            for k, v in other.items():
                if isinstance(v, dict):
                    if k in self and isinstance(self[k], DottableDict):
                        self[k].update(v)
                    else:
                        self[k] = DottableDict(v)
                else:
                    self[k] = v

        for k, v in kwargs.items():
            if isinstance(v, dict):
                if k in self and isinstance(self[k], DottableDict):
                    self[k].update(v)
                else:
                    self[k] = DottableDict(v)
            else:
                self[k] = v
