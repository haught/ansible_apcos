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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_smtp
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosSmtpModule(TestApcosModule):

    module = apcos_smtp

    def setUp(self):
        super(TestApcosSmtpModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_smtp.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_smtp.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosSmtpModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_smtp.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_smtp_set_from(self):
        set_module_args({'from_address': 'user@example.com'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -f user@example.com'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_from_unchanged(self):
        set_module_args({'from_address': 'address@example.com'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_set_server(self):
        set_module_args({'server': 'mail.example.net'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -s mail.example.net'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_server_unchanged(self):
        set_module_args({'server': 'mail.example.com'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_port(self):
        set_module_args({'port': 587})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -p 587'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_port_unchanged(self):
        set_module_args({'port': 25})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_auth_set_enable(self):
        set_module_args({'auth': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -a enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_auth_unchanged(self):
        set_module_args({'auth': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_set_username(self):
        set_module_args({'user': 'angryspud'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -u angryspud'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_username_unchanged(self):
        set_module_args({'user': 'User'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)


    def test_apcos_smtp_set_encryption_ifavail(self):
        set_module_args({'encryption': 'ifavail'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -e ifavail'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_set_encryption_always(self):
        set_module_args({'encryption': 'always'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -e always'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_set_encryption_implicit(self):
        set_module_args({'encryption': 'implicit'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -e implicit'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_encryption_unchanged(self):
        set_module_args({'encryption': 'none'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_set_reqcert(self):
        set_module_args({'require_certificate': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -c enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_reqcert_unchanged(self):
        set_module_args({'require_certificate': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_smtp_set_certfile(self):
        set_module_args({'certificate': 'test.cer'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'smtp -i test.cer'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_smtp_certfile_unchanged(self):
        set_module_args({'certificate': '<n/a>'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

