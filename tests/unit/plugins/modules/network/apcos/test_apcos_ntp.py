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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_ntp
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosNtpModule(TestApcosModule):

    module = apcos_ntp

    def setUp(self):
        super(TestApcosNtpModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_ntp.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_ntp.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosNtpModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_ntp.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_ntp_set_disable(self):
        set_module_args({'enable': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'ntp -e disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_ntp_enable_unchanged(self):
        set_module_args({'enable': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_ntp_primaryserver(self):
        set_module_args({'primaryserver': '10.10.10.11'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'ntp -p 10.10.10.11'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_ntp_primaryserve_unchanged(self):
        set_module_args({'primaryserver': '10.10.10.10'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_ntp_secondaryserver(self):
        set_module_args({'secondaryserver': '10.22.10.11'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'ntp -s 10.22.10.11'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_ntp_secondaryserver_unchanged(self):
        set_module_args({'secondaryserver': '10.22.10.10'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_ntp_overridemanual_disable(self):
        set_module_args({'overridemanual': False})
        result = self.execute_module(changed=True)
        expected_commands = [
            'ntp -OM disable'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_ntp_overridemanual_unchanged(self):
        set_module_args({'overridemanual': True})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
