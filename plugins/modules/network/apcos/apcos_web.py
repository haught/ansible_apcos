#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_web
author: "Matt Haught (@haught)"
short_description: Manage web configuration on APC OS devices.
description:
  - This module provides declarative management of APC web
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v2.2.1.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  enablehttp:
    description:
      - http enable.
    type: bool
  enablehttps:
    description:
      - https enable.
    type: bool
  httpport:
    description:
      - Port http uses.
    type: int
  httpsport:
    description:
      - Port https uses.
    type: int
  httpsproto:
    description:
      - Minimum https protocol
    type: str
    choices: ['TLS1.1', 'TLS1.2']
  limitedstatus:
    description:
      - Limited status page enabled
    type: bool
  limitedstatusdefault:
    description:
      - Limited status page enabled as default
    type: bool
  tls12ciphersuite:
    description:
      - TLS1.2 Cipher Suite Filter
    type: int
    choices: [0, 1, 2, 3, 4]

'''

EXAMPLES = """
- name: Enable HTTPS
  haught.apcos.apcos_web:
    httpsenable: true
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - web -s enable
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
)

SOURCE = "web"


def build_commands(module):
    commands = []
    config = parse_config(get_config(module, source=SOURCE))
    if module.params['enablehttp'] is not None:
        if config['http'].lower() == "disabled" and module.params['enablehttp'] is True:
            commands.append(SOURCE + ' -h enable')
        elif config['http'].lower() == "enabled" and module.params['enablehttp'] is False:
            commands.append(SOURCE + ' -h disable')
    if module.params['enablehttps'] is not None:
        if config['https'].lower() == "disabled" and module.params['enablehttps'] is True:
            commands.append(SOURCE + ' -s enable')
        elif config['https'].lower() == "enabled" and module.params['enablehttps'] is False:
            commands.append(SOURCE + ' -s disable')
    if module.params['httpport'] is not None:
        if config['httpport'] != str(module.params['httpport']):
            commands.append(SOURCE + ' -ph ' + str(module.params['httpport']))
    if module.params['httpsport'] is not None:
        if config['httpsport'] != str(module.params['httpsport']):
            commands.append(SOURCE + ' -ps ' + str(module.params['httpsport']))
    if module.params['httpsproto'] is not None:
        if config['minimumprotocol'] != module.params['httpsproto']:
            commands.append(SOURCE + ' -mp ' + module.params['httpsproto'])
    if module.params['limitedstatus'] is not None:
        if config['limitedstatusaccess'].lower() == "disabled" and module.params['limitedstatus'] is True:
            commands.append(SOURCE + ' -lsp enable')
        elif config['limitedstatusaccess'].lower() == "enabled" and module.params['limitedstatus'] is False:
            commands.append(SOURCE + ' -lsp disable')
    if module.params['limitedstatusdefault'] is not None:
        if config['lim.statuspageused'].lower() == "disabled" and module.params['limitedstatusdefault'] is True:
            commands.append(SOURCE + ' -lsd enable')
        elif config['lim.statuspageused'].lower() == "enabled" and module.params['limitedstatusdefault'] is False:
            commands.append(SOURCE + ' -lsd disable')
    if module.params['tls12ciphersuite'] is not None:
        if config['tls1.2ciphersuitefilter'] != str(module.params['tls12ciphersuite']):
            commands.append(SOURCE + ' -cs ' + str(module.params['tls12ciphersuite']))
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        enablehttp=dict(type='bool'),
        enablehttps=dict(type='bool'),
        httpport=dict(type='int'),
        httpsport=dict(type='int'),
        httpsproto=dict(type='str', choices=['TLS1.1', 'TLS1.2']),
        limitedstatus=dict(type='bool'),
        limitedstatusdefault=dict(type='bool'),
        tls12ciphersuite=dict(type='int', choices=[0, 1, 2, 3, 4])
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
