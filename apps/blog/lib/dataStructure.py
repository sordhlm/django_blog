from ctypes import Structure, c_uint8, c_uint16, c_uint32, c_uint64, Union
from enum import Enum, IntEnum, unique
class NTE(Union): # Error Information
    class bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('debug',      c_uint32, 1),   # LBA Format
            ('sensor',     c_uint32, 1),   # Metadata Settings
            ('remote',     c_uint32, 1),   # Protection information
            ('msg',        c_uint32, 1),   # Protection information
            ('rev',        c_uint32, 29),  #  reserved
        ]
    _anonymous_ = ('bits',)
    _fields_ = [
        ('value', c_uint32),
        ('bits', bits)]

if __name__ == "__main__":
    nte = NTE()
    print(nte.value)
    nte.value = 2
    print(nte.sensor)
