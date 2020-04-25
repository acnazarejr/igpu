#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation of igpu GPUInfo class
@author Antonio Carlos Nazare Jr.
@url http://github.com/acnazarejr/igpu
"""

import textwrap
import math
from typing import Dict, List
from datetime import datetime
from igpu import parser


class GPUMemoryInfo(object):
    """
    Helper class that handles the memory attributes of each GPU.

    On-board memory information. Reported total memory is affected by the ECC state.
    If ECC is enabled, the total available memory is decreased by several percent, due to the
    requisite parity bits. The driver may also reserve a small amount of memory for internal use,
    even without active work on the GPU. These attributes are available for all products.
    """

    def __init__(self, memory_dict: Dict) -> None:
        self._total = memory_dict['total']
        self._used = memory_dict['used']
        self._free = memory_dict['free']
        self._unit = memory_dict['unit']

        self._total = self._total if isinstance(self._total, float) else float('NaN')
        self._used = self._used if isinstance(self._used, float) else float('NaN')
        self._free = self._free if isinstance(self._free, float) else float('NaN')
        self._unit = self._unit if isinstance(self._unit, str) else 'N/A'

    @property
    def total(self) -> float:
        """float: Returns the total installed GPU memory."""
        return self._total

    @property
    def used(self) -> float:
        """float: Returns the total memory allocated by active contexts."""
        return self._used

    @property
    def free(self) -> float:
        """float: Returns the total free memory."""
        return self._free

    @property
    def unit(self) -> str:
        """str: Returns the memory unit of measurement."""
        return self._unit

    def __str__(self) -> str:
        ret = [
            'GPU MEMORY:',
            f'    {"Total":6s}: {self.total:10.2f} {self.unit} (100.00%)',
            f'    {"Used":6s}: {self.used:10.2f} {self.unit} ({self.used/self.total*100:6.2f}%)',
            f'    {"Free":6s}: {self.free:10.2f} {self.unit} ({self.free/self.total*100:6.2f}%)'
        ]
        return '\n'.join(ret)

class GPUUtilizationInfo(object):
    """
    Helper class that handles the utilization stats of each GPU.

    Utilization rates report how busy each GPU is over time, and can be used to determine how much
    an application is using the GPUs in the system.
    """

    def __init__(self, utilization_dict: Dict) -> None:
        self._gpu = utilization_dict['gpu']
        self._memory = utilization_dict['memory']
        self._fan = utilization_dict['fan']
        self._temp = utilization_dict['temperature']
        self._perf = utilization_dict['performance']

        self._gpu = float(self._gpu) if isinstance(self._gpu, int) else float('NaN')
        self._memory = float(self._memory) if isinstance(self._memory, int) else float('NaN')
        self._fan = float(self._fan) if isinstance(self._fan, int) else float('NaN')
        self._temp = float(self._temp) if isinstance(self._temp, int) else float('NaN')
        self._perf = self._perf if isinstance(self._perf, str) else 'N/A'

    @property
    def gpu(self) -> float:
        """float: Returns the percent of the time over the past sample period during which one or
        more kernels were executing on the GPU. The sample period may be between 1 second and 1/6
        second, depending on the product.
        """
        return self._gpu

    @property
    def memory(self) -> float:
        """float: Returns the percent of the time over the past sample period during which global
        (device) memory was being read or written. The sample period may be between 1 second and
        1/6 second, depending on the product."""
        return self._memory

    @property
    def fan(self) -> float:
        """float: Returns, for a healthy fan, the percent of fan's speed."""
        return self._fan

    @property
    def temperature(self) -> float:
        """float: Returns the core GPU temperature. For all discrete and S-class products."""
        return self._temp

    @property
    def performance(self) -> str:
        """str: Return the current performance state for the GPU. States range from
        P0 (maximum performance) to P12 (minimum performance).
        """
        return self._perf

    def __str__(self) -> str:

        if not math.isnan(self.gpu):
            ginfo = f'[{"|"*int(self.gpu/4):25s}] {self.gpu:3.2f}%'
        else:
            ginfo = 'N/A'

        if not math.isnan(self.memory):
            gmemory = f'[{"|"*int(self.memory/4):25s}] {self.memory:3.2f}%'
        else:
            gmemory = 'N/A'

        if not math.isnan(self.fan):
            gfan = f'[{"|"*int(self.fan/4):25s}] {self.fan:3.2f}%'
        else:
            gfan = 'N/A'

        ret = [
            'GPU UTILIZATION:',
            f'    {"Performance":12s}: {self.performance}',
            f'    {"Temperature":12s}: {self.temperature:3.2f}C',
            f'    {"Graphics":12s}: {ginfo}',
            f'    {"Memory":12s}: {gmemory}',
            f'    {"Fan":12s}: {gfan}',
        ]
        return '\n'.join(ret)

