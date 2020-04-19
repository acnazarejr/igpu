# iGPU

![GitHub](https://img.shields.io/github/license/acnazarejr/igpu)

The `igpu` is a pythonic cross-platform module for getting the GPU info and status from NVIDA GPU boards using th `pynvml` ([a python wrapper around the NVML library](https://github.com/gpuopenanalytics/pynvml)).

## Quick Start

1. Install the `igpu` module.

```python
pip install igpu
```

2. And, enjoy it!

```python
import igpu
gpu_count = igpu.count_devices()
gpu = igpu.get_devices(0)
print(f'This host has {gpu} devices.')
print(f'The first gpu is a {gpu.name} with {gpu.memory.total:.0f}{gpu.memory.unit}.')
```

```shell
This host has 4 devices.
The first gpu is a GeForce GTX 1080 Ti with 11178.50 MiB
```

**Table of Contents**

1. [Requirements](#requirements)
1. [Installation](#installation)
1. [Examples](#examples)
1. [Usage Documentation](#usage-documentation)
   1. [Available Devices](#available-devices)
   1. [Visible Devices](#visible-devices)
   1. [GPUInfo Class Description](#gpuinfo-class-description)
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

## Examples

The following examples illustrates the ease of use of this module. For a complete reference, see the [Usage Documentation](#usage-documentation) section.

### List the utilization stats of all devices

The user can access the utilization stats attributes in the following manner:

```python
import igpu
for gpu_info in igpu.devices():
    print(f'GPU board {gpu_info.index}: {gpu_info.name}')
    print(f'Utilization: GPU {gpu_info.utilization.gpu}% | Memory {gpu_info.utilization.memory}%')
    print(f'Temperature: {gpu_info.utilization.temperature}C (Fan - {gpu_info.utilization.fan}%)')
    print()
```

```shell
GPU board 0: GeForce GTX 1080 Ti
Utilization: GPU 0% | Memory 0%
Temperature: 30C (Fan - 23%)

GPU board 1: GeForce GTX 1080 Ti
Utilization: GPU 65% | Memory 58%
Temperature: 62C (Fan - 36%)

GPU board 2: GeForce GTX 1080 Ti
Utilization: GPU 38% | Memory 33%
Temperature: 63C (Fan - 37%)

GPU board 3: GeForce GTX 1080 Ti
Utilization: GPU 0% | Memory 0%
Temperature: 28C (Fan - 23%)
```

### List the memory and power summary of a specific device

Each attributes group (`memory`, `utilization`, `pci`, `clocks`, `power`, `processes`) can be summarized simply by calling the string converstion. In the next example, we will print the memory and power summary of the second GPU board:

```python
import igpu
gpu_info = igpu.get_device(1)
print(gpu_info.memory)
print(gpu_info.power)
```

```shell
GPU MEMORY:
    Total :   11178.50 MiB (100.00%)
    Used  :    6525.00 MiB ( 58.37%)
    Free  :    4653.50 MiB ( 41.63%)
POWER INFO:
    Management : Supported
    Draw       : 55.751
    Limit      : 250.0
    Min Limit  : 125.0
    Max Limit  : 300.0
```

### List the processes and the memory usage of a specific device

In this example, we will work with the `memory` and `processes` attributes of the first GPU board:

```python
import igpu
gpu_info = igpu.get_device(0)
print(f'The device has {gpu_info.memory.used} allocated out of a total of {gpu_info.memory.total}')
print(f'The {len(gpu_info.processes)} processe(s) running on device are:')
for proc in gpu_info.processes:
    print(f'{proc.pid}: created at {proc.create_time} by {proc.user} and using {proc.gpu_memory}')
```

```shell
The device has 10799.0 allocated out of a total of 11178.5
The 2 processe(s) running on device are:
4276: created at 2020-04-17 03:41:27 by antonio and using 4284
5764: created at 2020-04-16 17:57:12 by acnazarejr and using 6515
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

Also, the class has a method (`GPUInfo.update()`) to update the device information that can be used as follow:

```python
gpu_info.update()
```

The `GPUInfo` has the general GPU attributes:

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
    4276   | python            | antonio       | 45436    | '2020-04-17 03:41:27'  | 4284
    5764   | python            | acnazarejr    | 5759     | '2020-04-16 17:57:12'  | 6515

```


#### Memory Attributes (`GPUMemoryInfo`)

Helper class that handles the on-board memory attributes. Reported total memory is affected by the ECC state. If ECC is enabled, the total available memory is decreased by several percent, due to the requisite parity bits. The driver may also reserve a small amount of memory for internal use, even without active work on the GPU. These attributes are available for all products.

*Attributes*

* `total` (`float`) - The total installed GPU memory.
* `used` (`float`) - The total memory allocated by active contexts.
* `free` (`float`) - The total free memory.
* `unit` (`str`) - The memory unit of measurement.

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

*Attributes*

* `gpu` (`float`) - The percent of the time over the past sample period during which one or more kernels were executing on the GPU. The sample period may be between 1 second and 1/6 second, depending on the product.
* `memory` (`float`) - The percent of the time over the past sample period during which global (device) memory was being read or written. The sample period may be between 1 second and 1/6 second, depending on the product.
* `fan` (`float`) - For a healthy fan, the percent of fan's speed.
* `temperature` (`int`) - The core GPU temperature. For all discrete and S-class products.
* `performance` (`int`) - The current performance state for the GPU. States range from `P0` (maximum performance) to `P12` (minimum performance).

*Usage*

```python
>>> gpu_info.utilization.gpu
65
>>> gpu_info.utilization.memory
59
>>> gpu_info.utilization.fan
36
>>> gpu_info.utilization.temperature
61
>>> gpu_info.utilization.performance
'P2'
```

*String Conversion*

```python
>>> print(gpu_info.utilization)
GPU UTILIZATION:
    Performance : 'P2'
    Temperature : '61C'
    Graphics    : [||||||||||||||||         ] 65.00%
    Memory      : [||||||||||||||           ] 59.00%
    Fan         : [|||||||||                ] 36.00%
```


### PCI Attributes (`GPUPCIInfo`)

Helper class that handles the pci attributes of each GPU.

The class handles the basic PCI info for the device. Some of this information may change whenever cards are added/removed/moved in a system. It also provides the PCIe link generation and bus width. These attributes are available for all products.

*Attributes*

* `bus` (`str`) -The PCI bus number, in hex.
* `bus_id` (`str`) -The PCI bus id as "domain:bus:device.function", in hex.
* `device` (`str`) -The PCI device number, in hex.
* `device_id` (`str`) -The PCI vendor device id, in hex.
* `sub_system_id` (`str`) -The PCI Sub System id, in hex.
* `current_link_gen` (`str`) -The current link generation. These may be reduced when the GPU is not in use.
* `max_link_gen` (`str`) -The maximum link generation possible with this GPU and system configuration. For example, if the GPU supports a higher PCIe generation than the system supports then this reports the system PCIe generation.
* `current_link_width` (`str`) -The current link width. These may be reduced when the GPU is not in use.
* `max_link_width` (`str`) -The maximum link width possible with this GPU and system configuration. For example, if the GPU supports a higher link width than the system supports then this reports the system PCIe link with.

*Usage*

```python
>>> gpu_info.pci.bus
'88'
>>> gpu_info.pci.bus_id
'0000:88:00.0'
>>> gpu_info.pci.device
'00'
>>> gpu_info.pci.device_id
'1B0610DE'
>>> gpu_info.pci.sub_system_id
'1210196E'
>>> gpu_info.pci.current_link_gen
'3'
>>> gpu_info.pci.max_link_gen
'3'
>>> gpu_info.pci.current_link_width
'16x'
>>> gpu_info.pci.max_link_width
'16x'
```

*String Conversion*

```python
>>> print(gpu_info.pci)
PCI INFO:
    Bus           : '88'
    Bus ID        : '0000:88:00.0'
    Device        : '00'
    Device ID     : '1B0610DE'
    Sub-System ID : '1210196E'
    Generation    : '3' (Max: '3')
    Link Width    : '16x' (Max: '16x')
```


### Clock Attributes (`GPUClockInfo`)

Helper class that handles the clocks attributes of each GPU.

The current frequency at which parts of the GPU are running. All readings are in MHz.

*Attributes*

* `graphics` (`int`) - The current frequency of graphics (shader) clock.
* `sm` (`int`) - The current frequency of SM (Streaming Multiprocessor) clock.
* `memory` (`int`) - The current frequency of memory clock.
* `max_graphics` (`int`) - The maximum frequency of graphics (shader) clock.
* `max_sm` (`int`) - The maximum frequency of SM (Streaming Multiprocessor) clock.
* `max_memory` (`int`) - The maximum frequency of memory clock.

*Usage*

```python
>>> gpu_info.clocks.graphics
1885
>>> gpu_info.clocks.sm
1885
>>> gpu_info.clocks.memory
5005
>>> gpu_info.clocks.max_graphics
1911
>>> gpu_info.clocks.max_sm
1911
>>> gpu_info.clocks.max_memory
5505
```

*String Conversion*

```python
>>> print(gpu_info.clocks)
GPU CLOCK:
    Graphics (Shader)             : 1885 (Max: 1911)
    SM (Streaming Multiprocessor) : 1885 (Max: 1911)
    Memory                        : 5005 (Max: 5505)
```

### Power Attributes (`GPUPowerInfo`)

Helper class that handles the power attributes of each GPU.

Power readings help to shed light on the current power usage of the GPU, and the factors that affect that usage. When power management is enabled, the GPU limits power draw under load to fit within a defined power envelope by manipulating the current performance state. See below for limits of availability.

*Attributes*

* `management` (`str`) - A flag that indicates whether power management is enabled. Either "Supported" or "N/A". Requires Inforom PWR object version 3.0 or higher or Kepler device.
* `draw` (`int`) - The last measured power draw for the entire board, in watts. Only available if power management is supported. This reading is accurate to within +/- 5 watts. Requires Inforom PWR object version 3.0 or higher or Kepler device.
* `limit` (`int`) - The software power limit, in watts. Set by software such as nvidia-smi. Only available if power management is supported. Requires Inforom PWR object version 3.0 or higher or Kepler device.
* `min_limit` (`int`) - The minimum value in watts that power limit can be set to. Only on supported devices from Kepler family.
* `max_limit` (`int`) - The maximum value in watts that power limit can be set to. Only on supported devices from Kepler family."""

*Usage*

```python
>>> gpu_info.power.management
'Supported'
>>> gpu_info.power.draw
93.067
>>> gpu_info.power.limit
250.0
>>> gpu_info.power.min_limit
125.0
>>> gpu_info.power.max_limit
300.0
```

*String Conversion*

```python
>>> print(gpu_info.power)
POWER INFO:
    Management : Supported
    Draw       : 93.067
    Limit      : 250.0
    Min Limit  : 125.0
    Max Limit  : 300.0
```

### Processeses Attributes(`GPUProcessesInfo` and `GPUProcessInfo`)

While each process which has compute context on the GPU are handle by the `GPUProcessInfo`, the `GPUProcessesInfo` groups all processes. In other words, `GPUProcessesInfo` lists all processes and `GPUProcessInfo` has the attributes of each process.

To access the process list, the user need to use the `processes` property of `GPUInfo`. This property also has a implicit string conversion:

*Processes List String Conversion*

```python
>>> print(gpu_info.processes)
PROCESSES
    PID    | NAME              | USER          | PARENT   | CREATION TIME          | GPU MEM
    4276   | python            | antonio       | 45436    | '2020-04-17 03:41:27'  | 4284
    5764   | python            | acnazarejr    | 5759     | '2020-04-16 17:57:12'  | 6515
```

Once the `processes` property is a list of `GPUProcessesInfo`, the user can access each process individually, using their attributes.

*Attributes*

* `pid` (`int`) - The process PID.
* `name` (`str`) - The process name.
* `user` (`str`) - The name of the user that owns the process.
* `parent_pid` (`int`) - The process parent PID.
* `parent_name` (`str`) - The process parent name.
* `create_time` (`str`) - The process creation time as a floating point number expressed in seconds since the epoch, in UTC.
* `gpu_memory` (`int`) - The amount of GPU memory allocated by the process.

*Usage*

For example, for the first process in the list.

```python
>>> gpu.processes[0].pid
5764
>>> gpu.processes[0].name
'python'
>>> gpu.processes[0].user
'acnazarejr'
>>> gpu.processes[0].parent_pid
5759
>>> gpu.processes[0].parent_name
'slurmstepd'
>>> gpu.processes[0].create_time
'2020-04-16 17:57:12'
>>> gpu.processes[0].gpu_memory
10789
```

*String Conversion*

```python
>>> print(gpu_info.processes[0])
5764   | python            | acnazarejr    | 5759     | '2020-04-16 17:57:12'  | 6515
```

## License
See [LICENSE](https://github.com/acnazarejr/igpu/blob/develop/LICENSE).
