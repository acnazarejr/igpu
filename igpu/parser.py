#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementation of auxiliary parser functions
@author Antonio Carlos Nazare Jr.
@url http://github.com/acnazarejr/igpu
"""

from typing import Dict, List, Optional, Any
import psutil
from pynvml.smi import nvidia_smi as smi

__COMPLET_INFO_FILTER = [
    # Device Identification
    "index", "name", "serial", "uuid", "vbios_version",
    # Memory Info
    "memory.total", "memory.used", "memory.free",
    # Utilization
    "fan.speed", "utilization.gpu", "utilization.memory", "pstate",
    # Temperature
    "temperature.gpu",
    # PCI Info
    "pci.bus_id", "pci.bus", "pci.device", "pci.device_id", "pci.sub_device_id",
    "pcie.link.gen.current", "pcie.link.gen.max", "pcie.link.width.current", "pcie.link.width.max",
    # Clocks info
    "clocks.gr", "clocks.sm", "clocks.mem", "clocks.max.gr", "clocks.max.sm", "clocks.max.mem",
    # Power info
    "power.management", "power.draw", "power.limit", "enforced.power.limit", "power.default_limit",
    "power.min_limit", "power.max_limit",
    # Processes info
    "compute-apps",
]


def get_query_dict(filters: List[str]) -> Dict:
    """get_query_dict"""
    return smi.getInstance().DeviceQuery(', '.join(filters))

def get_all_info() -> Dict:
    """get_all_info"""
    return get_query_dict(__COMPLET_INFO_FILTER)

def parser_query_dict(device_index: int, query_dict: Dict) -> Optional[Dict]:
    """parser_query_dict"""

    for index, device_dict in enumerate(query_dict['gpu']):

        if not index == device_index:
            continue

        parsed_dict: Dict[str, Any] = dict()

        parsed_dict['index'] = index
        parsed_dict['name'] = device_dict['product_name']
        parsed_dict['serial'] = device_dict['serial']
        parsed_dict['uuid'] = device_dict['uuid']
        parsed_dict['bios'] = device_dict['vbios_version']

        parsed_dict['memory'] = dict()
        parsed_dict['memory']['total'] = device_dict['fb_memory_usage']['total']
        parsed_dict['memory']['used'] = device_dict['fb_memory_usage']['used']
        parsed_dict['memory']['free'] = device_dict['fb_memory_usage']['free']
        parsed_dict['memory']['unit'] = device_dict['fb_memory_usage']['unit']

        parsed_dict['utilization'] = dict()
        parsed_dict['utilization']['gpu'] = device_dict['utilization']['gpu_util']
        parsed_dict['utilization']['memory'] = device_dict['utilization']['memory_util']
        parsed_dict['utilization']['fan'] = device_dict['fan_speed']
        parsed_dict['utilization']['performance'] = device_dict['performance_state']
        parsed_dict['utilization']['temperature'] = device_dict['temperature']['gpu_temp']


        parsed_dict['pci'] = dict()
        parsed_dict['pci']['bus'] = device_dict['pci']['pci_bus']
        parsed_dict['pci']['bus_id'] = device_dict['pci']['pci_bus_id']
        parsed_dict['pci']['device'] = device_dict['pci']['pci_device']
        parsed_dict['pci']['device_id'] = device_dict['pci']['pci_device_id']
        parsed_dict['pci']['sub_system_id'] = device_dict['pci']['pci_sub_system_id']
        __aux_dict = device_dict['pci']['pci_gpu_link_info']
        parsed_dict['pci']['current_link_generation'] = __aux_dict['pcie_gen']['current_link_gen']
        parsed_dict['pci']['max_link_generation'] = __aux_dict['pcie_gen']['max_link_gen']
        parsed_dict['pci']['current_link_width'] = __aux_dict['link_widths']['current_link_width']
        parsed_dict['pci']['max_link_width'] = __aux_dict['link_widths']['max_link_width']

        parsed_dict['clocks'] = dict()
        parsed_dict['clocks']['graphics'] = device_dict['clocks']['graphics_clock']
        parsed_dict['clocks']['sm'] = device_dict['clocks']['sm_clock']
        parsed_dict['clocks']['memory'] = device_dict['clocks']['mem_clock']
        parsed_dict['clocks']['max_graphics'] = device_dict['max_clocks']['graphics_clock']
        parsed_dict['clocks']['max_sm'] = device_dict['max_clocks']['sm_clock']
        parsed_dict['clocks']['max_memory'] = device_dict['max_clocks']['mem_clock']
        parsed_dict['clocks']['unit'] = device_dict['clocks']['unit']

        parsed_dict['power'] = dict()
        parsed_dict['power']['management'] = device_dict['power_readings']['power_management']
        parsed_dict['power']['draw'] = device_dict['power_readings']['power_draw']
        parsed_dict['power']['limit'] = device_dict['power_readings']['power_limit']
        parsed_dict['power']['min_limit'] = device_dict['power_readings']['min_power_limit']
        parsed_dict['power']['max_limit'] = device_dict['power_readings']['max_power_limit']

        parsed_dict['processes'] = list()
        if device_dict['processes'] is not None:
            for process_dict in device_dict['processes']:
                _pid = psutil.Process(process_dict['pid'])
                with _pid.oneshot():
                    parsed_dict['processes'].append({
                        'pid': _pid.pid,
                        'name': _pid.name(),
                        'user': _pid.username(),
                        'parent_id': _pid.ppid(),
                        'parent_name': _pid.parent().name(),
                        'create_time': _pid.create_time(),
                        'gpu_memory': process_dict['used_memory'],
                    })

        return parsed_dict

    return None
