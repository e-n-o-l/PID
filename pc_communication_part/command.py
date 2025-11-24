import functools

class Command:
    def __init__(self):
        self._command = None
        self.allowed_commands = {}
        self.descriptions = ["quit: stops the program(doesn't stop any continues command)"]
        self.dependencies = {}

    def map_func(self, func):
        name = func.__name__ if "_" not in func.__name__ else func.__name__.replace("_", " ")
        self.allowed_commands[name] = func
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def description(self, text: str):
        def decorator(func):
            self.descriptions.append(f'{func.__name__}: {text}')
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def execute(self) -> None:
        self.allowed_commands[self.command]()

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command: str):
        if command not in self.allowed_commands:
            raise RuntimeError()
        self._command = command