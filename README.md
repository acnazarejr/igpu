# iGPU
A  for retrieving information and stats on installed gpus.

The `igpu` is a pythonic cross-platform module for getting the GPU info and status from NVIDA GPU boards using th `pynvml` ([a python wrapper around the NVML library](https://github.com/gpuopenanalytics/pynvml)).

**Table of Contents**

1. [Requirements](#requirements)
1. [Installation](#installation)
1. [Usage](#usage)
   1. [Main functions](#main-functions)
   1. [Helper functions](#helper-functions)
1. [Examples](#examples)
   1. [Select first available GPU in Caffe](#select-first-available-gpu-in-caffe)
   1. [Occupy only 1 GPU in TensorFlow](#occupy-only-1-gpu-in-tensorflow)
   1. [Monitor GPU in a separate thread](#monitor-gpu-in-a-separate-thread)
1. [License](#license)

## Requirements

Supports Python 3.4 or higher. Requires least one NVIDIA GPU with latest NVIDIA driver installed.

Python standard libraries:
* os ([The Python Standard Library](https://docs.python.org/3/library/os.html))
* textwraper ([The Python Standard Library](https://docs.python.org/3/library/textwrap.html))
* datetime ([The Python Standard Library](https://docs.python.org/3/library/datetime.html))

Third-party libraries:
* pynvml ([Python bindings to the NVIDIA Management Library](https://github.com/gpuopenanalytics/pynvml))
* psutil ([Python process and system utilities](https://github.com/giampaolo/psutil/))

## Installation

Currently it is only supported Python 3.4 or higher. It can be installed through pip:

```
pip install igpu
```

Test the installation:

1. Start a python console by typing `python` in the terminal
2. In the newly opened python console, type:
```python
import igpu
print(igpu.nvidia_driver_version())
```
3. Your output should look something like following, depending on your nvidia driver version.
```
(430, 34)
```

## Usage

The `igpu` module is very versatile and can be used in a different of ways, given below.

To include iGPU in your Python code, all you hve to do is included it on your script:

```python
import igpu
```

Once included all functions are available. The main functions along with a short description of inputs, outputs and their functionality can be found below.

### Main Functions

#### ```nvidia_driver_version()```
```python
>>> igpu.nvidia_driver_version()
(430, 34)
```



### GPUInfo class description
