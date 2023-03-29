# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2016 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import re
from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible.module_utils.connection import Connection


def get_connection(module):
    """Get switch connection

    Creates reusable SSH connection to the switch described in a given module.

    Args:
        module: A valid AnsibleModule instance.

    Returns:
        An instance of `ansible.module_utils.connection.Connection` with a
        connection to the switch described in the provided module.

    Raises:
        AnsibleConnectionFailure: An error occurred connecting to the device
    """
    if hasattr(module, 'apcos_connection'):
        return module.apcos_connection

    capabilities = get_capabilities(module)
    network_api = capabilities.get('network_api')
    if network_api == 'cliconf':
        module.apcos_connection = Connection(module._socket_path)
    else:
        module.fail_json(msg='Invalid connection type %s' % network_api)

    return module.apcos_connection


def get_capabilities(module):
    """Get switch capabilities

    Collects and returns a python object with the switch capabilities.

    Args:
        module: A valid AnsibleModule instance.

    Returns:
        A dictionary containing the switch capabilities.
    """
    if hasattr(module, 'apcos_capabilities'):
        return module.apcos_capabilities

    capabilities = Connection(module._socket_path).get_capabilities()
    module.apcos_capabilities = json.loads(capabilities)
    return module.apcos_capabilities


def run_commands(module, commands):
    """Run command list against connection.

    Get new or previously used connection and send commands to it one at a time,
    collecting response.

    Args:
        module: A valid AnsibleModule instance.
        commands: Iterable of command strings.

    Returns:
        A list of output strings.
    """
    responses = list()
    connection = get_connection(module)

    for cmd in to_list(commands):
        command = cmd['command']
        prompt = cmd['prompt']
        answer = cmd['answer']

        out = connection.get(command, prompt, answer)

        try:
            out = to_text(out, errors='surrogate_or_strict')
        except UnicodeError:
            module.fail_json(msg=u'Failed to decode output from %s: %s' % (cmd, to_text(out)))

        responses.append(out)

    return responses


def get_config(module, source="date"):
    """Get switch configuration

    Gets the described device's current configuration. If a configuration has
    already been retrieved it will return the previously obtained configuration.

    Args:
        module: A valid AnsibleModule instance.

    Returns:
        A string containing the configuration.
    """
    if not hasattr(module, 'device_configs'):
        module.device_configs = {}
    elif module.device_configs != {}:
        return module.device_configs

    connection = get_connection(module)
    out = connection.get_config(source=source)
    cfg = to_text(out, errors='surrogate_then_replace').strip()
    module.device_configs = cfg
    return cfg


def load_config(module, commands):
    """Apply a list of commands to a device.

    Given a list of commands apply them to the device to modify the
    configuration in bulk.

    Args:
        module: A valid AnsibleModule instance.
        commands: Iterable of command strings.

    Returns:
        None
    """
    connection = get_connection(module)
    connection.edit_config(commands)


def parse_config(config):
    parsed = {}
    for line in config.split('\n'):
        line_parts = re.match(r'^(.+):\s+(.+)$', line)
        if hasattr(line_parts, 'group'):
            key = line_parts.group(1).replace(" ", "").lower()
            value = line_parts.group(2) if re.search(r'\S', line_parts.group(2)) else ""
            parsed[key] = value
    return parsed


def parse_config_section(config, section, index=None, indexName="Index"):
    found_section = False
    found_index = None
    section_values = []
    for line in config.split('\n'):
        if found_section is True:
            if re.match(r'^\S', line):
                break
            if re.match(r'^\s+(.+)', line):
                section_values.append(line)
        if line == section:
            found_section = True
    subsection = {}
    for line in section_values:
        if index is not None:
            index_search = re.match(r'\s+?' + indexName + r':\s+(.+)', line)
            if hasattr(index_search, 'group'):
                found_index = int(index_search.group(1))
                subsection[found_index] = []
            if found_index is not None:
                subsection[found_index].append(line)
    if index is not None:
        for key in subsection:
            subsection[key] = parse_config("\n".join(subsection[key]))
        if index in subsection.keys():
            return subsection[index]
    return parse_config("\n".join(section_values))
