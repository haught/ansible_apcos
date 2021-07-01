#!/usr/bin/python
#
# Copyright: Ansible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
DOCUMENTATION = '''
---
module: apcos_command
author: "Matt Haught (@haught)"
short_description: Run commands on remote devices running APC OS
description:
  - Sends arbitrary commands to an APC UPS NMC and returns the results
    read from the device. This module includes an
    argument that will cause the module to wait for a specific condition
    before returning or timing out if the condition is not met.
notes:
  - Tested APC NMC v3 (AP9641) running APC OS v1.4.2.1
  - APC NMC v2 cards running AOS <= v6.8.2 and APC
    NMC v3 cards running AOS < v1.4.2.1 have a bug that
    stalls output and will not work with ansible
options:
  commands:
    description:
      - List of commands to send to the remote APC device over the
        configured provider. The resulting output from the command
        is returned. If the I(wait_for) argument is provided, the
        module is not returned until the condition is satisfied or
        the number of retries has expired.
      - If a command sent to the device requires answering a prompt,
        checkall and newline if multiple prompts, it is possible to pass
        a dict containing I(command), I(answer), I(prompt), I(check_all)
        and I(newline).Common answers are 'y' or "\\r" (carriage return,
        must be double quotes). See examples.
    required: true
    type: list
    elements: str
  wait_for:
    description:
      - List of conditions to evaluate against the output of the
        command. The task will wait for each condition to be true
        before moving forward. If the conditional is not true
        within the configured number of retries, the task fails.
        See examples.
    type: list
    elements: str
  match:
    description:
      - The I(match) argument is used in conjunction with the
        I(wait_for) argument to specify the match policy.  Valid
        values are C(all) or C(any).  If the value is set to C(all)
        then all conditionals in the wait_for must be satisfied.  If
        the value is set to C(any) then only one of the values must be
        satisfied.
    default: all
    choices: ['any', 'all']
    type: str
  retries:
    description:
      - Specifies the number of retries a command should by tried
        before it is considered failed. The command is run on the
        target device every retry and evaluated against the
        I(wait_for) conditions.
    default: 10
    type: int
  interval:
    description:
      - Configures the interval in seconds to wait between retries
        of the command. If the command does not pass the specified
        conditions, the interval indicates how long to wait before
        trying the command again.
    default: 1
    type: int
'''

EXAMPLES = """
tasks:
  - name: Run system on remote devices
    haught.apcos.apcos_command:
      commands: system

  - name: Run multiple commands on remote nodes
    haught.apcos.apcos_command:
      commands:
        - system
        - dns

  - name: Run multiple commands and evaluate the output
    haught.apcos.apcos_command:
      commands:
        - system
        - dns
      wait_for:
        - result[0] contains UPS01
        - result[1] contains example.net

  - name: Run command that requires answering a prompt
    haught.apcos.apcos_command:
      commands:
        - command: 'reboot'
          prompt: "Enter 'YES' to continue or <ENTER> to cancel"
          answer: "YES"
"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed
  returned: failed
  type: list
  sample: ['...', '...']
"""
import re
import time

from ansible_collections.haught.apcos.plugins.module_utils.network.apcos.apcos import run_commands
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import ComplexList
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import Conditional
from ansible.module_utils.six import string_types


__metaclass__ = type


def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).replace('\t', '    ').split('\n')
        yield item


def parse_commands(module, warnings):
    command = ComplexList(dict(
        command=dict(key=True),
        prompt=dict(),
        answer=dict()
    ), module)
    commands = command(module.params['commands'])
    for item in list(commands):
        if module.check_mode:
            disallowed_check_commands = ['bye', 'exit', 'quit', 'delete', 'format', 'clrrst',
                                         'reboot', 'logzip', 'upsfwupdate', 'resetToDef', 'ledblink']
            if (re.match(r'\S+\s\S+', item['command']) is not None) or (item['command'] in disallowed_check_commands):
                warnings.append(
                    'only show commands are supported when using check mode, not '
                    'executing `%s`' % item['command']
                )
                commands.remove(item)
    return commands


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        commands=dict(type='list', elements='str', required=True),

        wait_for=dict(type='list', elements='str'),
        match=dict(default='all', choices=['all', 'any']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    result = {'changed': False}

    warnings = list()
    commands = parse_commands(module, warnings)
    result['warnings'] = warnings

    wait_for = module.params['wait_for'] or list()
    conditionals = [Conditional(c) for c in wait_for]

    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries > 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):
            if item(responses):
                if match == 'any':
                    conditionals = list()
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update({
        'changed': False,
        'stdout': responses,
        'stdout_lines': list(to_lines(responses))
    })

    module.exit_json(**result)


if __name__ == '__main__':
    main()
