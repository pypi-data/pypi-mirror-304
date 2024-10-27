from datetime import datetime, timedelta, timezone

from esdateutil import dateformat
from tests import utils

default_parser = dateformat.DateFormat()

def generate_assert_dateformat_eval_equals_test(*args, **kwargs):
    def test_fn(self):
        self.assert_dateformat_eval_equals(*args, **kwargs)
    return test_fn

def generate_assert_dateformat_parse_exceptions_test(*args, **kwargs):
    def test_fn(self):
        self.assert_dateformat_parse_exceptions(*args, **kwargs)
    return test_fn

class DateFormatTests(utils.TestShim):
    def assert_dateformat_eval_equals(self, given_str, expected_datetime, parser=default_parser):
        self.assertEqual(parser.parse(given_str), expected_datetime)

    def assert_dateformat_parse_exceptions(self, given_str, expected_exception_list, parser=default_parser):
        expected_exception = ValueError("Unable to parse date string {}: {}".format(given_str, expected_exception_list))

        try:
            parser.parse(given_str)
        except type(expected_exception) as e:
            self.assertEqual(e.args, expected_exception.args)
        else:
            raise RuntimeError("Did not receive expected exception when parsing {}".format(given_str))

    @classmethod
    def gen_strict_date_optional_time(cls):
        test_name = "test_strict_date_optional_time"
        arg_names = ["given_str", "expected_datetime"]
        args_it = [
            ("2024",                           datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04",                        datetime(year=2024, month=4, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11",                     datetime(year=2024, month=4, day=11, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14",                  datetime(year=2024, month=4, day=11, hour=14, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02",               datetime(year=2024, month=4, day=11, hour=14, minute=2, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02:29",            datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02:29.123",        datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=None)),
            ("2024-04-11T14:02:29.123456",     datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=None)),
            ("2024-04-11T14:02:29.123456789Z", datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=timezone.utc)),
            ("2024-04-11T14:02:29.1234+05:30", datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=timezone(timedelta(hours=5, minutes=30)))),
            ("2024-04-11T14:02:29Z",           datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=0, tzinfo=timezone.utc)),
            ("2024-04-11T14:02-01:00",         datetime(year=2024, month=4, day=11, hour=14, minute=2, second=0, microsecond=0, tzinfo=timezone(timedelta(hours=-1, minutes=0)))),
            ("2024-04-11T14Z",                 datetime(year=2024, month=4, day=11, hour=14, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)),
        ]
        kwargs_static = {
            "parser": dateformat.DateFormat("strict_date_optional_time")
        }

        cls.generate_tests_from_iter(test_name, args_it, arg_names, kwargs_static=kwargs_static, generator_fn=generate_assert_dateformat_eval_equals_test)

    # TODO Test actual special date optional time stuff that wouldn't work in strict
    @classmethod
    def gen_date_optional_time(cls):
        test_name = "test_date_optional_time"
        arg_names = ["given_str", "expected_datetime"]
        args_it = [
            ("2024",                           datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04",                        datetime(year=2024, month=4, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11",                     datetime(year=2024, month=4, day=11, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14",                  datetime(year=2024, month=4, day=11, hour=14, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02",               datetime(year=2024, month=4, day=11, hour=14, minute=2, second=0, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02:29",            datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=0, tzinfo=None)),
            ("2024-04-11T14:02:29.123",        datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=None)),
            ("2024-04-11T14:02:29.123456",     datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=None)),
            ("2024-04-11T14:02:29.123456789Z", datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=timezone.utc)),
            ("2024-04-11T14:02:29.1234+05:30", datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=123000, tzinfo=timezone(timedelta(hours=5, minutes=30)))),
            ("2024-04-11T14:02:29Z",           datetime(year=2024, month=4, day=11, hour=14, minute=2, second=29, microsecond=0, tzinfo=timezone.utc)),
            ("2024-04-11T14:02-01:00",         datetime(year=2024, month=4, day=11, hour=14, minute=2, second=0, microsecond=0, tzinfo=timezone(timedelta(hours=-1, minutes=0)))),
            # Below doesn't work in non-strict date formats, because ES. We test for this in test_date_optional_time_hour_timezone_exception.
            #("2024-04-11T14Z",                  datetime(year=2024, month=4, day=11, hour=14, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)),
        ]
        kwargs_static = {
            "parser": dateformat.DateFormat("date_optional_time")
        }

        cls.generate_tests_from_iter(test_name, args_it, arg_names, kwargs_static=kwargs_static, generator_fn=generate_assert_dateformat_eval_equals_test)

    def test_date_optional_time_hour_timezone_exception(self):
        parser = dateformat.DateFormat("date_optional_time")
        s = "2024-04-11T14Z"
        es = [ValueError("Elasticsearch has a cool bug where strict_date_optional_time allows a timezone offset after the hour value of a time, but date_optional_time does not. String: {}".format(s))]
        self.assert_dateformat_parse_exceptions(s, es, parser=parser)

    @classmethod
    def gen_default_date_parser(cls):
        test_name = "test_default_date_parser"
        arg_names = ["given_str", "expected_datetime"]
        args_it = [
            ("2024",          datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)),
            ("1726861366756", datetime(year=2024, month=9, day=20, hour=20, minute=42, second=46, microsecond=756000, tzinfo=None)),
            # NOTE In Python 3.3, some numbers are scuffed due to floating point nonsense. Below check fails, above check succeeds.
            #("1726861366757", datetime(year=2024, month=9, day=20, hour=20, minute=42, second=46, microsecond=757000, tzinfo=None)),
        ]

        cls.generate_tests_from_iter(test_name, args_it, arg_names, generator_fn=generate_assert_dateformat_eval_equals_test)

    @classmethod
    def gen_custom_date_string_parser(cls):
        df = dateformat.DateFormat
        test_name = "test_custom_date_string_parser"
        arg_names = ["given_str", "expected_datetime"]
        kwarg_names = ["parser"]
        args_kwargs_it = [
            ("2024-01-24",               datetime(year=2024, month=1, day=24, hour=0, minute=0, second=0, tzinfo=timezone.utc), df("%Y-%m-%d", tzinfo=timezone.utc)),
            ("2024-01-24T13:05:12",      datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=timezone.utc), df("%Y-%m-%dT%H:%M:%S", tzinfo=timezone.utc)),
            ("2024-01-24T13:05:12-0000", datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=timezone.utc), df("%Y-%m-%dT%H:%M:%S%z")),
            ("2024-01-24T13:05:12+0530", datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=timezone(timedelta(hours=5, minutes=30))), df("%Y-%m-%dT%H:%M:%S%z", tzinfo=timezone.utc)),
        ]

        cls.generate_tests_from_iter(test_name, args_kwargs_it, arg_names, kwarg_names, generator_fn=generate_assert_dateformat_eval_equals_test)

    def test_init_bad_format_type_exception(self):
        bad_val = 999999
        fmt = ["strict_date_optional_time", bad_val]
        expected_exception = TypeError("DateFormat cannot init - expected fmt to be string separated by separator ({}) or list of functions and/or strings. Instead got {} containing element {} of type {}".format("||", fmt, bad_val, type(bad_val)))
        try:
            dateformat.DateFormat(fmt)
        except TypeError as e:
            self.assertEqual(e.args, expected_exception.args)

    @classmethod
    def gen_explicit_timezone(cls):
        tzinfo = timezone(timedelta(hours=-3, minutes=15))
        test_name = "test_custom_date_string_parser"
        arg_names = ["given_str", "expected_datetime"]
        args_kwargs_it = [
            ("2024-01-24",                datetime(year=2024, month=1, day=24, hour=0, minute=0, second=0, tzinfo=tzinfo)),
            ("2024-01-24T13:05:12",       datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=tzinfo)),
            ("2024-01-24T13:05:12Z",      datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=timezone.utc)),
            ("2024-01-24T13:05:12-01:00", datetime(year=2024, month=1, day=24, hour=13, minute=5, second=12, tzinfo=timezone(timedelta(hours=-1)))),
            ("1726861366000",             datetime(year=2024, month=9, day=20, hour=16, minute=57, second=46, tzinfo=tzinfo)),
        ]
        kwargs_static = {
            "parser": dateformat.DateFormat(tzinfo=tzinfo)
        }

        cls.generate_tests_from_iter(test_name, args_kwargs_it, arg_names, kwargs_static=kwargs_static, generator_fn=generate_assert_dateformat_eval_equals_test)


DateFormatTests.generate_shim_tests()
