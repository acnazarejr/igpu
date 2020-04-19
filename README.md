# iGPU

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

## Usage Documentation

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

#### ```igpu.visible_devices()```

Returns a [`GpuInfo`](#gpuinfo-class-description) list containing all visible devices defined by the `CUDA_VISIBLE_DEVICES` environmnt variable.

All properties and methods of `GpuInfo` class are described in [GPUInfo Class Description](#gpuinfo-class-description) section.

```python
>>> for gpu_info in igpu.visible_devices():
...     print(gpu_info.index, gpu_info.name)
1, GeForce GTX 1080 Ti
3, GeForce GTX 1080 Ti
```


### GPUInfo Class Description

The `GPUInfo` is a helper class that handles the attributes of each GPU. The user can access all properties and stats accordingly with the GPU attributes categories. Each category has another helper subclass described below. Also, the class, and consequently, its subclasses, has an implicit conversion to a pretty string.

For the all next examples, consider that the a instace of GPUInfo was created as follow:

```python
gpu_info = igpu.get_device(0)
```

The GPUInfo has the general GPU attributes:

*Attributes*

* `index` (`int`) - The index of the GPU device.
* `name` (`str`) - The official product name of the GPU.
* `serial` (`str`) - The GPU board serial number. This number matches the serial number physically printed on each board. It is a globally unique immutable alphanumeric value.
* `uuid` (`str`) - The GPU board uuid. This value is the globally unique immutable alphanumeric identifier of the GPU. It does not correspond to any physical label on the board.
* `bios` (`str`) - The BIOS version of the GPU board.

*Usage*

```python
>>> gpu_info.index
0
>>> gpu_info.name
'GeForce GTX 1080 Ti'
>>> gpu_info.serial
'N/A'
>>> gpu_info.uuid
'GPU-d9bf777c-e49e-e609-f873-d05b3208970b'
>>> gpu_info.bios
'86.02.39.00.01'
```

*String Conversion*

```python
>>> print(gpu_info)
INDEX        : 0
BOARD NAME   : 'GeForce GTX 1080 Ti'
SERIAL       : 'N/A'
UUID         : 'GPU-115dafb8-26db-32ba-d729-f21b29fc001f'
BIOS VERSION : '86.02.39.00.01'

GPU MEMORY:
    Total :   11178.50 MiB (100.00%)
    Used  :   10799.00 MiB ( 96.61%)
    Free  :     379.50 MiB (  3.39%)

GPU UTILIZATION:
    Performance : P2
    Temperature : '61C'
    Graphics    : [|||||||||||              ] 44.00%
    Memory      : [||||||||                 ] 35.00%
    Fan         : [|||||||||                ] 36.00%

PCI INFO:
    Bus           : '88'
    Bus ID        : '0000:88:00.0'
    Device        : '00'
    Device ID     : '1B0610DE'
    Sub-System ID : '1210196E'
    Generation    : '3 (Max: 3)'
    Link Width    : '16x (Max: 16x)'

GPU CLOCK:
    Graphics (Shader)             : 1885 (Max: 1911)
    SM (Streaming Multiprocessor) : 1885 (Max: 1911)
    Memory                        : 5005 (Max: 5505)

POWER INFO:
    Management : 'Supported'
    Draw       : 122.23
    Limit      : 250.0
    Min Limit  : 125.0
    Max Limit  : 300.0

PROCESSES
    PID    | NAME              | USER          | PARENT   | CREATION TIME          | GPU MEM
    5764   | python            | acnazarejr    | 5759     | '2020-04-16 17:57:12'  | 10789
```


#### Memory Attributes (`GPUMemoryInfo`)

Helper class that handles the on-board memory attributes. Reported total memory is affected by the ECC state. If ECC is enabled, the total available memory is decreased by several percent, due to the requisite parity bits. The driver may also reserve a small amount of memory for internal use, even without active work on the GPU. These attributes are available for all products.

*Attributes*

* `total` (`float`) - The total installed GPU memory;
* `used` (`float`) - The total memory allocated by active contexts;
* `free` (`float`) - The total free memory;
* `unit` (`str`) - The memory unit of measurement;

*Usage*

```python
>>> gpu.memory.total
11178.5
>>> gpu.memory.used
10799.0
>>> gpu.memory.free
379.5
>>> gpu.memory.unit
'MiB'
```

*String Conversion*

```python
>>> print(gpu_info.memory)
GPU MEMORY:
    Total :   11178.50 MiB (100.00%)
    Used  :   10799.00 MiB ( 96.61%)
    Free  :     379.50 MiB (  3.39%)
```

#### Utilization Stats (`GPUUtilizationInfo`)

Helper class that handles the utilization stats of each GPU. Utilization rates report how busy each GPU is over time, and can be used to determine how much an application is using the GPUs in the system.

**Attributes**

* `gpu` (`float`) - The percent of the time over the past sample period during which one or more kernels were executing on the GPU. The sample period may be between 1 second and 1/6 second, depending on the product.
* `memory` (`float`) - The percent of the time over the past sample period during which global (device) memory was being read or written. The sample period may be between 1 second and 1/6 second, depending on the product.
* `fan` (`float`) - For a healthy fan, the percent of fan's speed.
* `temperature` (`int`) - The core GPU temperature. For all discrete and S-class products.
* `performance` (`int`) - The current performance state for the GPU. States range from `P0` (maximum performance) to `P12` (minimum performance).

**Usage**

```python
>>> gpu.utilization.gpu
65
>>> gpu.utilization.memory
59
>>> gpu.utilization.fan
36
>>> gpu.utilization.temperature
61
>>> gpu.utilization.performance
'P2'
```

**String Conversion**

```python
>>> print(gpu.utilization)
GPU UTILIZATION:
    Performance : 'P2'
    Temperature : '61C'
    Graphics    : [||||||||||||||||         ] 65.00%
    Memory      : [||||||||||||||           ] 59.00%
    Fan         : [|||||||||                ] 36.00%
```

