import json
import re
from rich.console import Console
import ast

console = Console()


def extract_call_and_kwargs_from_line(line):
    pattern = r"'call': '([^']+)', 'kwargs':\s*({[^{}]*})"
    match = re.search(pattern, line)
    if match:
        call = match.group(1)
        kwargs = match.group(2)
        kwargs = ast.literal_eval(kwargs)
        return call, kwargs
    else:
        return None, None


def count_call_with_kwargs(string, call, kwargs):
    counter = 0
    for line in string.splitlines():
        cur_call, cur_kwargs = extract_call_and_kwargs_from_line(line)
        if cur_call == call and cur_kwargs == kwargs:
            counter += 1
    return counter


def count_call(string, call, kwargs):
    counter = 0
    for line in string.splitlines():
        if (str(call) in line) and (str(kwargs) in line):
            counter += 1
    return counter


def count_calls(string, call):
    counter = 0
    for line in string.splitlines():
        cur_call, _ = extract_call_and_kwargs_from_line(line)
        if cur_call == call:
            counter += 1
    return counter


def assertion_error_msg(call, kwargs, num_calls):
    return f"\ncall: {call}\nkwargs:{kwargs}\nrequired calls:{num_calls}"
