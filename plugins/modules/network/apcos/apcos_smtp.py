#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_smtp
author: "Matt Haught (@haught)"
short_description: Manage SMTP configuration on APC OS devices.
description:
  - This module provides declarative management of APC SMTP
    configuration on APC UPS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v2.2.1.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  from_address:
    description:
      - From address.
    type: str
  server:
    description:
      - SMTP server.
    type: str
  port:
    description:
      - Port SMTP uses.
    type: int
  auth:
    description:
      - SMTP authentication enabled.
    type: bool
  user:
    description:
      - Username for auth.
    type: str
  password:
    description:
      - Password for auth.
    type: str
  encryption:
    description:
      - Encryption option for connection.
    type: str
    choices: ['none', 'ifavail', 'always', 'implicit']
  require_certificate:
    description:
      - Require certificate for connection.
    type: bool
  certificate:
    description:
      - Certificate file name.
    type: str
  forcepwchange:
    description:
      - Force a password change
    type: bool
    default: False
'''

EXAMPLES = """
- name: Set SMTP server
  haught.apcos.apcos_smtp:
    server: smtp.example.com
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - smtp -a enable
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
)

SOURCE = "smtp"


def build_commands(module):
    commands = []
    config = parse_config(get_config(module, source=SOURCE))
    if module.params['from_address'] is not None:
        if config['from'] != module.params['from_address']:
            commands.append(SOURCE + ' -f ' + module.params['from_address'])
    if module.params['server'] is not None:
        if config['server'] != module.params['server']:
            commands.append(SOURCE + ' -s ' + module.params['server'])
    if module.params['port'] is not None:
        if config['port'] != str(module.params['port']):
            commands.append(SOURCE + ' -p ' + str(module.params['port']))
    if module.params['auth'] is not None:
        if config['auth'].lower() == "disabled" and module.params['auth'] is True:
            commands.append(SOURCE + ' -a enable')
        elif config['auth'].lower() == "enabled" and module.params['auth'] is False:
            commands.append(SOURCE + ' -a disable')
    if module.params['user'] is not None:
        if config['user'] != module.params['user']:
            commands.append(SOURCE + ' -u ' + module.params['user'])
    if module.params['password'] is not None:
        if config['password'] == '<not set>' or module.params['forcepwchange'] is True:
            commands.append(SOURCE + ' -w ' + module.params['password'])
    if module.params['encryption'] is not None:
        if config['encryption'] != module.params['encryption']:
            commands.append(SOURCE + ' -e ' + module.params['encryption'])
    if module.params['require_certificate'] is not None:
        if config['req.cert'].lower() == "disabled" and module.params['require_certificate'] is True:
            commands.append(SOURCE + ' -c enable')
        elif config['req.cert'].lower() == "enabled" and module.params['require_certificate'] is False:
            commands.append(SOURCE + ' -c disable')
    if module.params['certificate'] is not None:
        if config['certfile'] != module.params['certificate']:
            commands.append(SOURCE + ' -i ' + module.params['certificate'])
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        from_address=dict(type='str'),
        server=dict(type='str'),
        port=dict(type='int'),
        auth=dict(type='bool'),
        user=dict(type='str'),
        password=dict(type='str', no_log=True),
        encryption=dict(type='str', choices=['none', 'ifavail', 'always', 'implicit']),
        require_certificate=dict(type='bool'),
        certificate=dict(type='str'),
        forcepwchange=dict(type='bool', default=False)
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
