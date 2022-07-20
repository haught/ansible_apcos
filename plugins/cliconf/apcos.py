#
# (c) 2017 Red Hat Inc.
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
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
author: Matt Haught (@haught)
name: apcos
short_description: Use apcos cliconf to run command on APC OS devices
description:
  - This apcos plugin provides low level abstraction apis for
    sending and receiving CLI commands from APC OS devices.
'''

import re
import json

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible.plugins.cliconf import CliconfBase


class Cliconf(CliconfBase):

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'apcos'
        reply = self.get('about')
        data = to_text(reply, errors='surrogate_or_strict').strip()

        match = re.search(r'Hardware Revision:\s+(\S+)', data)
        if match:
            device_info['network_os_version'] = match.group(1)

        match = re.search(r'^Model Number:\s+(\S+)', data, re.M)
        if match:
            device_info['network_os_model'] = match.group(1)

        reply = self.get('dns')
        data = to_text(reply, errors='surrogate_or_strict').strip()

        match = re.search(r'^Host Name:\s+(\S+)', data, re.M)
        if match:
            device_info['network_os_hostname'] = match.group(1)

        return device_info

    def get_config(self, source='date', flags=None):
        if source not in ('boot', 'cipher', 'console', 'date', 'dns', 'eapol',
                          'email', 'firewall', 'ftp', 'ntp', 'portspeed', 'prompt',
                          'radius', 'session', 'smtp', 'snmp', 'snmptrap', 'snmpv3',
                          'system', 'tcpip', 'tcpip6', 'user', 'userdflt', 'web'):
            raise ValueError("fetching configuration from %s is not supported" % source)
        cmd = source

        flags = [] if flags is None else flags
        cmd += ' '.join(flags)
        cmd = cmd.strip()

        return self.send_command(cmd)

    def edit_config(self, command):
        for cmd in to_list(command):
            if isinstance(cmd, dict):
                command = cmd['command']
                prompt = cmd['prompt']
                answer = cmd['answer']
                newline = cmd.get('newline', True)
            else:
                command = cmd
                prompt = None
                answer = None
                newline = True
                self.send_command(command=command, prompt=prompt, answer=answer, sendonly=False, newline=newline)

    def get(self, command, prompt=None, answer=None, sendonly=False, newline=True, check_all=False):
        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, newline=newline, check_all=check_all)

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        return json.dumps(result)
