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

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="simisatool",
        description="Compress, decompress, or convert a file or directory.",
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
        parser.error(f"input does not exist: {args.input}")

    if not (args.input.is_file() or args.input.is_dir()):
        parser.error(f"input must be a file or directory: {args.input}")

    if args.output is not None and args.output.exists():
        if args.input.is_file() != args.output.is_file():
            parser.error("input and output must both be files or both be directories")

    return args


def main() -> None:
    args = parse_args()

    if args.compress:
        operation = "compress"
    elif args.decompress:
        operation = "decompress"
    else:
        operation = "convert"

    print(f"Operation: {operation}")
    print(f"Format:    {args.format}")
    print(f"Input:     {args.input}")
    print(f"Output:    {args.output}")


if __name__ == "__main__":
    main()