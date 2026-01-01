import uuid
import os
import unittest
import tempfile
import team_league_generator
from team_league_generator.errors import (
    InvalidSizeRequestError,
    NotIterableError,
)
from team_league_generator.generics import (
    IterableDataLoader,
    UniformGenerator,
    BaseLinearBiasedGenerator,
    LinearBiasedGenerator,
    ReversedLinearBiasedGenerator,
)


class GenericsTests(unittest.TestCase):
    """
    Test generic data types and generators.
    """

    def random_data(self, size):
        return [str(uuid.uuid4()) for j in range(size)]

    def test_iterable_data_loader(self):
        data = self.random_data(100)
        i = IterableDataLoader(data)
        self.assertEqual(data, i.data)

    def test_iterable_data_loader_errors(self):
        data = True
        with self.assertRaises(NotIterableError):
            i = IterableDataLoader(data)

    def check_generator(self, GenClass):
        nsamples = 100

        data = self.random_data(nsamples)
        g = GenClass(data=data)

        sample = g.generate()[0]
        self.assertIn(sample, data)

        sample = g.generate()[0]
        self.assertIn(sample, data)

        samples = g.generate(size=nsamples // 2)
        for sample in samples:
            self.assertIn(sample, data)

        with self.assertRaises(InvalidSizeRequestError):
            g.generate(size=nsamples + 1)

    def test_uniform_generator(self):
        class SampleUniformGenerator(IterableDataLoader, UniformGenerator):
            pass

        self.check_generator(SampleUniformGenerator)

    def test_base_linear_biased_generator(self):
        class SampleBaseLinearBiasedGenerator(
            IterableDataLoader, BaseLinearBiasedGenerator
        ):
            pass

        self.check_generator(SampleBaseLinearBiasedGenerator)

    def test_linear_biased_generator(self):
        class SampleLinearBiasedGenerator(IterableDataLoader, LinearBiasedGenerator):
            pass

        self.check_generator(SampleLinearBiasedGenerator)

    def test_reversed_linear_biased_generator(self):
        class SampleReversedLinearBiasedGenerator(
            IterableDataLoader, ReversedLinearBiasedGenerator
        ):
            pass

        self.check_generator(SampleReversedLinearBiasedGenerator)


class BiasTests(unittest.TestCase):
    """
    Test that the different biased generators
    are correctly biased.
    """

    def get_data(self):
        return ["blue", "red", "green", "yellow", "purple"]

    def get_pct_samples(self, color, samples):
        count = sum([1 for s in samples if s == color])
        return count / len(samples)

    def test_bias_uniform_generator(self):
        class SampleUniformGenerator(IterableDataLoader, UniformGenerator):
            pass

        data = self.get_data()
        g = SampleUniformGenerator(data=data)
        samples = [g.generate()[0] for j in range(1000)]
        pct_red = self.get_pct_samples("red", samples)
        self.assertLess(pct_red, 0.50)

    def test_bias_linear_biased_generator(self):
        """
        Expected probabilities for a five-item list:

        blue    5 / (5+4+3+2+1) = 33.3%
        red     4 / ( ...     ) = 26.6%
        green   3 / ( ...     ) = 20.0%
        yellow  2 / ( ...     ) = 13.3%
        purple  1 / ( ...     ) = 6.6%
        """
        # -------------------
        # Define test classes

        class SampleLinearBiasedGenerator(IterableDataLoader, LinearBiasedGenerator):
            pass

        class SampleRevLinearBiasedGenerator(
            IterableDataLoader, ReversedLinearBiasedGenerator
        ):
            pass

        # -------------------
        # Test the linear bias generator

        g = SampleLinearBiasedGenerator(data=self.get_data())

        samples = [g.generate()[0] for j in range(10000)]

        # First item in list is most likely
        pct_blue = self.get_pct_samples("blue", samples)
        self.assertLess(pct_blue, 0.35)
        self.assertGreater(pct_blue, 0.28)

        pct_purp = self.get_pct_samples("purple", samples)
        self.assertLess(pct_purp, 0.08)
        self.assertGreater(pct_purp, 0.04)

        # -------------------
        # Test the reversed linear bias generator

        h = SampleRevLinearBiasedGenerator(data=self.get_data())

        revsamples = [h.generate()[0] for j in range(10000)]

        # Last item in list is most likely
        revpct_purp = self.get_pct_samples("purple", revsamples)
        self.assertLess(revpct_purp, 0.35)
        self.assertGreater(revpct_purp, 0.28)

        revpct_blue = self.get_pct_samples("blue", revsamples)
        self.assertLess(revpct_blue, 0.08)
        self.assertGreater(revpct_blue, 0.04)
