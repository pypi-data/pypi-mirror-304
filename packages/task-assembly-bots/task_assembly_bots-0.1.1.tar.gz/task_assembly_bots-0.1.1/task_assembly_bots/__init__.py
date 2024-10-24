import json
from inspect import Signature
from typing import Callable
from collections import Counter
from collections.abc import Iterable


class Value:
    def __init__(self, value=None, **kwargs):
        # TODO: Build this out to do all of the necessary formatting and data cleaning
        self.value = {}
        if isinstance(value, dict):
            self.value = value
            self.value.update(kwargs)
        elif value:
            self.value = value
        else:
            self.value = kwargs

    @property
    def response(self):
        return {"value": self.value}


class Error:
    def __init__(self, message: str):
        self.message = str(message)

    @property
    def response(self):
        return {"error": self.message}


class Extend:
    def __init__(self, extend=True):
        self.extend = extend

    @property
    def response(self):
        return {"extend": self.extend}


class ResponseScores:
    def __init__(self, scores: list[int]):
        for score in scores:
            if not isinstance(score, int) or score < 0 or score > 100:
                raise ValueError("Scores must integers be between 0 and 100")
        self.scores = scores

    @property
    def response(self):
        return {"responseScores": self.scores}


def __build_params(func: Callable, event: dict, parameter_names: list[str]):
    params = {}
    for i, param in enumerate(Signature.from_callable(func).parameters):
        if param in parameter_names or f"{param}_" in parameter_names:
            params[param] = event.get(param)
        else:
            params[param] = event.get(parameter_names[i])
    return params


def __build_response(result):
    if isinstance(result, dict):
        return result
    elif isinstance(result, str):
        return {"value": result}
    elif isinstance(result, Error):
        return result.response
    elif isinstance(result, (Value, Extend, ResponseScores)):
        return result.response
    elif isinstance(result, Iterable):
        response = {}
        for r in result:
            response.update(__build_response(r))
        return response
    else:
        return {"value": result}


def __create_bot_wrapper(func: Callable, parameter_names: list[str]):
    def wrapper(event, context=None) -> dict:
        params = __build_params(
            func, event, parameter_names=parameter_names
        )
        try:
            result = func(**params)
        except Exception as e:
            result = Error(str(e))
        return __build_response(result)

    wrapper.local = func
    return wrapper


def launch_bot(func):
    return __create_bot_wrapper(func, ["input", "context", "parameters"])


def response_bot(func):
    return __create_bot_wrapper(func, ["value", "input", "context", "parameters"])


def result_bot(func):
    return __create_bot_wrapper(func, ["responses", "workers", "input", "context", "parameters"])


def scoring_bot(func):
    return __create_bot_wrapper(func, ["response", "expected", "input", "worker", "context", "parameters"])


def integration_bot(func):
    return __create_bot_wrapper(func, ["input", "context", "parameters"])


def text_agreement(values: list[str], count: int):
    counter = Counter([v.strip() for v in values])
    mc = counter.most_common(1)
    if mc[0][1] >= count:
        return mc[0][0]
    else:
        return None
