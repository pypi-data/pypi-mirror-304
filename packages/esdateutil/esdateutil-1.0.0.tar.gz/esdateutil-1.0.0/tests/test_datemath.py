from datetime import datetime, timedelta, timezone

from esdateutil import datemath
from tests import utils

# TODO We removed several tests that used a timezone of CET - we need some tests that straddle DST timezones to eval how that works in python. zoneinfo is only added in 3.9. tzdata https://pypi.org/project/tzdata/ is 1st party backwards compat option for testing in 3.3-3.8
# ES Datemath Tests: https://github.com/elastic/elasticsearch/blob/main/server/src/test/java/org/elasticsearch/common/time/JavaDateMathParserTests.java

# TODO DateMath arg timezone to tzinfo to not conflict with datetime.timezone, then %s/timezone=tzinfo/tzinfo=tzinfo/g and update test_now_timezone

def generate_assert_datemath_eval_equals_test(*args, **kwargs):
    def test_fn(self):
        self.assert_datemath_eval_equals(*args, **kwargs)
    return test_fn

def generate_assert_datemath_parse_exceptions_test(*args, **kwargs):
    def test_fn(self):
        self.assert_datemath_parse_exceptions(*args, **kwargs)
    return test_fn

class DateMathTests(utils.TestShim):
    def assert_datemath_eval_equals(self, given, expected, **kwargs):
        dm = datemath.DateMath(**kwargs)
        self.assertEqual(dm.eval(given), dm.eval(expected))

    def assert_datemath_parse_exceptions(self, given, expected_exception):
        dm = datemath.DateMath()
        try:
            # Consume generator.
            for _ in dm.parse(given):
                pass
        except type(expected_exception) as e:
            self.assertEqual(e.args, expected_exception.args)
        else:
            raise RuntimeError("Did not receive expected exception when parsing {}".format(given))

    @classmethod
    def gen_basic_math(cls):
        test_name = "test_basic_math"
        arg_names = ["given", "expected"]
        args_it = [
            ("2014-11-18||+y", "2015-11-18"),
            ("2014-11-18||-2y", "2012-11-18"),

            ("2014-11-18||+3M", "2015-02-18"),
            ("2014-11-18||-M", "2014-10-18"),
            ("2014-11-18||-11M", "2013-12-18"),
            ("2014-01-18||-13M", "2012-12-18"),
            ("2014-11-18||+25M", "2016-12-18"),
            ("2014-11-18||+26M", "2017-01-18"),

            ("2014-11-18||+1w", "2014-11-25"),
            ("2014-11-18||-3w", "2014-10-28"),

            ("2014-11-18||+22d", "2014-12-10"),
            ("2014-11-18||-423d", "2013-09-21"),

            ("2014-11-18T14||+13h", "2014-11-19T03"),
            ("2014-11-18T14||-1h", "2014-11-18T13"),
            ("2014-11-18T14||+13H", "2014-11-19T03"),
            ("2014-11-18T14||-1H", "2014-11-18T13"),

            ("2014-11-18T14:27||+10240m", "2014-11-25T17:07"),
            ("2014-11-18T14:27||-10m", "2014-11-18T14:17"),

            ("2014-11-18T14:27:32||+60s", "2014-11-18T14:28:32"),
            ("2014-11-18T14:27:32||-3600s", "2014-11-18T13:27:32"),
        ]

        cls.generate_tests_from_iter(test_name, args_it, arg_names, generator_fn=generate_assert_datemath_eval_equals_test)

    def test_lenient_no_math(self):
        self.assert_datemath_eval_equals("2014-05-30T20:21", "2014-05-30T20:21:00.000")

    def test_lenient_empty_math(self):
        self.assert_datemath_eval_equals("2014-05-30T20:21||", "2014-05-30T20:21:00.000")

    @classmethod
    def gen_multiple_adjustments(cls):
        test_name = "test_multiple_adjustments"
        arg_names = ["given", "expected"]
        args_it = [
            ("2014-11-18||+1M-1M", "2014-11-18"),
            ("2014-11-18||+1M-1m", "2014-12-17T23:59"),
            ("2014-11-18||-1m+1M", "2014-12-17T23:59"),
            ("2014-11-18||+1M/M", "2014-12-01"),
            ("2014-11-18||+1M/M+1h", "2014-12-01T01"),
        ]

        cls.generate_tests_from_iter(test_name, args_it, arg_names, generator_fn=generate_assert_datemath_eval_equals_test)

    @classmethod
    def gen_now(cls):
        test_name = "test_now"
        arg_names = ["given", "expected"]
        args_it = [
            ("now", "2014-11-18T14:27:32"),
            ("now+M", "2014-12-18T14:27:32"),
            ("now+M", "2014-12-18T14:27:32"),
            ("now-2d", "2014-11-16T14:27:32"),
            ("now/m", "2014-11-18T14:27"),
            ("now/M", "2014-11-01T00:00:00"),
        ]
        kwargs_static = {
            "now_fn": lambda _: datetime(2014, 11, 18, 14, 27, 32)
        }

        cls.generate_tests_from_iter(test_name, args_it, arg_names, kwargs_static=kwargs_static, generator_fn=generate_assert_datemath_eval_equals_test)

    @classmethod
    def gen_now_round_up(cls):
        test_name = "test_now_round_up"
        arg_names = ["given", "expected"]
        args_it = [
            ("now", "2014-11-18T14:27:32"),
            ("now+M", "2014-12-18T14:27:32"),
            ("now+M", "2014-12-18T14:27:32"),
            ("now-2d", "2014-11-16T14:27:32"),
            ("now/m", "2014-11-18T14:27:59.999000"),
            ("now/M", "2014-11-30T23:59:59.999000"),
            ("now/m", "2014-11-18T14:27:59.999"),
            ("now/M", "2014-11-30T23:59:59.999"),
        ]
        kwargs_static = {
            "now_fn": lambda _: datetime(2014, 11, 18, 14, 27, 32),
            "units_round": datemath.UNITS_ROUND_UP_MILLIS
        }

        cls.generate_tests_from_iter(test_name, args_it, arg_names, kwargs_static=kwargs_static, generator_fn=generate_assert_datemath_eval_equals_test)

    def test_now_timezone(self):
        now = datetime(2014, 11, 18, 14, 27, 32)
        self.assert_datemath_eval_equals("now/m", "2014-11-18T14:27", now_fn=lambda tz: now.replace(tzinfo=tz), tzinfo=timezone(timedelta(hours=2)))

    @classmethod
    def gen_implicit_rounding(cls):
        test_name = "test_implicit_rounding"
        arg_names = ["given", "expected"]
        kwarg_names = ["tzinfo"]
        args_kwargs_it = [
            ("2014-11-18", "2014-11-18", None),
            ("2014-11-18T09:20", "2014-11-18T09:20", None),

            ("2014-11-18", "2014-11-17T23:00:00.000Z", timezone(timedelta(hours=1))),
            ("2014-11-18T09:20", "2014-11-18T08:20:00.000Z", timezone(timedelta(hours=1))),
        ]

        cls.generate_tests_from_iter(test_name, args_kwargs_it, arg_names, kwarg_names, generator_fn=generate_assert_datemath_eval_equals_test)

    @classmethod
    def gen_explicit_rounding(cls):
        test_name = "test_explicit_rounding"
        arg_names = ["given", "expected"]
        kwarg_names = ["tzinfo", "units_round"]
        args_kwargs_it = [
            ("2014-11-18||/y", "2014-01-01", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/y", "2014-12-31T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-01-01T00:00:00.001||/y", "2014-01-01T00:00:00.000", None, datemath.UNITS_ROUND_DOWN),

            # rounding should also take into account time zone
            ("2014-11-18||/y", "2013-12-31T23:00:00.000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/y", "2014-12-31T22:59:59.999000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_UP_MILLIS),

            ("2014-11-18||/M", "2014-11-01", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-01||/M", "2014-11-01", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-01||/M", "2014-11-30T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),

            ("2014-11-18||/M", "2014-10-31T23:00:00.000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_DOWN),

            ("2014-11-18T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14||/w", "2014-11-23T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-17T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-19T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-20T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-21T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-22T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-23T14||/w", "2014-11-17", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/w", "2014-11-23T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18||/w", "2014-11-16T23:00:00.000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/w", "2014-11-17T01:00:00.000Z", timezone(timedelta(hours=-1)), datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/w", "2014-11-16T23:00:00.000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/w", "2014-11-23T22:59:59.999000Z", timezone(timedelta(hours=1)), datemath.UNITS_ROUND_UP_MILLIS),
            #("2014-07-22||/w", "2014-07-20T22:00:00.000Z", 0, false, ZoneId.of("CET")); # TODO CET with DST straddling.

            ("2014-11-18T14||/d", "2014-11-18", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14||/d", "2014-11-18T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18||/d", "2014-11-18", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18||/d", "2014-11-18T23:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),

            ("2014-11-18T14:27||/h", "2014-11-18T14", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27||/h", "2014-11-18T14:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18T14||/H", "2014-11-18T14", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14||/H", "2014-11-18T14:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18T14:27||/h", "2014-11-18T14", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27||/h", "2014-11-18T14:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18T14||/H", "2014-11-18T14", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14||/H", "2014-11-18T14:59:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),

            ("2014-11-18T14:27:32||/m", "2014-11-18T14:27", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27:32||/m", "2014-11-18T14:27:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18T14:27||/m", "2014-11-18T14:27", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27||/m", "2014-11-18T14:27:59.999000", None, datemath.UNITS_ROUND_UP_MILLIS),

            ("2014-11-18T14:27:32.123||/s", "2014-11-18T14:27:32", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27:32.123||/s", "2014-11-18T14:27:32.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
            ("2014-11-18T14:27:32||/s", "2014-11-18T14:27:32", None, datemath.UNITS_ROUND_DOWN),
            ("2014-11-18T14:27:32||/s", "2014-11-18T14:27:32.999000", None, datemath.UNITS_ROUND_UP_MILLIS),
        ]

        cls.generate_tests_from_iter(test_name, args_kwargs_it, arg_names, kwarg_names, generator_fn=generate_assert_datemath_eval_equals_test)


    # Test Exceptions
    @classmethod
    def gen_illegal_math_format(cls):
        test_name = "test_illegal_math_format"
        arg_names = ["given", "expected_exception"]
        args_it = [
            ("2014-11-18||*5", ValueError("operator * at position 12 in 2014-11-18||*5 not supported. valid operators: +, -, /")),
            ("2014-11-18||/2m", ValueError("unit 2 at position 13 in 2014-11-18||/2m not supported in rounding operation. valid units: {}".format(', '.join(datemath.UNITS_DELTA_DEFAULT.keys())))),
            ("2014-11-18||+2a", ValueError("unit a at position 14 in 2014-11-18||+2a not supported in arithmetic operation. valid units: {}".format(', '.join(datemath.UNITS_DELTA_DEFAULT.keys())))),
            ("2014-11-18||+12", ValueError("truncated input whilst parsing number - expected character at position 15 in 2014-11-18||+12, instead reached end of string")),
            ("2014-11-18||-", ValueError("truncated input whilst parsing number - expected character at position 13 in 2014-11-18||-, instead reached end of string")),
        ]

        cls.generate_tests_from_iter(test_name, args_it, arg_names, generator_fn=generate_assert_datemath_parse_exceptions_test)

DateMathTests.generate_shim_tests()
