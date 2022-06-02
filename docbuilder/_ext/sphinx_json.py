"""Extension for a JSON directive allowing inclusion of specific portions of JSON files based on a pointer"""

import json
import os
from typing import Dict, List, Union

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
import jsonpointer


def flag(opt: Union[str, None]) -> bool:
    """Parse flag option from string or None into boolean

    :param opt: The option being parsed
    :return: The corresponding boolean flag
    """
    if not opt or opt.lower() in {"true", "yes"}:
        return True

    return False


class SphinxJson(Directive):
    """Directive for including a JSON file or a specific subsection of a JSON file

    Example::

        .. json:: ../../../eureka/module_dependencies.json#/sensor_id
            :indent: 2
            :caption: Sensor ID Module Dependencies
            :keep_key:
    """

    required_arguments = 1
    has_content = True
    option_spec = {
        "caption": str,
        "indent": int,
        "keep_key": flag
    }

    def __init__(self, name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
        super().__init__(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine)

        # Allows accession of allowable options as attributes, with automatic default setting
        for option in self.option_spec:
            setattr(self, option, self.options.get(option, self.defaults[option]))

    @property
    def defaults(self) -> Dict:
        """Default values for allowable options"""
        return {
            "caption": "",
            "indent": 4,
            "keep_key": False
        }

    def run(self) -> List[nodes.Node]:
        json_path, pointer = self.parse_path_arg(self.arguments[0])

        with open(json_path, 'r', encoding="utf-8") as json_fh:
            json_content = json.load(json_fh)

        json_subsection = jsonpointer.resolve_pointer(json_content, pointer)

        if pointer and self.keep_key:
            key = pointer.split("/")[-1]
            json_subsection = {key: json_subsection}

        output_json = json.dumps(json_subsection, indent=self.indent)

        json_node = nodes.literal_block(output_json, output_json)

        if self.caption:
            json_node = self.add_caption(self.caption, json_node)

        return [json_node]

    def add_caption(self, caption: str, node_to_update: nodes.Node) -> nodes.Node:
        """Adds a caption string to the given Node

        Taken from https://github.com/sphinx-doc/sphinx/blob/5.x/sphinx/directives/code.py#L68

        :param caption: The caption to add
        :param node_to_update: The Node to add the caption to
        :return: The updated Node
        """
        container_node = nodes.container('', literal_block=True, classes=['literal-block-wrapper'])

        parsed = nodes.Element()

        self.state.nested_parse(StringList([caption], source=''), self.content_offset, parsed)

        caption_node = nodes.caption(parsed[0].rawsource, '', *parsed[0].children)

        caption_node.source = node_to_update.source
        caption_node.line = node_to_update.line
        container_node += caption_node
        container_node += node_to_update

        return container_node

    def parse_path_arg(self, path_arg: str) -> (str, str):
        """Parse directive path argument into JSON file path and pointer, if pointer is given

        :param path_arg: The directive's path argument
        :return: Tuple of JSON file path and pointer, with pointer set to the empty string if not given
        """
        split_path_arg = path_arg.split("#")

        if len(split_path_arg) == 1:
            split_path_arg.append("")

        file_path, pointer = split_path_arg

        if not os.path.isabs(file_path):
            file_path = os.path.join(os.path.dirname(self.state.document.current_source), file_path)

        return file_path, pointer


def setup(app):
    app.add_directive("json", SphinxJson)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
