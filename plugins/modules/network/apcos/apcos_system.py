#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_system
author: "Matt Haught (@haught)"
short_description: Manage system configuration on APC OS devices.
description:
  - This module provides declarative management of APC OS system
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v1.4.2.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  name:
    description:
      - System system name of device.
    type: str
  contact:
    description:
      - Contact name for device.
    type: str
  location:
    description:
      - Location of device.
    type: str
  motd:
    description:
      - Show a custom message on the logon page of the web UI or the CLI.
    type: str
  hostnamesync:
    description:
      - Synchronize the system and the hostname.
    type: bool
    default: False
'''

EXAMPLES = """
- name: Set system name
  haught.apcos.apcos_system:
    name: "device01"

- name: Set two system settings
  haught.apcos.apcos_system:
    name: "device01"
    location: "Bldg-101"
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - system -l Bldg 101
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
)

SOURCE = "system"


def build_commands(module):
    commands = []
    config = parse_config(get_config(module, source=SOURCE))
    if module.params['name']:
        if config['name'] != module.params['name']:
            commands.append(SOURCE + ' -n ' + module.params['name'])
    if module.params['contact']:
        if config['contact'] != module.params['contact']:
            commands.append(SOURCE + ' -c ' + module.params['contact'])
    if module.params['location']:
        if config['location'] != module.params['location']:
            commands.append(SOURCE + ' -l ' + module.params['location'])
    if module.params['motd']:
        if config['message'] != module.params['motd']:
            commands.append(SOURCE + ' -m ' + module.params['motd'])
    if module.params['hostnamesync'] is not None:
        if config['hostnamesync'].lower() == "disabled" and module.params['hostnamesync'] is True:
            commands.append(SOURCE + ' -s enable')
        elif config['hostnamesync'].lower() == "enabled" and module.params['hostnamesync'] is False:
            commands.append(SOURCE + ' -s disable')
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        name=dict(type='str'),
        contact=dict(type='str'),
        location=dict(type='str'),
        motd=dict(type='str'),
        hostnamesync=dict(type='bool', default=False)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    warnings = list()

    result = {'changed': False}

    if warnings:
        result['warnings'] = warnings

    commands = build_commands(module)

    result['commands'] = commands

    if commands:
        if not module.check_mode:
            load_config(module, commands)

        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
