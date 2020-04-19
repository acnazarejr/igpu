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

To include iGPU in your Python code, all you have to do is included it on your script:

```python
import igpu
```

Once included all functions are available. The main functions along with a short description of inputs, outputs, and functionality can be found in the next sections.

### Available Devices

The `igpu` can manipulate information and stats for all available devices. Availability is determined based on the GPU boards installed on the host.

#### ```igpu.count_devices()```

Returns the number of available GPU devices installed on the host.

```python
>>> igpu.count_devices()
4
```

#### ```igpu.devices_index()```

Returns an index list, containing the device index for each available GPU.

```python
>>> igpu.devices_index()
[0, 1, 2, 3]
```

#### ```igpu.get_device(device_index)```

Given a `device_index`, returns a [`GpuInfo`](#gpuinfo-class-description) object containing the device properties and stats. If a nonexistent `device_index` is provided, an error is thrown.

All properties and methods of `GpuInfo` class are described in [GPUInfo Class Description](#gpuinfo-class-description) section.

```python
>>> gpu_info = igpu.get_device(2)
>>> print(gpu_info.index, gpu_info.name)
2, GeForce GTX 1080 Ti
```

#### ```igpu.devices()```

Returns a [`GpuInfo`](#gpuinfo-class-description) list containing all available devices.

All properties and methods of `GpuInfo` class are described in [GPUInfo Class Description](#gpuinfo-class-description) section.

```python
>>> for gpu_info in igpu.devices():
...     print(gpu_info.index, gpu_info.name)
0, GeForce GTX 1080 Ti
1, GeForce GTX 1080 Ti
2, GeForce GTX 1080 Ti
3, GeForce GTX 1080 Ti
```

### Visible Devices

By manually setting the environment variable ```CUDA_VISIBLE_DEVICES``` (or automatically, by other software, like SLURM cluster manager), the user can mask which GPUs should be visible to different Deep Learning frameworks (e.g. TensorFlow, PyTorch, Caffee, etc). See [this stackoverflow question ](https://stackoverflow.com/questions/39649102/how-do-i-select-which-gpu-to-run-a-job-on) for more info.

The `igpu` module can deal with this, and consider only the visible devices, by the following methods. This functionality is handy for those who work on environments where the visible devices are defined externally. For example, [when the SLURM sets](https://slurm.schedmd.com/gres.html) the `CUDA_VISIBLE_DEVICES` variable in a job.

For the next examples, consider that the `CUDA_VISIBLE_DEVICES` variable was set as below:

```shell
export CUDA_VISIBLE_DEVICES=1,3
```


#### ```igpu.count_visible_devices()```

Returns the number of visible GPU devices, defined by the `CUDA_VISIBLE_DEVICES` environmnt variable.

```python
>>> igpu.count_visible_devices()
2
```

#### ```igpu.visible_devices_index()```

Returns an index list, containing the device index for each visible GPU defined by the `CUDA_VISIBLE_DEVICES` environmnt variable.

```python
>>> igpu.visible_devices_index()
[1, 3]
```


### GPUInfo Class Description