class GPUPCIInfo(object):
    """
    Helper class that handles the pci attributes of each GPU.

    The class handles the basic PCI info for the device. Some of this information may change
    whenever cards are added/removed/moved in a system. It also provides the PCIe link generation
    and bus width. These attributes are available for all products.
    """

    def __init__(self, pci_dict: Dict) -> None:
        self._bus = pci_dict['bus']
        self._bus_id = pci_dict['bus_id']
        self._device = pci_dict['device']
        self._device_id = pci_dict['device_id']
        self._sub_system_id = pci_dict['sub_system_id']
        self._current_link_generation = pci_dict['current_link_generation']
        self._max_link_generation = pci_dict['max_link_generation']
        self._current_link_width = pci_dict['current_link_width']
        self._max_link_width = pci_dict['max_link_width']

    @property
    def bus(self) -> str:
        """str: Returns the PCI bus number, in hex."""
        return self._bus

    @property
    def bus_id(self) -> str:
        """str: Returns the PCI bus id as "domain:bus:device.function", in hex."""
        return self._bus_id

    @property
    def device(self) -> str:
        """str: Returns the PCI device number, in hex."""
        return self._device

    @property
    def device_id(self) -> str:
        """str: Returns the PCI vendor device id, in hex."""
        return self._device_id

    @property
    def sub_system_id(self) -> str:
        """str: Returns the PCI Sub System id, in hex."""
        return self._sub_system_id

    @property
    def current_link_gen(self) -> str:
        """str: Returns the current link generation.
        These may be reduced when the GPU is not in use."""
        return self._current_link_generation

    @property
    def max_link_gen(self) -> str:
        """str: Returns the maximum link generation possible with this GPU and system
        configuration. For example, if the GPU supports a higher PCIe generation than the system
        supports then this reports the system PCIe generation."""
        return self._max_link_generation

    @property
    def current_link_width(self) -> str:
        """str: Returns the current link width.
        These may be reduced when the GPU is not in use."""
        return self._current_link_width

    @property
    def max_link_width(self) -> str:
        """str: Returns the maximum link width possible with this GPU and system
        configuration. For example, if the GPU supports a higher link width than the system
        supports then this reports the system PCIe link with."""
        return self._max_link_width


    def __str__(self):
        ret = [
            'PCI INFO:',
            f'    {"Bus":14s}: {self.bus}',
            f'    {"Bus ID":14s}: {self.bus_id}',
            f'    {"Device":14s}: {self.device}',
            f'    {"Device ID":14s}: {self.device_id}',
            f'    {"Sub-System ID":14s}: {self.sub_system_id}',
            f'    {"Generation":14s}: {self.current_link_gen} (Max: {self.max_link_gen})',
            f'    {"Link Width":14s}: {self.current_link_width} (Max: {self.max_link_width})',
        ]
        return '\n'.join(ret)

