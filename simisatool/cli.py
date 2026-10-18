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
from typing import List, Tuple, Optional


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
        default=None,
        help="Output format (default: binary when compressing, otherwise unicode).",
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

    if args.format is None:
        args.format = "binary" if args.compress else "unicode"

    if args.format == "unicode" and parser.compress:
        args.format = "ascii"

    return args


def process_file(input_file: Path, output_file: Path, args: argparse.Namespace) -> Optional[bool]:
    input_compressed = simisa.is_compressed(input_file)
    input_binary = simisa.is_binary(input_file)
    input_unicode = simisa.is_unicode(input_file)
    input_text = simisa.is_text(input_file)
    input_filetype = simisa.read_filetype(input_file)

    if input_compressed is None:
        print(f"{input_file.name}: invalid or unrecognized header", file=sys.stderr)
        return False

    loaders = {
        "s": (simisa.shape.load, simisa.shape.dump),
        "t": (simisa.terrain.load, simisa.terrain.dump),
        "w": (simisa.world.load, simisa.world.dump),
    }

    if input_filetype not in loaders:
        print(f"{input_file.name}: unsupported file type '{input_filetype}'", file=sys.stderr)
        return False

    detected_formats = [
        input_format
        for input_format, detected in (
            ("binary", input_binary),
            ("unicode", input_unicode),
            ("ascii", input_text and not input_unicode),
        )
        if detected is True
    ]

    if len(detected_formats) != 1:
        print(f"{input_file.name}: invalid or ambiguous encoding", file=sys.stderr)
        return False

    input_format = detected_formats[0]

    if args.compress:
        output_compressed = True
    elif args.decompress:
        output_compressed = False
    else:
        output_compressed = input_compressed

    output_format = args.format

    same_file = input_file.resolve() == output_file.resolve()
    same_format = input_format == output_format
    same_compression = input_compressed == output_compressed

    if same_file and same_format and same_compression:
        return None

    load, dump = loaders[input_filetype]

    try:
        data = load(input_file)

        dump(
            data,
            output_file,
            compressed=output_compressed,
            binary=output_format == "binary",
            ascii=output_format == "ascii",
        )
    except Exception as exc:
        print(f"{input_file.name}: failed: {exc}", file=sys.stderr)
        return False

    return True


def main() -> None:
    args = parse_args()

    extensions = {".s", ".t", ".w"}
    is_single_file = args.input.is_file()

    input_files = (
        [args.input]
        if is_single_file
        else [
            path
            for path in args.input.iterdir()
            if path.is_file() and path.suffix.lower() in extensions
        ]
    )

    results: List[Tuple[Path, Optional[bool]]] = []

    for input_file in input_files:
        if args.output is None:
            output_file = input_file
        elif args.output.is_dir():
            output_file = args.output / input_file.name
        else:
            output_file = args.output

        success = process_file(input_file, output_file, args)

        if is_single_file:
            if success is True:
                print(f"{input_file.name}: success")
            elif success is False:
                print(f"{input_file.name}: failed")
            else:
                print(f"{input_file.name}: skipped")
        else:
            results.append((input_file, success))

    if not is_single_file:
        succeeded = sum(success is True for _, success in results)
        failed = sum(success is False for _, success in results)
        skipped = sum(success is None for _, success in results)

        print(
            f"Processed {len(results)} files: "
            f"{succeeded} succeeded, {failed} failed, {skipped} skipped"
        )


if __name__ == "__main__":
    main()