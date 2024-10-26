import random


CHARSET: str = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
DEFAULT_VALUE_LENGTH: int = 12


class CFID:
    def __init__(self, value: str = None, length: int = DEFAULT_VALUE_LENGTH):
        if value is None:
            value = Crockford32.generate_from_random_charset_choice(length=length)

        self.value: str = value
        self.__clean_value()

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "%s(value=%r)" % (self.__class__.__name__, str(self.value))

    def __eq__(self, other):
        match other:
            case CFID():
                return self.value == other.value
            case str():
                return self.value == other
            case _:
                raise NotImplementedError

    def __str__(self) -> str:
        return self.value

    def __clean_value(self) -> None:
        # https://www.crockford.com/base32.html

        excluded_letters = {
            "i": "1",
            "I": "1",
            "l": "1",
            "L": "1",
            "O": "0",
            "o": "0",
        }
        self.value = "".join(excluded_letters.get(c, c) for c in self.value).upper()


class Crockford32:
    @staticmethod
    def generate_from_random_charset_choice(length: int = DEFAULT_VALUE_LENGTH):
        return "".join(random.choices(CHARSET, k=length))
