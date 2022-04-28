"""Build sphinx docs"""

__author__ = "Aaron Berlin"

import argparse
import os
import subprocess

BUILDER_DIR = "_builder"
CONFLUENCE_CONF_PATH = "/scripts/confluence.conf"
DOCUMENTATION_BASE = "docs"


def build_api_docs(code_dir: str, out_dir: str = DOCUMENTATION_BASE) -> None:
    """Runs sphinx-apidocs on the directories to produce rst docs

    :param code_dir: Directory to document
    :param out_dir: Directory to write documentation to
    """

    api_output_path = out_dir + "/_" + code_dir

    print(f"Building API docs for {code_dir} and writing them to {api_output_path}")
    api_builder_cmd = ["sphinx-apidoc", "-fM", "-o", api_output_path, "-e", code_dir]
    subprocess.run(api_builder_cmd)


def _get_sphinx_builder(builder: str, build_dir: str, conf_dir: str = None, warn_as_error: bool = False,
                        sphinx_options: dict = None) -> list:
    warn_opt = ""
    if warn_as_error:
        warn_opt = "-W"

    conf_opt = ""
    if conf_dir:
        conf_opt = f"-c {conf_dir}"

    options = ""
    if sphinx_options:
        for k, v in sphinx_options.items():
            options += f" -D {k}={v} "

    return ["sphinx-build", f"-M {builder}", conf_opt, warn_opt, options, DOCUMENTATION_BASE, build_dir]


def _build_docs(builder: str, build_dir: str, conf_dir: str = None, warn_as_error: bool = False,
                options: dict = None) -> None:
    build_cmd = _get_sphinx_builder(builder, build_dir, conf_dir, warn_as_error=warn_as_error, sphinx_options=options)
    os.system((' '.join(build_cmd)))


def build_html(warn_as_error: bool, build_dir: str) -> None:
    """Render the documents to html

    :param warn_as_error: Treat warnings as errors
    :param build_dir: Directory to write documentation to
    """
    _build_docs("html", build_dir, warn_as_error=warn_as_error)


def build_confluence(warn_as_error: bool, build_dir: str, secret: str, publish: bool = False) -> None:
    """Render the documents for Confluence publication

    :param warn_as_error: Treat warnings as errors
    :param build_dir: Directory to write documentation to
    :param secret: Confluence secret needed to publish
    :param publish: If true publish to confluence; if false render docs but do not publish
    """
    confluence_options = {}
    if secret:
        confluence_options.update({"confluence_server_pass": secret})

    # Note sphinx struggles with booleans passed as options through -D so only write the option when it is True
    if publish:
        confluence_options.update({"confluence_publish": publish})

    config_dir = "confluence"
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    write_custom_config([CONFLUENCE_CONF_PATH, DOCUMENTATION_BASE + "/conf.py"], config_dir)
    _build_docs("confluence", build_dir=build_dir, conf_dir=".", warn_as_error=warn_as_error,
                options=confluence_options)


def write_custom_config(input_files: list[str], output_directory: str) -> None:
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
    parser.add_argument("-s", "--confluence_secret", required=False, help="Publish to Confluence API token")
    parser.add_argument("-p", "--confluence_publish", required=False, default=False, action='store_true',
                        help="Publish to Confluence")

    return parser.parse_args()


def main(args):

    if args.dirs:
        for directory in args.dirs:
            build_api_docs(directory)

    if args.html:
        build_html(args.warn_as_error, BUILDER_DIR)

    if args.confluence:
        build_confluence(args.warn_as_error, BUILDER_DIR, args.confluence_secret, args.confluence_publish)


if __name__ == "__main__":
    opts = parse_args()
    main(opts)
