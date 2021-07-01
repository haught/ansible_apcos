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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_snmpv3
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosSnmpv3Module(TestApcosModule):

    module = apcos_snmpv3

    def setUp(self):
        super(TestApcosSnmpv3Module, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_snmpv3.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_snmpv3.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosSnmpv3Module, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_snmpv3.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_snmpv3_set_disable(self):
        set_module_args({'enable': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -S disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_enable_unchanged(self):
        set_module_args({'enable': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_username(self):
        set_module_args({'index': 1, 'username': 'janedoe'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -u1 janedoe'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_username_unchanged(self):
        set_module_args({'index': 1, 'username': 'lab-user'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_authprotocol(self):
        set_module_args({'index': 1, 'authprotocol': 'MD5'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -ap1 MD5'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_authprotocol_unchanged(self):
        set_module_args({'index': 1, 'authprotocol': 'SHA'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_authphrase_forced(self):
        set_module_args({'index': 1, 'authphrase': 'password', 'forcepwchange': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -a1 password'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_authphrase_notforced(self):
        set_module_args({'index': 1, 'authphrase': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_authphrase_namechange(self):
        set_module_args({'index': 1, 'username': 'test', 'authphrase': 'password'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -u1 test',
            'snmpv3 -a1 password'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_authphrase_notnamechange(self):
        set_module_args({'index': 1, 'username': 'lab-user', 'authphrase': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_privprotocol(self):
        set_module_args({'index': 1, 'privprotocol': 'DES'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -pp1 DES'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_privprotocol_unchanged(self):
        set_module_args({'index': 1, 'privprotocol': 'AES'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_privphrase_forced(self):
        set_module_args({'index': 1, 'privphrase': 'password', 'forcepwchange': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -c1 password'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_privphrase_notforced(self):
        set_module_args({'index': 1, 'privphrase': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_privphrase_namechange(self):
        set_module_args({'index': 1, 'username': 'test', 'privphrase': 'password'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -u1 test',
            'snmpv3 -c1 password'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_privphrase_notnamechange(self):
        set_module_args({'index': 1, 'username': 'lab-user', 'privphrase': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_disable_access(self):
        set_module_args({'index': 1, 'access': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -ac1 disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_access_unchanged(self):
        set_module_args({'index': 1, 'access': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_accessusername(self):
        set_module_args({'index': 1, 'accessusername': 'janedoe'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -au1 janedoe'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_accessusername_unchanged(self):
        set_module_args({'index': 1, 'accessusername': 'lab-user'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_snmpv3_set_accessaddress(self):
        set_module_args({'index': 1, 'accessaddress': '10.11.12.14'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'snmpv3 -n1 10.11.12.14'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_snmpv3_accessaddress_unchanged(self):
        set_module_args({'index': 1, 'accessaddress': '10.11.12.13'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
