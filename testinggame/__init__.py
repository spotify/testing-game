# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
 * Copyright (c) 2015 Spotify AB.
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
'''
import argparse
import os
import subprocess


def _find_name_from_blame(blame_line):
    """
    Finds the name of the committer of code given a blame line from git

    Args:
        blame_line: A string from the git output of the blame for a file.
    Returns:
        The username as a string of the user to blame
    """
    blame_info = blame_line[blame_line.find('(')+1:]
    blame_info = blame_info[:blame_info.find(')')]
    blame_components = blame_info.split()
    name_components = blame_components[:len(blame_components)-4]
    return ' '.join(name_components)


def _find_xctest_tests(blame_lines, names, source, xctestsuperclasses):
    """
    Finds the number of XCTest cases per user.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
        source: A string containing the raw source code for the file.
        xctestsuperclasses: An array containing alternative superclasses for
        the xctest framework.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    xctest_identifiers = ['XCTestCase']
    xctest_identifiers.extend(xctestsuperclasses)
    contains_test_case = False
    for xctest_identifier in xctest_identifiers:
        contains_test_case |= source.find(xctest_identifier) != -1
        if contains_test_case:
            break
    if contains_test_case:
        for blame_line in blame_lines:
            if blame_line.replace(' ', '').find('-(void)test') != -1:
                name = _find_name_from_blame(blame_line)
                name_count = names.get(name, 0)
                names[name] = name_count + 1
    return names


def _find_java_tests(blame_lines, names):
    """
    Finds the number of Java test cases per user. This will find tests both
    with the @Test annotation and the standard test methods.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    next_is_test = False
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if next_is_test or blame_code_nospaces.startswith('publicvoidtest'):
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
            next_is_test = False
        else:
            next_is_test = blame_code_nospaces.startswith('@Test')
    return names

def _find_cs_tests(blame_lines, names):
    """
    Finds the number of C# test cases per user. This will find nUnit tests
    with the [Test] attribute

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    next_is_test = False
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if next_is_test and blame_code_nospaces.find('{') != -1:
            next_is_test = False
        elif next_is_test and blame_code_nospaces.startswith('public'):
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
            next_is_test = False
        else:
            next_is_test = next_is_test or blame_code_nospaces.startswith('[Test]')
    return names

def _find_boost_tests(blame_lines, names):
    """
    Finds the number of Boost test cases per user.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    test_cases = ['BOOST_AUTO_TEST_CASE', 'BOOST_FIXTURE_TEST_CASE']
    for blame_line in blame_lines:
        contains_test_case = False
        for test_case in test_cases:
            contains_test_case |= blame_line.find(test_case) != -1
            if contains_test_case:
                break
        if contains_test_case:
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
    return names

def _find_python_tests(blame_lines, names, source):
    """
    Finds the number of python test cases per user.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if blame_code_nospaces.startswith('deftest'):
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
    return names

def _find_php_tests(blame_lines, names):
    """
    Finds the number of php test cases per user. Does not consider data providers

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if blame_code_nospaces.startswith('publicfunctiontest'):
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
    return names


def _find_git_status(directory, xctestsuperclasses):
    """
    Finds the number of tests per user within a given directory. Note that this
    will only work on the root git subdirectory, submodules will not be
    counted.

    Args:
        directory: The path to the directory to scan.
        xctestsuperclasses: An array of strings containing names for xctest
        superclasses.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.

    >>> _find_git_status('tests', 'SPTTestCase')
    {'Will Sackfield': 6}
    """
    names = {}
    objc_extensions = ['.m', '.mm']
    java_extensions = ['.java']
    cpp_extensions = ['.cpp', '.mm']
    python_extensions = ['.py']
    cs_extensions = ['.cs']
    php_extensions = ['.php']
    valid_extensions = objc_extensions
    valid_extensions.extend(java_extensions)
    valid_extensions.extend(cpp_extensions)
    valid_extensions.extend(python_extensions)
    valid_extensions.extend(cs_extensions)
    valid_extensions.extend(php_extensions)
    for root, dirs, files in os.walk(directory):
        for name in files:
            filename, fileextension = os.path.splitext(name)
            absfile = os.path.join(root, name)
            if fileextension in valid_extensions:
                try:
                    with open(absfile) as sourcefile:
                        source = sourcefile.read()
                        p = subprocess.Popen(['git', 'blame', absfile],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        blame_lines = out.splitlines()
                        if fileextension in objc_extensions:
                            names = _find_xctest_tests(blame_lines,
                                                       names,
                                                       source,
                                                       xctestsuperclasses)
                        if fileextension in java_extensions:
                            names = _find_java_tests(blame_lines,
                                                     names)
                        if fileextension in cpp_extensions:
                            names = _find_boost_tests(blame_lines,
                                                      names)
                        if fileextension in python_extensions:
                            names = _find_python_tests(blame_lines,
                                                       names,
                                                       source)
                        if fileextension in cs_extensions:
                            names = _find_cs_tests(blame_lines,
                                                   names)
                        if fileextension in php_extensions:
                           names = _find_php_tests(blame_lines,
                                                      names)
                except:
                    'Could not open file: ' + absfile
    return names


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help='The directory to search for files in',
                        required=False,
                        default=os.getcwd())
    parser.add_argument('-x',
                        '--xctestsuperclasses',
                        help='A comma separated list of XCTest super classes',
                        required=False,
                        default='')
    parser.add_argument('-v',
                        '--version',
                        help='Prints the version of testing game',
                        required=False,
                        default=False,
                        action='store_true')
    args = parser.parse_args()
    if args.version:
        print 'testing game version 1.0.0'
        return
    xctest_superclasses = args.xctestsuperclasses.replace(' ', '').split(',')
    names = _find_git_status(args.directory, xctest_superclasses)
    total_tests = 0
    for name in names:
        total_tests += names[name]
    print "Total Tests: %(t)d" % {'t': total_tests}
    print "-------------------------------------------"
    sorted_list = sorted(names.items(), key=lambda x: x[1], reverse=True)
    for t in sorted_list:
        percentage = (float(t[1]) / float(total_tests)) * 100.0
        t_index = sorted_list.index(t) + 1
        print "%(i)d. %(n)s, %(t)d (%(p).2f%%)" % {'i': t_index,
                                                   'n': t[0],
                                                   't': t[1],
                                                   'p': percentage}

if __name__ == "__main__":
    _main()
