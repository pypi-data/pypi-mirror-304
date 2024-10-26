# test/__init__.py
# Part of ‘changelog-chug’, a parser for project Change Log documents.
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Test suite for this code base. """

import builtins
import contextlib
import unittest.mock

import testtools


def make_expected_error_context(
        testcase,
        *,
        expected_error_attr_name='expected_error',
        expected_error_message_regex_attr_name='expected_error_message_regex',
):
    """ Make a context for the `testcase.expected_error`, if any.

        :param testcase: The `TestCase` instance to inspect.
        :param expected_error_attr_name: Name (text) of an attribute of
            `testcase` to inspect; the value is the exception type to expect.
        :param expected_error_message_regex_attr_name: Name (text) of an
            attribute of `testcase` to inspect; the value is the regex pattern
            to expect match in the exception object caught.
        :return: The Python context to wrap test calls.

        If the `testcase.expected_error` attribute is bound, return a
        `testtools.ExpectedException` for that exception type; otherwise,
        return a `contextlib.nullcontext`.

        If the `testcase.expected_error` attribute is bound and the
        `testcase.expected_error_message_regex` attribute is bound, use that
        value as the `value_re` specification of regular expression pattern
        that must match the exception's message.
        """
    context = contextlib.nullcontext()
    if hasattr(testcase, expected_error_attr_name):
        expected_error_message_regex = getattr(
            testcase,
            expected_error_message_regex_attr_name,
            None)
        context = testtools.ExpectedException(
            getattr(testcase, expected_error_attr_name),
            value_re=expected_error_message_regex,
        )
    return context


def mock_builtin_open_for_fake_files(testcase, *, fake_file_content_by_path):
    """ Mock builtin `open` during `testcase`, for specific fake files.

        :param testcase: The test case during which to mock `open`.
        :param fake_file_content_by_path: Mapping of
            `{file_path: fake_file_content}`.

        Create fake files (`io.StringIO`) containing each `fake_file_content`.
        Wrap the `builtins.open` function such that, for the specified
        `file_path` only, a specific mock `open` function will be called,
        that returns the corresponding fake file; for any unspecified path,
        the original `builtins.open` will be called as normal.
        """
    testcase.mock_open_by_path = {
        file_path: unittest.mock.mock_open(read_data=fake_file_content)
        for (file_path, fake_file_content)
        in fake_file_content_by_path.items()}

    open_orig = builtins.open

    def fake_open(file, *args, **kwargs):
        """ Wrapper for builtin `open`, faking for specific paths. """
        open_func = (
            testcase.mock_open_by_path[file]
            if file in testcase.mock_open_by_path
            else open_orig)
        return open_func(file, *args, **kwargs)

    testcase.open_patcher = unittest.mock.patch.object(
        builtins, 'open', side_effect=fake_open)
    testcase.open_patcher.start()
    testcase.addCleanup(testcase.open_patcher.stop)


# Copyright © 2008–2024 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; version 3 or, at your option, a later version.
# No warranty expressed or implied. See the file ‘LICENSE.AGPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
