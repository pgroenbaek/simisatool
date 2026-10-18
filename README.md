# simisatool

A cross-platform CLI for compressing and decompressing `.s`, `.t`, and `.w` files used with Open Rails and MSTS.

If you need this functionality from within a Python script, then have a look at the [simisa](https://github.com/pgroenbaek/simisa) module instead.

> [!NOTE]
> **The underlying Python module [simisa](https://github.com/pgroenbaek/simisa) used by this CLI is in a beta testing phase.** The CLI and underlying module are functional and stable enough to use, but further testing and real-world usage are needed to validate their reliability and ensure stability across different use cases and that file output works with all the different tools that exist like TSRE5, TSFV, ffeditc_unicode.exe, etc.

## Installation

Download the CLI executable from the [Releases](https://github.com/pgroenbaek/cdp-unpack/releases) page for your operating system, then extract it somewhere you can find it.

## Usage

```bash
simisatool <input> [output]
simisatool --compress <input> [output]
simisatool -c <input> [output]
simisatool --decompress <input> [output]
simisatool -d <input> [output]
simisatool [--format=ascii] <input> [output]
simisatool [-f ascii] <input> [output]
simisatool [--format=unicode] <input> [output]
simisatool [-f unicode] <input> [output]
simisatool [--format=binary] <input> [output]
simisatool [-f binary] <input> [output]
```

## License

The source code of this project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html). You are free to use, modify, and distribute the code under the terms of this license.

See the [LICENSE](/LICENSE) file for the full license text.