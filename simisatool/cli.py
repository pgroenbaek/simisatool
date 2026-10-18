"""
This file is part of Simisatool.

Copyright (C) 2026 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import simisa
import argparse
from pathlib import Path


CLI_VERSION = "0.1.0-beta"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="simisatool",
        description="Compress, decompress, or convert a file or directory.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + CLI_VERSION,
        help="Show the version number and exit.",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-c",
        "--compress",
        action="store_true",
        help="Compress the input.",
    )
    mode.add_argument(
        "-d",
        "--decompress",
        action="store_true",
        help="Decompress the input.",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=("ascii", "unicode", "binary"),
        default="unicode",
        help="Output format (default: unicode).",
    )

    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input file or directory.",
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Output file or directory (optional).",
    )

    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Input does not exist: {args.input}")

    if not (args.input.is_file() or args.input.is_dir()):
        parser.error(f"Input must be a file or directory: {args.input}")

    if args.output is not None and args.output.exists():
        if args.input.is_file() != args.output.is_file():
            parser.error("Input and output must both be files or both be directories")

    if args.format == "unicode" and parser.compress:
        print("Format 'unicode' not supported when compressing, using 'ascii' instead.", file=sys.stderr)
        args.format = "ascii"

    return args


def process_file(input_file: Path, output_file: Path) -> None:
    pass


def main() -> None:
    args = parse_args()
    
    write_binary = True if args.format == "binary" else False
    write_unicode = True if args.format == "unicode" else False
    write_ascii = True if args.format == "ascii" else False
    write_compressed = True if args.compress else False
    write_decompressed = True if args.decompress else False

    extensions = {".s", ".t", ".w"}

    input_files = (
        [args.input]
        if args.input.is_file()
        else [
            path
            for path in args.input.iterdir()
            if path.is_file() and path.suffix.lower() in extensions
        ]
    )

    for input_file in files:
        if args.output is None:
            output_file = input_file
        elif args.output.is_dir():
            output_file = args.output / input_file.name
        else:
            output_file = args.output

        process_file(input_file, output_file)


if __name__ == "__main__":
    main()