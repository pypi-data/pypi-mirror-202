#!/usr/bin/python3
# coding=utf-8

import os
import sys
import stat
import struct

from uuid import UUID
from array import array
from fcntl import ioctl

EXIT_FAILURE = 1

BLKGETSIZE = 0x1260
BLKGETSIZE64 = 0x80081272
BLKSSZGET = 0x1268
BLKPBSZGET = 0x127b


def hatoi(s: str) -> int:
    unit = {
        'k': 1024,
        'K': 1024,
        'm': 1024**2,
        'M': 1024**2,
        'g': 1024**3,
        'G': 1024**3,
        't': 1024**4,
        'T': 1024**4,
    }
    times = unit.get(s[-1], 0)
    number = s[:-1] if times else s
    assert number.isnumeric()
    return int(number) * (times if times else 1)


def getblocks(device: str) -> int:
    assert os.path.exists(device) and stat.S_ISBLK(os.stat(device).st_mode)
    try:
        with open(device, 'rb') as fd:
            buf = array('B', [0] * 8)
            ioctl(fd, BLKGETSIZE64, buf)
            block_size = struct.unpack('L', buf)[0]
            return block_size
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        exit(EXIT_FAILURE)


def get_blocksize(device: str) -> int:
    assert os.path.exists(device) and stat.S_ISBLK(os.stat(device).st_mode)
    try:
        # /* check IO limits:
        #  * BLKALIGNOFF: alignment_offset
        #  * BLKPBSZGET: physical_block_size
        #  * BLKSSZGET: logical_block_size
        #  * BLKIOMIN: minimum_io_size
        #  * BLKIOOPT: optimal_io_size
        #  *
        #  * It may be tempting to use physical_block_size,
        #  * or even minimum_io_size.
        #  * But to be as transparent as possible,
        #  * we want to use logical_block_size.
        #  */
        with open(device, 'rb') as fd:
            buf = array('B', [0] * 4)
            ioctl(fd, BLKSSZGET, buf)
            logical_block_size = struct.unpack('I', buf)[0]
            return logical_block_size
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        exit(EXIT_FAILURE)
