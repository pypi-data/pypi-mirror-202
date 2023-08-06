def say_hello(name=None):
    if name is None:
        return f'Hello World!'
    else:
        return f"hello, {name}"
