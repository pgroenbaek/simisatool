# simisapack


## Building

Visual Studio Build Tools
workload: Desktop development with C++

`python -m nuitka --onefile --follow-imports --enable-plugin=numpy --output-filename=simisapack simisapack.py`

`python -m nuitka your.py \
  --standalone \
  --follow-imports \
  --enable-plugin=some_plugin`