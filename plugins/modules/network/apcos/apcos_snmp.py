#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_snmp
author: "Matt Haught (@haught)"
short_description: Manage snmp configuration on APC OS devices.
description:
  - This module provides declarative management of APC snmp
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v1.4.2.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  enable:
    description:
      - Global SNMPv1 enable.
    type: bool
  index:
    description:
      - Index of SNMPv1 user.
    type: int
    choices: [1, 2, 3, 4]
  community:
    description:
      - SNMPv1 community name.
    type: str
  accesstype:
    description:
      - SNMP access enable for index.
    type: str
    choices: ['disabled', 'read', 'write', 'writeplus']
  accessaddress:
    description:
      - SNMPv1 NMS IP/CIDR address for index.
    type: str
'''

EXAMPLES = """
- name: Set snmp name
  haught.apcos.apcos_snmp:
    index: 1
    community: "public"
    accesstype: "read"
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - snmp -c1 public
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
    parse_config_section,
)

SOURCE = "snmp"


def build_commands(module):
    commands = []
    config = {}
    config['config'] = parse_config(config=get_config(module, source=SOURCE))
    config['access'] = parse_config_section(
        config=get_config(module, source=SOURCE),
        section='Access Control Summary:',
        index=module.params['index'],
        indexName='Access Control #')
    if module.params['enable'] is not None:
        if config['config']['snmpv1'].lower() == "disabled" and module.params['enable'] is True:
            commands.append(SOURCE + ' -S enable')
        elif config['config']['snmpv1'].lower() == "enabled" and module.params['enable'] is False:
            commands.append(SOURCE + ' -S disable')
    if module.params['community'] and module.params['index']:
        if config['access']['community'] != module.params['community']:
            commands.append(SOURCE + ' -c' + str(module.params['index']) + ' ' + module.params['community'])
    if module.params['accesstype'] and module.params['index']:
        if config['access']['accesstype'] != module.params['accesstype']:
            commands.append(SOURCE + ' -a' + str(module.params['index']) + ' ' + module.params['accesstype'])
    if module.params['accessaddress'] and module.params['index']:
        if config['access']['address'] != module.params['accessaddress']:
            commands.append(SOURCE + ' -n' + str(module.params['index']) + ' ' + module.params['accessaddress'])
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        enable=dict(type='bool'),
        index=dict(type='int', choices=[1, 2, 3, 4]),
        community=dict(type='str'),
        accesstype=dict(type='str', choices=['disabled', 'read', 'write', 'writeplus']),
        accessaddress=dict(type='str')
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_by={
            'community': 'index',
            'accesstype': 'index',
            'accessaddress': 'index',
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
