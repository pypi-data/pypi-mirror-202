# opm-origen

## Prerequisites

- Install make, cmake and g++
- Build/Install Opm-Common
- Build/Install Opm-Grid

## Install opm packages

```bash
sudo apt-add-repository ppa:opm/ppa
sudo apt-get update

sudo apt-get install libopm-common-dev
sudo apt-get install libopm-grid-dev
```

## How to build

```bash
git clone git@github.com:OriGenAI/opm-origen.git
cd opm-origen
mkdir build
cd build
cmake ..
make
```

## How to use

- Copy the binary under `build/lib` folder
- Import the binary from your Python code
- Call the library functions

## Example

```python
from origen.ai.ecl import read_transmissibility

trans = read_transmissibility("path-to-data.DATA")
print(trans)
```

## Develop

You can use the main.cpp file to debug. Just call your function from there and compile the code. You will find the binary in `build/bin/main`
