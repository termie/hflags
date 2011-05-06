# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest

import hflags


FLAGS = hflags.FLAGS
hflags.DEFINE_string('flags_unittest', 'foo', 'for testing purposes only')


class FlagsTestCase(unittest.TestCase):

    def setUp(self):
        super(FlagsTestCase, self).setUp()
        self.FLAGS = hflags.FlagValues()
        self.global_FLAGS = hflags.FLAGS

    def test_define(self):
        self.assert_('string' not in self.FLAGS)
        self.assert_('int' not in self.FLAGS)
        self.assert_('false' not in self.FLAGS)
        self.assert_('true' not in self.FLAGS)

        hflags.DEFINE_string('string', 'default', 'desc',
                             flag_values=self.FLAGS)
        hflags.DEFINE_integer('int', 1, 'desc', flag_values=self.FLAGS)
        hflags.DEFINE_bool('false', False, 'desc', flag_values=self.FLAGS)
        hflags.DEFINE_bool('true', True, 'desc', flag_values=self.FLAGS)

        self.assert_(self.FLAGS['string'])
        self.assert_(self.FLAGS['int'])
        self.assert_(self.FLAGS['false'])
        self.assert_(self.FLAGS['true'])
        self.assertEqual(self.FLAGS.string, 'default')
        self.assertEqual(self.FLAGS.int, 1)
        self.assertEqual(self.FLAGS.false, False)
        self.assertEqual(self.FLAGS.true, True)

        argv = ['flags_test',
                '--string', 'foo',
                '--int', '2',
                '--false',
                '--notrue']

        self.FLAGS(argv)
        self.assertEqual(self.FLAGS.string, 'foo')
        self.assertEqual(self.FLAGS.int, 2)
        self.assertEqual(self.FLAGS.false, True)
        self.assertEqual(self.FLAGS.true, False)

    def test_declare(self):
        self.assert_('answer' not in self.global_FLAGS)
        hflags.DECLARE('answer', 'tests.declare_flags')
        self.assert_('answer' in self.global_FLAGS)
        self.assertEqual(self.global_FLAGS.answer, 42)

        # Make sure we don't overwrite anything
        self.global_FLAGS.answer = 256
        self.assertEqual(self.global_FLAGS.answer, 256)
        hflags.DECLARE('answer', 'tests.declare_flags')
        self.assertEqual(self.global_FLAGS.answer, 256)

    def test_runtime_and_unknown_flags(self):
        self.assert_('runtime_answer' not in self.global_FLAGS)

        argv = ['flags_test', '--runtime_answer=60', 'extra_arg']
        args = self.global_FLAGS(argv)
        self.assertEqual(len(args), 2)
        self.assertEqual(args[1], 'extra_arg')

        self.assert_('runtime_answer' not in self.global_FLAGS)

        import tests.runtime_flags

        self.assert_('runtime_answer' in self.global_FLAGS)
        self.assertEqual(self.global_FLAGS.runtime_answer, 60)
