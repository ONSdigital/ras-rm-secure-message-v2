import itertools
from typing import Any


class ValidatorBase:
    """
    Base class for performing validation of a dictionary against a specific criteria, for example checking
    existence of specific keys, format of specific values, etc.

    Each subclass must be a callable, i.e. must implement dunder method __call__, which accepts the
    dictionary to be validated and returns True if the dictionary is deemed valid. The member property
    _errors should also be set, this is a list of string values, where each string value is an error
    message (where errors exist). I.e. multiple errors may be found for any given dictionary, thus
    multiple error messages can be set.
    """

    def __init__(self) -> None:
        self._errors: list[str] = []

    @property
    def errors(self) -> list[str]:
        return self._errors


class Exists(ValidatorBase):
    ERROR_MESSAGE = "Required key '{}' is missing."

    def __init__(self, *keys: str) -> None:
        super().__init__()
        self._keys = set(keys)
        self._diff: set[Any]

    def __call__(self, data: dict) -> bool:
        keys = flatten_keys(data)
        self._diff = self._keys.difference(keys)
        self._errors = [self.ERROR_MESSAGE.format(d) for d in self._diff]
        return len(self._diff) == 0


class Validator:
    def __init__(self, *rules: Any):
        self._rules: list = list(rules)
        self.valid = True

    def validate(self, d: dict) -> bool:
        self.valid = all([r(d) for r in self._rules])
        return self.valid

    @property
    def errors(self) -> list:
        return list(itertools.chain(*[r.errors for r in self._rules]))


def flatten_keys(d: dict, prefix: str = "") -> list[str]:
    prefix = prefix or ""
    result = []

    for k, v in d.items():
        result.append(".".join([prefix, k] if prefix else [k]))

    return result
