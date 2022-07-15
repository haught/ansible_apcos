#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_ftp
author: "Matt Haught (@haught)"
short_description: Manage FTP configuration on APC OS devices.
description:
  - This module provides declarative management of APC FTP
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v2.2.1.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  enable:
    description:
      - FTP enable.
    type: bool
  port:
    description:
      - Port FTP uses.
    type: int
    default: 21
'''

EXAMPLES = """
- name: Enable FTP
  haught.apcos.apcos_ftp:
    enable: true
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - ftp -S enable
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
)

SOURCE = "ftp"


def build_commands(module):
    commands = []
    config = parse_config(get_config(module, source=SOURCE))
    if module.params['enable'] is not None:
        if config['service'].lower() == "disabled" and module.params['enable'] is True:
            commands.append(SOURCE + ' -S enable')
        elif config['service'].lower() == "enabled" and module.params['enable'] is False:
            commands.append(SOURCE + ' -S disable')
    if module.params['port'] is not None:
        if config['ftpport'] != str(module.params['port']):
            commands.append(SOURCE + ' -p ' + str(module.params['port']))
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        enable=dict(type='bool'),
        port=dict(type='int')
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    warnings = list()

    result = {'changed': False}

    if warnings:
        result['warnings'] = warnings

    commands = []
    commands = build_commands(module)

    result['commands'] = commands

    if commands:
        if not module.check_mode:
            load_config(module, commands)

        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