class GPUClockInfo(object):
    """
    Helper class that handles the clocks attributes of each GPU.

    The current frequency at which parts of the GPU are running. All readings are in MHz.
    """

    def __init__(self, clocks_dict: Dict) -> None:
        self._gr = clocks_dict['graphics']
        self._sm = clocks_dict['sm']
        self._memory = clocks_dict['memory']
        self._max_gr = clocks_dict['max_graphics']
        self._max_sm = clocks_dict['max_sm']
        self._max_mem = clocks_dict['max_memory']
        self._unit = clocks_dict['unit']

        self._gr = float(self._gr) if isinstance(self._gr, int) else float('NaN')
        self._sm = float(self._sm) if isinstance(self._sm, int) else float('NaN')
        self._memory = float(self._memory) if isinstance(self._memory, int) else float('NaN')
        self._max_gr = float(self._max_gr) if isinstance(self._max_gr, int) else float('NaN')
        self._max_sm = float(self._max_sm) if isinstance(self._max_sm, int) else float('NaN')
        self._max_mem = float(self._max_mem) if isinstance(self._max_mem, int) else float('NaN')
        self._unit = self._unit if isinstance(self._unit, str) else 'N/A'

    @property
    def graphics(self) -> float:
        """float: Returns the current frequency of graphics (shader) clock."""
        return self._gr

    #pylint: disable=invalid-name
    @property
    def sm(self) -> float:
        """float: Returns the current frequency of SM (Streaming Multiprocessor) clock."""
        return self._sm
    #pylint: enable=invalid-name

    @property
    def memory(self) -> float:
        """float: Returns the current frequency of memory clock."""
        return self._memory

    @property
    def max_graphics(self) -> float:
        """float: Returns the maximum frequency of graphics (shader) clock."""
        return self._max_gr

    @property
    def max_sm(self) -> float:
        """float: Returns the maximum frequency of SM (Streaming Multiprocessor) clock."""
        return self._max_sm

    @property
    def max_memory(self) -> float:
        """float: Returns the maximum frequency of memory clock."""
        return self._max_mem

    @property
    def unit(self) -> str:
        """str: Returns the clock unit of measurement."""
        return self._unit

    def __str__(self):
        ret = [
            'GPU CLOCK:',
            f'    {"Graphics":9s}: {self.graphics:.1f} {self.unit} (Max: {self.max_graphics:.1f})',
            f'    {"SM":9s}: {self.sm:.1f} {self.unit} (Max: {self.max_sm:.1f})',
            f'    {"Memory":9s}: {self.memory:.1f} {self.unit} (Max: {self.max_memory:.1f})',
        ]
        return '\n'.join(ret)

class GPUPowerInfo(object):
    """
    Helper class that handles the power attributes of each GPU.

    Power readings help to shed light on the current power usage of the GPU, and the factors that
    affect that usage. When power management is enabled, the GPU limits power draw under load to
    fit within a defined power envelope by manipulating the current performance state.
    See below for limits of availability.
    """

    def __init__(self, power_dict: Dict) -> None:
        self._management = power_dict['management']
        self._draw = power_dict['draw']
        self._limit = power_dict['limit']
        self._min_lim = power_dict['min_limit']
        self._max_lim = power_dict['max_limit']
        self._unit = power_dict['unit']

        self._management = self._management if isinstance(self._management, str) else 'N/A'
        self._draw = self._draw if isinstance(self._draw, float) else float('NaN')
        self._limit = self._limit if isinstance(self._limit, float) else float('NaN')
        self._min_lim = self._min_lim if isinstance(self._min_lim, float) else float('NaN')
        self._max_lim = self._max_lim if isinstance(self._max_lim, float) else float('NaN')
        self._unit = self._unit if isinstance(self._unit, str) else 'N/A'


    @property
    def management(self) -> str:
        """int: Returns a flag that indicates whether power management is enabled.
        Either "Supported" or "N/A".
        Requires Inforom PWR object version 3.0 or higher or Kepler device."""
        return self._management

    @property
    def draw(self) -> float:
        """float: Returns the last measured power draw for the entire board, in watts.
        Only available if power management is supported.
        This reading is accurate to within +/- 5 watts.
        Requires Inforom PWR object version 3.0 or higher or Kepler device."""
        return self._draw

    @property
    def limit(self) -> float:
        """float: Returns the software power limit, in watts. Set by software such as nvidia-smi.
        Only available if power management is supported.
        Requires Inforom PWR object version 3.0 or higher or Kepler device.
        """
        return self._limit

    @property
    def min_limit(self) -> float:
        """float: Returns the minimum value in watts that power limit can be set to.
        Only on supported devices from Kepler family.
        """
        return self._min_lim

    @property
    def max_limit(self) -> float:
        """float: Returns the maximum value in watts that power limit can be set to.
        Only on supported devices from Kepler family."""
        return self._max_lim

    @property
    def unit(self) -> str:
        """str: Returns the power unit of measurement."""
        return self._unit

    def __str__(self):
        ret = [
            'POWER INFO:',
            f'    {"Management":11s}: {self.management}',
            f'    {"Draw":11s}: {self.draw:.2f} {self.unit}',
            f'    {"Limit":11s}: {self.limit:.2f} {self.unit}',
            f'    {"Min Limit":11s}: {self.min_limit:.2f} {self.unit}',
            f'    {"Max Limit":11s}: {self.max_limit:.2f} {self.unit}',
        ]
        return '\n'.join(ret)

