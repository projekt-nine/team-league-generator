from collections.abc import Iterable
import random
from .errors import NotIterableError, InvalidSizeRequestError


class IterableDataLoader(object):
    def __init__(self, data):
        if isinstance(data, Iterable):
            self.data = data
        else:
            raise NotIterableError(
                "Error: data provided to {self.__class__.__name__} was not iterable!"
            )


class UniformGenerator(object):
    def generate_nonunique(self, size=1):
        """
        Sample data with replacement using uniform bias.
        Returns a list of the specified size.
        """
        if size > len(self.data) or size < 0:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: generate_nonunique method got size parameter {size}, must be between 0 and {len(self.data)}"
            )
        return random.choices(self.data, k=size)

    def generate(self, size=1):
        """
        Sample data without replacement using uniform bias.
        Returns a list of the specified size.
        """
        if size > len(self.data) or size < 0:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: generate_nonunique method got size parameter {size}, must be between 0 and {len(self.data)}"
            )
        if size > (2 * len(self.data)) // 3 and len(self.data) > 100:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: requested too many unique choices (>2/3 of a data set with >1k items)"
            )
        choices = set()
        while len(choices) < size:
            choices.add(random.choice(self.data))
        return list(choices)


class BaseLinearBiasedGenerator(object):
    """
    Returns a generator that will be linearly biased to return items from the top of the list.

    Example: a five-item list would have the following probabilities:

    blue    5 / (5+4+3+2+1) = 25%
    red     4 / ( ...     ) = 20%
    green   3 / ( ...     ) = 15%
    yellow  2 / ( ...     ) = 10%
    purple  1 / ( ...     ) = 5%

    If reversed:
    """

    def generate_nonunique(self, size=1, reverse=False):
        """
        Sample data with replacement using linear bias.
        Returns a list of the specified size.

        Normally, bias is toward items at front of list.
        If reverse is true, bias is twoard items at back of list.
        """
        if size > len(self.data) or size < 0:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: generate_nonunique method got size parameter {size}, must be between 0 and {len(self.data)}"
            )
        revweights = list(range(1, len(self.data) + 1))
        if reverse:
            weights = revweights
        else:
            weights = list(reversed(revweights))

        # Note: this returns repeats. it's up to the user to filter duplicates
        return random.choices(self.data, weights=weights, k=size)

    def generate(self, size=1, reverse=False):
        """
        Sample data without replacement using linear bias.
        Returns a list of the specified size.

        Normally, bias is toward items at front of list.
        If reverse is true, bias is twoard items at back of list.
        """
        if size > len(self.data) or size < 1:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: generate method got size parameter {size}, must be between 0 and {len(self.data)}"
            )
        if size > (2 * len(self.data)) // 3 and len(self.data) > 100:
            raise InvalidSizeRequestError(
                f"{self.__class__.__name__}: Error: requested too many unique choices (>2/3 of a data set with >1k items)"
            )
        revweights = list(range(1, len(self.data) + 1))
        if reverse:
            weights = revweights
        else:
            weights = list(reversed(revweights))

        choices = set()
        while len(choices) < size:
            choices.add(random.choices(self.data, weights=weights, k=1)[0])
        return list(choices)


class LinearBiasedGenerator(BaseLinearBiasedGenerator):
    """
    Generator that is linearly biased toward items at the front of the list
    """

    def generate_nonunique(self, size=1):
        return super().generate_nonunique(size, reverse=False)

    def generate(self, size=1):
        return super().generate(size, reverse=False)


class ReversedLinearBiasedGenerator(BaseLinearBiasedGenerator):
    """
    Generator that is linearly biased toward items at the back of the list
    """

    def generate_nonunique(self, size=1):
        return super().generate_nonunique(size, reverse=True)

    def generate(self, size=1):
        return super().generate(size, reverse=True)
