#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementation of igpu core
@author Antonio Carlos Nazare Jr.
@url http://github.com/acnazarejr/igpu
"""

import os
from typing import Tuple, List, Optional
from pynvml.smi import nvidia_smi as smi
from igpu import parser
from igpu.gpu_info import GPUInfo

def count_devices() -> int:
    """
    Finds the number of available gpu devices.

    Returns:
        int: The number of available gpus.
    """
    query = smi.getInstance().DeviceQuery('count')
    if query:
        return int(query['count'])
    return 0


def count_visible_devices() -> int:
    """
    Finds the number of visible gpu devices defined by the CUDA_VISIBLE_DEVICES environmnt variable.

    Returns:
        int: The number of visible gpus.
    """
    return len(visible_devices_index())


def devices_index() -> List[int]:
    """
    Get the device index for each available gpu.

    Returns:
        list: A list with all available devices index.
    """
    query = smi.getInstance().DeviceQuery('index')
    if query:
        return list(range(len(query['gpu'])))
    return list()


def visible_devices_index() -> List[int]:
    """
    Get the device index for each visible gpu defined by the CUDA_VISIBLE_DEVICES
    environmnt variable.

    Returns:
        list: A list with all visible devices index.
    """
    visible_devices_env = os.environ.get('CUDA_VISIBLE_DEVICES', None)
    if visible_devices_env is None:
        return list()
    return [int(index) for index in visible_devices_env.split(sep=',')]


def nvidia_driver_version() -> Tuple[Optional[int], Optional[int]]:
    """
    Find the version of nvidia driver.

    Returns:
        tuple: A tuple with major and minor driver version.
    """
    query = smi.getInstance().DeviceQuery('driver_version')
    if query:
        _version = query['driver_version'].split('.')
        return int(_version[0]), int(_version[1])
    return None, None


def get_device(device_index: int) -> GPUInfo:
    """
    Given a device index, returns a GpuInfo object containing the device infos and stats.

    Args:
        device_index (int): The index of desired device.

    Returns:
        GpuInfo: A GpuInfo object with device info.
    """
    if count_devices() == 0:
        raise ValueError(f'There are no devices available')

    device_dict = parser.parser_query_dict(device_index, parser.get_all_info())
    if device_dict is None:
        raise ValueError(f'Invalid device index: {device_index}. Valid: {devices_index()}')
    return GPUInfo(device_dict)


def devices() -> List[GPUInfo]:
    """
    Returns a list of GpuInfo object of all available devices.


    Returns:
        list: A list of GpuInfo objects.
    """
    all_info = parser.get_all_info()
    ret_devices = list()
    for device_index in devices_index():
        device_dict = parser.parser_query_dict(device_index, all_info)
        if device_dict is None:
            raise ValueError(f'Invalid device index: {device_index}')
        ret_devices.append(GPUInfo(device_dict))
    return ret_devices

def visible_devices() -> List[GPUInfo]:
    """
    Returns a list of GpuInfo object of the visible devices.


    Returns:
        list: A list of GpuInfo objects.
    """
    all_info = parser.get_all_info()
    ret_devices = list()
    for device_index in visible_devices_index():
        device_dict = parser.parser_query_dict(device_index, all_info)
        if device_dict is None:
            raise ValueError(f'Invalid device index: {device_index}')
        ret_devices.append(GPUInfo(device_dict))
    return ret_devices
