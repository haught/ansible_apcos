#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_snmpv3
author: "Matt Haught (@haught)"
short_description: Manage snmpv3 configuration on APC OS devices.
description:
  - This module provides declarative management of APC snmpv3
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v1.4.2.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  enable:
    description:
      - Global SNMPv3 enable.
    type: bool
  index:
    description:
      - Index of SNMPv3 user.
    type: int
    choices: [1, 2, 3, 4]
  username:
    description:
      - SNMPv3 user name for index.
    type: str
  authprotocol:
    description:
      - SNMPv3 authentication protocol for index.
    type: str
    choices: ['SHA', 'MD5', 'NONE']
  authphrase:
    description:
      - SNMPv3 authentication phrase for index.
    type: str
  privprotocol:
    description:
      - SNMPv3 privacy protocol for index.
    type: str
    choices: ['AES', 'DES', 'NONE']
  privphrase:
    description:
      - SNMPv3 privacy phrase for index.
    type: str
  access:
    description:
      - SNMPv3 access enable for index.
    type: bool
  accessusername:
    description:
      - SNMPv3 access user name for index.
    type: str
  accessaddress:
    description:
      - SNMPv3 NMS IP/CIDR address for index.
    type: str
  forcepwchange:
    description:
      - Force a auth/priv phrase change
    type: bool
    default: False
'''

EXAMPLES = """
- name: Set snmpv3 name
  haught.apcos.apcos_snmpv3:
    primarysnmpv3: "1.1.1.1"

- name: Set two snmpv3 settings
  haught.apcos.apcos_snmpv3:
    primarysnmpv3: "1.1.1.1"
    secondarysnmpv3: "4.4.4.4"
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - snmpv3 -n ups001
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config_section,
)

SOURCE = "snmpv3"


def build_commands(module):
    commands = []
    config = {}
    config['config'] = parse_config_section(get_config(module, source=SOURCE), 'SNMPv3 Configuration')
    config['user'] = parse_config_section(get_config(module, source=SOURCE), 'SNMPv3 User Profiles', module.params['index'])
    config['access'] = parse_config_section(get_config(module, source=SOURCE), 'SNMPv3 Access Control', module.params['index'])
    if module.params['enable'] is not None:
        if config['config']['snmpv3'].lower() == "disabled" and module.params['enable'] is True:
            commands.append(SOURCE + ' -S enable')
        elif config['config']['snmpv3'].lower() == "enabled" and module.params['enable'] is False:
            commands.append(SOURCE + ' -S disable')
    if module.params['authprotocol'] and module.params['index']:
        if config['user']['authentication'] != module.params['authprotocol']:
            commands.append(SOURCE + ' -ap' + str(module.params['index']) + ' ' + module.params['authprotocol'])
    if module.params['privprotocol'] and module.params['index']:
        if config['user']['encryption'] != module.params['privprotocol']:
            commands.append(SOURCE + ' -pp' + str(module.params['index']) + ' ' + module.params['privprotocol'])
    if (module.params['username'] or module.params['forcepwchange'] is True) and module.params['index']:
        if module.params['username'] and config['user']['username'] != module.params['username']:
            commands.append(SOURCE + ' -u' + str(module.params['index']) + ' ' + module.params['username'])
        # set password if username changes or set to force
        if (module.params['username'] and config['user']['username'] != module.params['username']) or module.params['forcepwchange'] is True:
            if module.params['authphrase'] and module.params['index']:
                commands.append(SOURCE + ' -a' + str(module.params['index']) + ' ' + module.params['authphrase'])
            if module.params['privphrase'] and module.params['index']:
                commands.append(SOURCE + ' -c' + str(module.params['index']) + ' ' + module.params['privphrase'])
    if module.params['accessusername'] and module.params['index']:
        if config['access']['username'] != module.params['accessusername']:
            commands.append(SOURCE + ' -au' + str(module.params['index']) + ' ' + module.params['accessusername'])
    if module.params['access'] is not None and module.params['index']:
        if config['access']['access'].lower() == "disabled" and module.params['access'] is True:
            commands.append(SOURCE + ' -ac' + str(module.params['index']) + ' enable')
        elif config['access']['access'].lower() == "enabled" and module.params['access'] is False:
            commands.append(SOURCE + ' -ac' + str(module.params['index']) + ' disable')
    if module.params['accessaddress'] and module.params['index']:
        if config['access']['nmsip/hostname'] != module.params['accessaddress']:
            commands.append(SOURCE + ' -n' + str(module.params['index']) + ' ' + module.params['accessaddress'])
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        enable=dict(type='bool'),
        index=dict(type='int', choices=[1, 2, 3, 4]),
        username=dict(type='str'),
        authphrase=dict(type='str', no_log=True),
        authprotocol=dict(type='str', choices=['SHA', 'MD5', 'NONE']),
        privphrase=dict(type='str', no_log=True),
        privprotocol=dict(type='str', choices=['AES', 'DES', 'NONE']),
        access=dict(type='bool'),
        accessusername=dict(type='str'),
        accessaddress=dict(type='str'),
        forcepwchange=dict(type='bool', default=False)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_by={
            'username': 'index',
            'authphrase': 'index',
            'authprotocol': 'index',
            'privphrase': 'index',
            'privprotocol': 'index',
            'access': 'index',
            'accessusername': 'index',
            'accessaddress': 'index'
        },
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
