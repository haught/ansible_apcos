#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: apcos_dns
author: "Matt Haught (@haught)"
short_description: Manage dns configuration on APC OS devices.
description:
  - This module provides declarative management of APC UPS dns
    configuration on APC OS NMC systems.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v1.4.2.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  primaryserver:
    description:
      - Set the primary DNS server.
    type: str
  secondaryserver:
    description:
      - Set the secondary DNS server.
    type: str
  hostname:
    description:
      - Set the host name
    type: str
  domainname:
    description:
      - Set the domain name
    type: str
  domainnameipv6:
    description:
      - Set the domain name IPv6.
    type: str
  systemnamesync:
    description:
      - Synchronizes the system name and the hostname.
    type: bool
  overridemanual:
    description:
      - Override the manual DNS.
    type: bool
'''

EXAMPLES = """
- name: Set dns name
  haught.apcos.apcos_dns:
    primarydns: "1.1.1.1"

- name: Set two dns settings
  haught.apcos.apcos_dns:
    primarydns: "1.1.1.1"
    secondarydns: "4.4.4.4"
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - dns -n ups001
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import (
    load_config,
    get_config,
    parse_config,
)

SOURCE = "dns"


def build_commands(module):
    commands = []
    config = parse_config(get_config(module, source=SOURCE))
    if module.params['primaryserver']:
        if config['primarydnsserver'] != module.params['primaryserver']:
            commands.append(SOURCE + ' -p ' + module.params['primaryserver'])
    if module.params['secondaryserver']:
        if config['secondarydnsserver'] != module.params['secondaryserver']:
            commands.append(SOURCE + ' -s ' + module.params['secondaryserver'])
    if module.params['domainname']:
        if config['domainname'] != module.params['domainname']:
            commands.append(SOURCE + ' -d ' + module.params['domainname'])
    if module.params['domainnameipv6']:
        if config['domainnameipv6'] != module.params['domainnameipv6']:
            commands.append(SOURCE + ' -n ' + module.params['domainnameipv6'])
    if module.params['hostname']:
        if config['hostname'] != module.params['hostname']:
            commands.append(SOURCE + ' -h ' + module.params['hostname'])
    if module.params['systemnamesync'] is not None:
        if config['systemnamesync'].lower() == "disabled" and module.params['systemnamesync'] is True:
            commands.append(SOURCE + ' -y enable')
        elif config['systemnamesync'].lower() == "enabled" and module.params['systemnamesync'] is False:
            commands.append(SOURCE + ' -y disable')
    if module.params['overridemanual'] is not None:
        if config['overridemanualdnssettings'].lower() == "disabled" and module.params['overridemanual'] is True:
            commands.append(SOURCE + ' -OM enable')
        elif config['overridemanualdnssettings'].lower() == "enabled" and module.params['overridemanual'] is False:
            commands.append(SOURCE + ' -OM disable')
    return commands


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        primaryserver=dict(type='str'),
        secondaryserver=dict(type='str'),
        domainname=dict(type='str'),
        domainnameipv6=dict(type='str'),
        hostname=dict(type='str'),
        systemnamesync=dict(type='bool'),
        overridemanual=dict(type='bool')
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
