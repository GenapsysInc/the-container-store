"""Extension for a JSON directive allowing inclusion of specific portions of JSON files based on a pointer"""

import json
import os

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
import jsonpointer


def flag(opt: str | None) -> bool:
    """Parse flag option from string or None into boolean

    :param opt: The option being parsed
    :return: The corresponding boolean flag
    """
    if not opt or opt.lower() in {"true", "yes"}:
        return True

    return False


class CompactListJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that tries to put elements of lists with only literals on fewer lines

    Modified from https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92

    If the list is small enough you will end up with:

    ::

        {
            "key": [1, 2, 3, 4, 5]
        }

    otherwise, something like:

    ::

        {
            "key": [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 16, 17,
                ...
            ]
        }
    """

    # Container datatypes include primitives or other containers
    CONTAINER_TYPES = (list, tuple, dict)

    # Maximum width of a line for elements in a list
    MAX_WIDTH = 70

    # Used to create indents during formatting
    INDENTATION_CHAR = " "

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o) -> str:
        """Encode JSON object *o*"""
        # If we decided to not have any indentation, just short circuit here
        if not self.indent:
            return json.dumps(o)

        if isinstance(o, (list, tuple)):
            if self._primitives_only(o):
                return self._encode_list(o)

            self.indentation_level += 1
            output = [self.indent_str + self.encode(elem) for elem in o]
            self.indentation_level -= 1
            return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"

        if isinstance(o, dict):
            if o:
                self.indentation_level += 1
                output = [self.indent_str + f"{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()]
                self.indentation_level -= 1
                return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"

            return "{}"

        return json.dumps(o)

    def _encode_list(self, l: list) -> str:
        """Encodes a list - assumes the list only contains primitives"""
        whole_list_dumped = json.dumps(l)
        elements_in_l = len(l)

        encoded = "["

        # If the list needs to be on multiple lines based on length
        if len(whole_list_dumped) > self.MAX_WIDTH:
            self.indentation_level += 1
            encoded += "\n" + self.indent_str

        cur_line_length = 0

        for index, item in enumerate(l):
            dumped_item = json.dumps(item)

            # Ignore if handling the first element of the list which shouldn't reset anything
            if index != 0:
                # Go to new line if current elem puts us over self.MAX_WIDTH
                # Add 1 for possibly added "," at the end of line
                if cur_line_length + len(dumped_item) + 1 > self.MAX_WIDTH:
                    cur_line_length = 0
                    encoded += "\n" + self.indent_str
                # We are still on the same line, add a space before the next element
                else:
                    encoded += " "

            encoded += dumped_item
            cur_line_length += len(dumped_item)

            if index != elements_in_l - 1:
                encoded += ","
                cur_line_length += 1

        # Close out the list indent change if we put it on multiple lines
        if len(whole_list_dumped) > self.MAX_WIDTH:
            self.indentation_level -= 1
            encoded += "\n" + self.indent_str

        encoded += "]"

        return encoded

    def _primitives_only(self, o: list | tuple) -> bool:
        return not any(isinstance(elem, self.CONTAINER_TYPES) for elem in o)

    @property
    def indent_str(self) -> str:
        return self.INDENTATION_CHAR * (self.indentation_level * self.indent)


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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Allows accession of allowable options as attributes, with automatic default setting
        for option in self.option_spec:
            setattr(self, option, self.options.get(option, self.defaults[option]))

    @property
    def defaults(self) -> dict:
        """Default values for allowable options"""
        return {
            "caption": "",
            "indent": 4,
            "keep_key": False
        }

    def run(self) -> list[nodes.Node]:
        json_path, pointer = self.parse_path_arg(self.arguments[0])

        final_key = None

        if self.keep_key:
            try:
                # Note: if a single key is given, pointer will be the empty string
                pointer, final_key = pointer.rsplit("/", maxsplit=1)
            except ValueError:
                pass

        try:
            with open(json_path, 'r', encoding="utf-8") as json_fh:
                json_content = json.load(json_fh)
        except FileNotFoundError as e:
            raise self.warning(f"Could not find JSON file {json_path}") from e
        except json.decoder.JSONDecodeError as e:
            raise self.warning(f"Could not parse JSON file, got error: {e}") from e

        try:
            json_subsection = jsonpointer.resolve_pointer(json_content, pointer)

            if final_key is not None:
                if isinstance(json_subsection, dict):
                    json_subsection = {final_key: jsonpointer.resolve_pointer(json_subsection, f"/{final_key}")}
                else:
                    json_subsection = jsonpointer.resolve_pointer(json_subsection, f"/{final_key}")
        except jsonpointer.JsonPointerException as e:
            raise self.warning(f"Invalid pointer for given JSON file, got: {e}") from e

        output_content = json.dumps(json_subsection, indent=self.indent, cls=CompactListJSONEncoder)

        output_node = nodes.literal_block(output_content, output_content)

        if self.caption:
            output_node = self.add_caption(self.caption, output_node)

        return [output_node]

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
        split_path_arg = path_arg.rsplit("#", maxsplit=1)

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
