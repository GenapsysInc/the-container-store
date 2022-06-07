"""Build sphinx docs"""

__author__ = "Aaron Berlin"

import argparse
import os
import shlex
import subprocess
from typing import List

BUILDER_DIR = "_builder"
BUILDER_HTML = f"{BUILDER_DIR}/html"
BUILDER_CONF = f"{BUILDER_DIR}/confluence"
CONFLUENCE_CONF_PATH = "/scripts/confluence.conf"
DOCUMENTATION_BASE = "docs"


def build_api_docs(code_dir: str, out_dir: str = DOCUMENTATION_BASE) -> None:
    """Runs sphinx-apidocs on the directories to produce rst docs

    :param code_dir: Directory to document
    :param out_dir: Directory to write documentation to
    """

    api_output_path = out_dir + "/_" + code_dir

    print(f"Building API docs for {code_dir} and writing them to {api_output_path}")
    api_builder_cmd = ["sphinx-apidoc", "-fM", "-o", api_output_path, "-e", code_dir, "--implicit-namespaces"]
    subprocess.run(api_builder_cmd, check=True)


def _get_sphinx_builder(builder: str, build_dir: str, conf_dir: str = None, user_options: list = None,
                        builder_override_options: dict = None) -> list:

    sphinx_build_cmd = ["sphinx-build", "-b", builder]

    if conf_dir:
        sphinx_build_cmd.extend(["-c", conf_dir])

    if user_options:
        sphinx_build_cmd.extend(user_options)

    if builder_override_options:
        for k, v in builder_override_options.items():
            sphinx_build_cmd.extend(["-D", f"{k}={v}"])

    sphinx_build_cmd.extend([DOCUMENTATION_BASE, build_dir])

    return sphinx_build_cmd


def _build_docs(builder: str, build_dir: str, conf_dir: str = None, user_options: list = None,
                builder_options: dict = None) -> None:

    build_cmd = _get_sphinx_builder(builder, build_dir, conf_dir, user_options=user_options,
                                    builder_override_options=builder_options)
    subprocess.run(build_cmd, check=True)


def build_html(build_dir: str, user_options: list = None, version: str = None) -> None:
    """Render the documents to html

    :param build_dir: Directory to write documentation to
    :param user_options: Extra builder options specified by the user
    :param version: Version to display in rendered html docs, defaults to whatever is in the conf.py
    """
    html_options = {}

    if version:
        html_options.update({"version": version})
        html_options.update({"release": ".".join(version.split(".")[0:2])})

    _build_docs("html", build_dir, user_options=user_options, builder_options=html_options)


def build_confluence(build_dir: str, user_options: list = None, secret: str = None, publish: bool = False) -> None:
    """Render the documents for Confluence publication

    :param build_dir: Directory to write documentation to
    :param user_options: Extra build options
    :param secret: Confluence secret needed to publish
    :param publish: If true publish to confluence; if false render docs but do not publish
    """
    confluence_options = {}
    if secret:
        confluence_options.update({"confluence_server_pass": secret})

    # Note: sphinx struggles with booleans passed as options through -D so only write the option when it is True
    if publish:
        confluence_options.update({"confluence_publish": publish})

    config_dir = "confluence"
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    write_custom_config([CONFLUENCE_CONF_PATH, DOCUMENTATION_BASE + "/conf.py"], config_dir)
    _build_docs("confluence", build_dir=build_dir, conf_dir=config_dir, user_options=user_options,
                builder_options=confluence_options)


def write_custom_config(input_files: List[str], output_directory: str) -> None:
    """Write a custom config for a specific builder.

    :param output_directory: Directory to write the custom conf file
    :param input_files: Configuration files. Order matters, file are written in order provided
    """

    with open(output_directory + "/conf.py", 'w') as custom_config:
        for in_file in input_files:
            with open(in_file, 'r') as input_config:
                custom_config.write(input_config.read())


def parse_args():
    """Parse commandline args"""

    parser = argparse.ArgumentParser(description="Build Sphinx docs for a repository")

    parser.add_argument("-c", "--confluence", required=False, default=False, action='store_true',
                        help="Build and publish to confluence")
    parser.add_argument("-m", "--html", required=False, default=False, action='store_true',
                        help="Build and publish to html")
    parser.add_argument("-d", "--dirs", required=False, nargs="+", help="Code directories for API documentation")
    parser.add_argument("-w", "--warn_as_error", required=False, default=False, action='store_true',
                        help="Raise warnings as errors")
    parser.add_argument("-u", "--user_build_options", required=False, default=None, help="User specified build options")
    parser.add_argument("-s", "--confluence_secret", required=False, help="Publish to Confluence API token")
    parser.add_argument("-p", "--confluence_publish", required=False, default=False, action='store_true',
                        help="Publish to Confluence")
    parser.add_argument("-v", "--version", required=False, help="Version string for doc build")

    return parser.parse_args()


def main(args):

    if args.dirs:
        for directory in args.dirs:
            build_api_docs(directory)

    if not os.path.exists(BUILDER_DIR):
        os.mkdir(BUILDER_DIR)

    user_options = []
    if args.warn_as_error:
        user_options.extend(["-W", "--keep-going"])

    if args.user_build_options:
        user_options.extend(shlex.split(args.user_build_options))

    if args.html:
        build_html(BUILDER_HTML, user_options,  version=args.version)

    if args.confluence:
        build_confluence(BUILDER_CONF, user_options, args.confluence_secret, args.confluence_publish)


if __name__ == "__main__":
    opts = parse_args()
    main(opts)
