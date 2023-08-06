#!/usr/bin/python3
# coding=utf-8

import os
import stat

from ctypes import addressof
from ctypes import memmove
from ctypes import sizeof
from ctypes import c_char

from .bcache import cache_sb
from .bcache import SB_START


def read_super_block(device: str) -> cache_sb:
    assert os.path.exists(device) and stat.S_ISBLK(os.stat(device).st_mode)
    with open(device, 'rb') as obj:
        sb = cache_sb()
        length = sizeof(cache_sb)
        # read superblock
        obj.seek(SB_START, 0)
        context = obj.read(length)
        # assignment by memory copy
        rptr = (c_char * length).from_buffer(bytearray(context))
        memmove(addressof(sb), rptr, length)
        return sb


def write_super_block(device: str, sb: cache_sb) -> None:
    assert os.path.exists(device) and stat.S_ISBLK(os.stat(device).st_mode)
    with open(device, 'wb') as obj:
        obj.seek(SB_START, 0)
        # context = bytes(sb)
        # obj.write(context)
