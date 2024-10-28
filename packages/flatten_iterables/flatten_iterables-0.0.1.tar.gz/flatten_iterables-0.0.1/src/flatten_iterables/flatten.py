import typing

mappables = {dict}
iterables = {list}


def flatten(it=None) -> typing.Any:

    global mappables, iterables

    _mappables = tuple(mappables)
    _iterables = tuple(iterables)
    seen = list()
    ot = dict()

    if isinstance(it, _mappables):
        stack = list((f"['{k}']", v) if isinstance(k, str) else (f"[{k}]", v) for k, v in it.items())[::-1]
    elif isinstance(it, _iterables):
        stack = list((f"[{k}]", v) for k, v in enumerate(it))[::-1]

    while stack:
        path, value = stack.pop()
        for ref in seen:
            if value is ref:
                raise ValueError("Circular reference detected")
        if isinstance(value, _mappables):
            seen.append(value)
            if len(value) == 0:
                ot[path] = value
            stack = (
                stack
                + list((f"{path}['{k}']", v) if isinstance(k, str) else (f"{path}[{k}]", v) for k, v in value.items())[
                    ::-1
                ]
            )
        elif isinstance(value, _iterables):
            seen.append(value)
            if len(value) == 0:
                ot[path] = value
            else:
                stack = stack + list((f"{path}[{k}]", v) for k, v in enumerate(value))[::-1]
        else:
            ot[path] = value
    return ot
