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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_dns
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosDnsModule(TestApcosModule):

    module = apcos_dns

    def setUp(self):
        super(TestApcosDnsModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_dns.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_dns.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosDnsModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_dns.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_dns_primaryserver_set(self):
        set_module_args({'primaryserver': '8.8.8.8'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -p 8.8.8.8'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_primaryserver_unchanged(self):
        set_module_args({'primaryserver': '1.1.1.1'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_secondaryserver_set(self):
        set_module_args({'secondaryserver': '1.0.0.1'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -s 1.0.0.1'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_secondaryserver_unchanged(self):
        set_module_args({'secondaryserver': '8.8.4.4'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_domainname_set(self):
        set_module_args({'domainname': 'example.com'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -d example.com'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_domainname_unchanged(self):
        set_module_args({'domainname': 'example.net'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_domainnameipv6_set(self):
        set_module_args({'domainnameipv6': 'example.com'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -n example.com'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_domainnameipv6_unchanged(self):
        set_module_args({'domainnameipv6': 'example.net'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_hostname_set(self):
        set_module_args({'hostname': 'test'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -h test'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_hostname_unchanged(self):
        set_module_args({'hostname': 'apctest2-1'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_systemnamesync_enable(self):
        set_module_args({'systemnamesync': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -y enable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_systemnamesync_unchanged(self):
        set_module_args({'systemnamesync': False})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_dns_overridemanual_disable(self):
        set_module_args({'overridemanual': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'dns -OM disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_dns_overridemanual_unchanged(self):
        set_module_args({'overridemanual': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
