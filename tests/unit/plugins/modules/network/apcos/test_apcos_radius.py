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
from ansible_collections.haught.apcos.plugins.modules.network.apcos import apcos_radius
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.haught.apcos.tests.unit.plugins.modules.network.apcos.apcos_module import TestApcosModule, load_fixture


class TestApcosRadiusModule(TestApcosModule):

    module = apcos_radius

    def setUp(self):
        super(TestApcosRadiusModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_radius.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.haught.apcos.plugins.modules.network.apcos.apcos_radius.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestApcosRadiusModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        config_file = 'apcos_config_radius.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_apcos_radius_set_access(self):
        set_module_args({'access': 'radius'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -a radius'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_set_access_both(self):
        set_module_args({'access': 'radiuslocal'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -a radiuslocal'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_access_unchanged(self):
        set_module_args({'access': 'local'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_primaryserver(self):
        set_module_args({'primaryserver': '10.11.11.12'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -p1 10.11.11.12'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_primaryserver_unchanged(self):
        set_module_args({'primaryserver': '10.11.11.11'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_primarysecret_serverchange(self):
        set_module_args({'primarysecret': 'test123', 'primaryserver': '10.1.1.10'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -p1 10.1.1.10',
            'radius -s1 test123'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_primarysecret_forced(self):
        set_module_args({'primarysecret': 'test123', 'forcepwchange': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -s1 test123'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_primarysecret_not_forced(self):
        set_module_args({'primarysecret': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_primaryport(self):
        set_module_args({'primaryport': 1645})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -o1 1645'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_primaryport_unchanged(self):
        set_module_args({'primaryport': 1812})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_primarytimeout(self):
        set_module_args({'primarytimeout': 10})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -t1 10'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_primarytimeout_unchanged(self):
        set_module_args({'primarytimeout': 30})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_secondaryserver(self):
        set_module_args({'secondaryserver': '10.11.11.14'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -p2 10.11.11.14'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_secondaryserver_unchanged(self):
        set_module_args({'secondaryserver': '0.0.0.0'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_secondarysecret_serverchange(self):
        set_module_args({'secondarysecret': 'test123', 'secondaryserver': '10.1.1.10'})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -p2 10.1.1.10',
            'radius -s2 test123'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_secondarysecret_forced(self):
        set_module_args({'secondarysecret': 'test123', 'forcepwchange': True})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -s2 test123'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_secondarysecret_not_forced(self):
        set_module_args({'secondarysecret': 'test'})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_secondaryport(self):
        set_module_args({'secondaryport': 1645})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -o2 1645'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_secondaryport_unchanged(self):
        set_module_args({'secondaryport': 1812})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)

    def test_apcos_radius_secondarytimeout(self):
        set_module_args({'secondarytimeout': 12})
        result = self.execute_module(changed=True)
        expected_commands = [
            'radius -t2 12'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_apcos_radius_secondarytimeout_unchanged(self):
        set_module_args({'secondarytimeout': 5})
        result = self.execute_module(changed=False)
        self.assertEqual(result['changed'], False)
