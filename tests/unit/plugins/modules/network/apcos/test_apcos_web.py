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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_web
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosWebModule(TestApcosModule):

    module = apcos_web

    def setUp(self):
        super(TestApcosWebModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_web.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_web.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosWebModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_web.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_web_set_http_enable(self):
        set_module_args({'enablehttp': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -h enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_web_enable_http_unchanged(self):
        set_module_args({'enablehttp': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_web_set_https_disable(self):
        set_module_args({'enablehttps': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -s disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_web_enable_https_unchanged(self):
        set_module_args({'enablehttps': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_http_port(self):
        set_module_args({'httpport': 5001})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -ph 5001'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_http_port_unchanged(self):
        set_module_args({'httpport': 80})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_https_port(self):
        set_module_args({'httpsport': 5002})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -ps 5002'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_https_port_unchanged(self):
        set_module_args({'httpsport': 443})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_https_proto(self):
        set_module_args({'httpsproto': 'TLS1.1'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -mp TLS1.1'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_https_proto_unchanged(self):
        set_module_args({'httpsproto': 'TLS1.2'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_web_set_limitedstatus_enable(self):
        set_module_args({'limitedstatus': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -lsp enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_web_enable_limitedstatus_unchanged(self):
        set_module_args({'limitedstatus': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_web_set_limitedstatusdefault_enable(self):
        set_module_args({'limitedstatusdefault': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -lsd enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_web_enable_limitedstatus_unchanged(self):
        set_module_args({'limitedstatusdefault': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_tls_cipher_suite(self):
        set_module_args({'tls12ciphersuite': 2})
        result = self.execute_module(changed=True)
        expected_commands = [
            'web -cs 2'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_tls_cipher_suite_unchanged(self):
        set_module_args({'tls12ciphersuite': 4})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