class GPUProcessInfo(object):
    """
    Helper class that handles each process which has compute context on the GPU.
    """
    def __init__(self, process_dict: Dict) -> None:
        self._pid = process_dict['pid']
        self._name = process_dict['name']
        self._user = process_dict['user']
        self._parent_id = process_dict['parent_id']
        self._parent_name = process_dict['parent_name']
        self._create_time = process_dict['create_time']
        self._create_time = datetime.fromtimestamp(int(self._create_time))
        self._create_time = self._create_time.strftime('%Y-%m-%d %H:%M:%S')
        self._gpu_memory = process_dict['gpu_memory']

    @property
    def pid(self) -> int:
        """int: Returns the process PID."""
        return self._pid

    @property
    def name(self) -> str:
        """str: Returns The process name."""
        return self._name

    @property
    def user(self) -> str:
        """str: Returns The name of the user that owns the process."""
        return self._user

    @property
    def parent_pid(self) -> int:
        """int: Returns the process parent PID."""
        return self._parent_id

    @property
    def parent_name(self) -> str:
        """str: Returns the process parent name."""
        return self._parent_name

    @property
    def create_time(self) -> str:
        """str: Returns the process creation time as a floating point number expressed in seconds
        since the epoch, in UTC."""
        return self._create_time

    @property
    def gpu_memory(self) -> int:
        """int: Returns the amount of GPU memory allocated by the process."""
        return self._gpu_memory

    def __str__(self) -> str:
        ret = [
            f'{self.pid:<6d}',
            f'{textwrap.shorten(self.name, width=20):20s}',
            f'{textwrap.shorten(self.user, width=20):20s}',
            f'{self.parent_pid:<8d}',
            f'{self.create_time:20s}',
            f'{self.gpu_memory:<6d}',
        ]
        return ' | '.join(ret)

class GPUProcessesInfo(list):
    """


    List of processes having compute context on the device.
    """

    def __init__(self, processes_list: List) -> None:
        list.__init__(self)
        for process_dict in processes_list:
            self.append(GPUProcessInfo(process_dict))

    def __str__(self):
        ret = [
            f'{"PID":6s}',
            f'{"NAME":20s}',
            f'{"USER":20s}',
            f'{"PARENT":8s}',
            f'{"CREATION TIME":20s}',
            f'{"GPU MEM":6s}',
        ]
        ret = 'PROCESSES\n' + '    ' + ' | '.join(ret) + '\n'
        for process in self:
            ret += '    ' + str(process) + '\n'
        return ret

