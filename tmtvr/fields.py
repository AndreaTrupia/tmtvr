from datetime import datetime, timezone


class Field:
    def __init__(self, required=False, default=None):
        self.required = required
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class StringField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected str, got {type(value).__name__}')
        super().__set__(instance, value)


class IntegerField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected int, got {type(value).__name__}')
        super().__set__(instance, value)


class FloatField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise TypeError(f'Expected float, got {type(value).__name__}')
        super().__set__(instance, value)


class DateTimeField(Field):
    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise TypeError(f'Expected ISO 8601 format, got {value}')
        if not isinstance(value, datetime):
            raise TypeError(f'Expected datetime, got {type(value).__name__}')
        super().__set__(instance, value)
