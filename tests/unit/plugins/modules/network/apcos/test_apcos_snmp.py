#
# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_snmp
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosSnmpModule(TestApcosModule):

    module = apcos_snmp

    def setUp(self):
        super(TestApcosSnmpModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_snmp.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_snmp.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosSnmpModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_snmp.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_snmp_set_enable(self):
        set_module_args({'enable': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmp -S enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmp_enable_unchanged(self):
        set_module_args({'enable': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmp_set_community(self):
        set_module_args({'index': 1, 'community': 'public_test2'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmp -c1 public_test2'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmp_community_unchanged(self):
        set_module_args({'index': 1, 'community': 'public_test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmp_set_accesstype(self):
        set_module_args({'index': 1, 'accesstype': 'write'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmp -a1 write'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmp_accesstype_unchanged(self):
        set_module_args({'index': 1, 'accesstype': 'read'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmp_set_accessaddress(self):
        set_module_args({'index': 1, 'accessaddress': '10.11.12.14'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmp -n1 10.11.12.14'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmp_accessaddress_unchanged(self):
        set_module_args({'index': 1, 'accessaddress': '10.11.12.13'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
