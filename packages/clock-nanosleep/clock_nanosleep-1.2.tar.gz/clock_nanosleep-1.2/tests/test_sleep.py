import unittest
import sys
from time import perf_counter

from clock_nanosleep import sleep

class SleepTestCase(unittest.TestCase):
    def test_arg_type(self):
        with self.assertRaises(TypeError):
            sleep()
        with self.assertRaises(TypeError):
            sleep(1, 2)
        with self.assertRaises(ValueError):
            sleep('a')
        with self.assertRaises(ValueError):
            sleep(b'a')
        with self.assertRaises(ValueError):
            sleep(('a',))
        with self.assertRaises(ValueError):
            sleep(['a',])

    def test_arg_range(self):
        # int
        with self.assertRaises(ValueError):
            sleep(-1)
        with self.assertRaises(ValueError):
            sleep(2**63)
        # float
        with self.assertRaises(ValueError):
            sleep(-1.1)
        with self.assertRaises(ValueError):
            sleep(-1e-9)
        with self.assertRaises(ValueError):
            sleep(float('nan'))
        with self.assertRaises(ValueError):
            sleep(sys.float_info.max)
        with self.assertRaises(ValueError):
            sleep(9.3e+9)

    def test_0(self):
        sleep(0)
        sleep(-0)
        sleep(0.0)
        sleep(-0.0)

        # not 0, but very small.
        sleep(0.000_000_000_001)
        sleep(0.000_000_000_01)
        sleep(0.000_000_000_1)
        sleep(0.000_000_001)
        sleep(0.000_001)
        sleep(0.001)

    def test_sleep(self):
        secs = (0.2, 1, 1.5)
        print('(please wait %.2f seconds)' % sum(secs))

        for sec in secs:
            t1 = perf_counter()
            sleep(sec)
            delta = perf_counter() - t1

            if delta > sec:
                big, small = delta, sec
            else:
                big, small = sec, delta
            ratio = big / small
            self.assertLessEqual(ratio, 1.2,
                                 ('There is a significant difference between '
                                  'sleep time and measured time, may be '
                                  'due to unstable testing environment.'))

if __name__ == "__main__":
    unittest.main()