class GPUInfo(object):
    """
    Helper class that handles the attributes of each GPU
    """


    def __init__(self, device_dict: Dict) -> None:
        self._index = device_dict['index']
        self._name = device_dict['name']
        self._serial = device_dict['serial']
        self._uuid = device_dict['uuid']
        self._bios = device_dict['bios']

        self._name = self._name if isinstance(self._name, str) else 'N/A'
        self._serial = self._serial if isinstance(self._serial, str) else 'N/A'
        self._uuid = self._uuid if isinstance(self._uuid, str) else 'N/A'
        self._bios = self._bios if isinstance(self._bios, str) else 'N/A'

        self._memory_info: GPUMemoryInfo = GPUMemoryInfo(device_dict['memory'])
        self._utilization_info = GPUUtilizationInfo(device_dict['utilization'])
        self._pci_info = GPUPCIInfo(device_dict['pci'])
        self._clocks_info = GPUClockInfo(device_dict['clocks'])
        self._power_info = GPUPowerInfo(device_dict['power'])
        if device_dict['processes'] is None:
            self._processes_info = None
        else:
            self._processes_info = GPUProcessesInfo(device_dict['processes'])

    @property
    def index(self) -> int:
        """int: Returns the index of the GPU device."""
        return self._index

    @property
    def name(self) -> str:
        """str: Returns the official product name of the GPU."""
        return self._name

    @property
    def serial(self) -> str:
        """str: Returns the GPU board serial number. This number matches the serial number
        physically printed on each board. It is a globally unique immutable alphanumeric value."""
        return self._serial

    @property
    def uuid(self) -> str:
        """str: Returns the GPU board uuid. This value is the globally unique immutable
        alphanumeric identifier of the GPU. It does not correspond to any physical label on
        the board."""
        return self._uuid

    @property
    def bios(self) -> str:
        """str: Returns the BIOS version of the GPU board."""
        return self._bios

    @property
    def memory(self) -> GPUMemoryInfo:
        "GPUMemoryInfo: Returns the GPU board memory info."
        return self._memory_info

    @property
    def utilization(self) -> GPUUtilizationInfo:
        "GPUUtilizationInfo: Returns the GPU board utilization info."
        return self._utilization_info

    @property
    def pci(self) -> GPUPCIInfo:
        "GPUPCIInfo: Returns the GPU board PCI info."
        return self._pci_info

    @property
    def clocks(self) -> GPUClockInfo:
        "GPUClockInfo: Returns the GPU board clocks info."
        return self._clocks_info

    @property
    def power(self) -> GPUPowerInfo:
        "GPUPowerInfo: Returns the GPU board power info."
        return self._power_info

    @property
    def processes(self) -> GPUProcessesInfo:
        "GPUProcessesInfo: Returns the GPU board clocks info."
        return self._processes_info

    def update(self) -> None:
        """
        Updates the GPU attributes.
        """

        device_dict = parser.parser_query_dict(self.index, parser.get_all_info())

        if device_dict is None:
            raise ValueError(f'Invalid device index: {self.index}.')

        self._index = device_dict['index']
        self._name = device_dict['name']
        self._serial = device_dict['serial']
        self._uuid = device_dict['uuid']
        self._bios = device_dict['bios']

        self._memory_info = GPUMemoryInfo(device_dict['memory'])
        self._utilization_info = GPUUtilizationInfo(device_dict['utilization'])
        self._pci_info = GPUPCIInfo(device_dict['pci'])
        self._clocks_info = GPUClockInfo(device_dict['clocks'])
        self._power_info = GPUPowerInfo(device_dict['power'])
        self._processes_info = GPUProcessesInfo(device_dict['processes'])


    def __str__(self):
        ret = f'''{"INDEX":13s}: {self.index}
{"BOARD NAME":13s}: {self.name}
{"SERIAL":13s}: {self.serial}
{"UUID":13s}: {self.uuid}
{"BIOS VERSION":13s}: {self.bios}

{str(self.memory)}

{str(self.utilization)}

{str(self.pci)}

{str(self.clocks)}

{str(self.power)}

{str(self.processes)}
'''
        return textwrap.dedent(ret)
