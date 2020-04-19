"""Top-level package Library."""

__author__ = 'Antonio C. Nazare Jr.'
__email__ = 'antonio.nazare@dcc.ufmg.br'
__version__ = '0.1.0'


from igpu.core import count_devices, count_visible_devices
from igpu.core import devices_index, visible_devices_index
from igpu.core import nvidia_driver_version
from igpu.core import get_device, devices, visible_devices
