# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser


from compat import dict
from lib import JohnnyDist, has_error
from logs import configure_logging
from util import python_interpreter
from requirementstxt import parseFile
from walk import node_license_walk

FIELDS = dict(
    [
        # (attribute, help)
        ("name", "Canonical name of the distribution"),
        ("summary", "Short description of the distribution"),
        ("specifier", "Requirement specifier (see PEP 508) e.g. ~=1.7"),
        ("requires", "Immediate dependencies"),
        ("required_by", "Parent(s) in the tree"),
        ("import_names", "Python imports provided (top-level names only)"),
        ("homepage", "Project URL"),
        ("extras_available", "Optional extensions available for the distribution"),
        ("extras_requested", "Optional extensions parsed from requirement specifier"),
        ("project_name", "Usually matches the canonical name but may have different case"),
        ("license", "License covering the distribution"),
        ("versions_available", "List of versions available at index"),
        ("version_installed", "Version currently installed, if any"),
        ("version_latest", "Latest version available"),
        ("version_latest_in_spec", "Best version: latest available within requirement specifier"),
        ("download_link", "Source or binary distribution URL"),
        ("checksum", "Source or binary distribution hash"),
    ]
)


def main():
    default_fields = os.environ.get("JOHNNYDEP_FIELDS", "name,summary").split(",")
    parser = ArgumentParser(prog="johnnydep", description=__doc__)
    # parser.add_argument("req", help="The project name or requirement specifier")
    parser.add_argument("--index-url", "-i")
    parser.add_argument("--extra-index-url")
    parser.add_argument(
        "--ignore-errors",
        action="store_true",
        help="Continue rendering the tree even if errors occur",
    )
    parser.add_argument(
        "--output-format",
        "-o",
        choices=["human", "json", "yaml", "python", "toml", "pinned"],
        default="human",
        help="default: %(default)s",
    )
    parser.add_argument(
        "--no-deps",
        help="Don't recurse the dependency tree. Has no effect for output format 'human'",
        dest="recurse",
        action="store_false",
    )
    parser.add_argument(
        "--fields",
        "-f",
        nargs="*",
        default=default_fields,
        choices=list(FIELDS) + ["ALL"],
        help="default: %(default)s",
    )
    parser.add_argument("--for-python", "-p", dest="env", type=python_interpreter)
    parser.add_argument("--verbose", "-v", default=1, type=int, choices=range(3))
    # parser.add_argument(
    #     "--version",
    #     action="version",
    #     version="%(prog)s v{}".format(__version__),
    # )
    parser.add_argument(
        "--requirements", "-r", 
        dest="requirements",
        nargs="*",
        type=str
    )
    parser.add_argument(
        "--walk", "-w", 
        dest="walk",
        nargs=1,
        type=str
    )
    parser.add_argument(
        "--node-license-walk", "-n", 
        dest="node_license_walk",
        nargs=1,
        type=str
    )
    args = parser.parse_args()

    if "ALL" in args.fields:
        args.fields = list(FIELDS)
    configure_logging(verbosity=args.verbose)
    if args.node_license_walk:
        node_license_walk(path=args.node_license_walk[0])
    elif args.walk:
        pass
    elif args.requirements:
        parseFile(args, filename=args.requirements[0])
        sys.exit(0)
    
    else:
        dist = JohnnyDist(
            args.req,
            index_url=args.index_url,
            env=args.env,
            extra_index_url=args.extra_index_url,
            ignore_errors=args.ignore_errors,
        )
        print(dist.serialise(fields=args.fields, format=args.output_format, recurse=args.recurse))
        if (args.recurse and has_error(dist)) or (not args.recurse and dist.error is not None):
            sys.exit(1)
