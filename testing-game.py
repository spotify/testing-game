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

# !/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess


def find_xctest_tests(blame_lines, names, source, xctestsuperclasses):
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
                blame_info = blame_line[blame_line.find('(')+1:]
                blame_info = blame_info[:blame_info.find(')')]
                blame_components = blame_info.split()
                name_components = blame_components[:len(blame_components)-4]
                name = ' '.join(name_components)
                name_count = names.get(name, 0)
                names[name] = name_count + 1
    return names


def find_java_tests(blame_lines, names, source):
    next_is_test = False
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if next_is_test or blame_code_nospaces.startswith('publicvoidtest'):
            blame_info = blame_line[:separator]
            name = blame_info[blame_info.find('<')+1:blame_info.find('@')]
            name_count = names.get(name, 0)
            names[name] = name_count + 1
            next_is_test = False
        else:
            next_is_test = blame_code_nospaces.startswith('@Test')
    return names


def find_boost_tests(blame_lines, names, source):
    test_cases = ['BOOST_AUTO_TEST_CASE', 'BOOST_FIXTURE_TEST_CASE']
    for blame_line in blame_lines:
        contains_test_case = False
        for test_case in test_cases:
            contains_test_case |= blame_line.find(test_case) != -1
            if contains_test_case:
                break
        if contains_test_case:
            blame_info = blame_line[blame_line.find('(')+1:]
            blame_info = blame_info[:blame_info.find(')')]
            blame_components = blame_info.split()
            name_components = blame_components[:len(blame_components)-4]
            name = ' '.join(name_components)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
    return names


def find_nose_tests(blame_lines, names, source):
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if blame_code_nospaces.startswith('deftest_'):
            blame_info = blame_line[:separator]
            name = blame_info[blame_info.find('<')+1:blame_info.find('@')]
            name_count = names.get(name, 0)
            names[name] = name_count + 1
    return names


def find_git_status(directory, xctestsuperclasses):
    names = {}
    objc_extensions = ['.m', '.mm']
    java_extensions = ['.java']
    cpp_extensions = ['.cpp']
    python_extensions = ['.py']
    valid_extensions = objc_extensions
    valid_extensions.extend(java_extensions)
    valid_extensions.extend(cpp_extensions)
    valid_extensions.extend(python_extensions)
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
                            names = find_xctest_tests(blame_lines,
                                                      names,
                                                      source,
                                                      xctestsuperclasses)
                        elif fileextension in java_extensions:
                            names = find_java_tests(blame_lines, names, source)
                        elif fileextension in cpp_extensions:
                            names = find_boost_tests(blame_lines,
                                                     names,
                                                     source)
                        elif fileextension in python_extensions:
                            names = find_nose_tests(blame_lines, names, source)
                except:
                    'Could not open file: ' + absfile
    return names

if __name__ == "__main__":
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
    args = parser.parse_args()
    names = find_git_status(args.directory, args.xctestsuperclasses.split(','))
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
