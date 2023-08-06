#!/usr/bin/python3
# coding=utf-8

import argparse
import sys

from .bcache import cache_sb
from .bcache import bcache_magic
from .bcache import SB_SECTOR
from .bcache import BDEV_DATA_START_DEFAULT

from .bcache import BCACHE_SB_VERSION_BDEV

from .bcache import bcache_version_string
from .bcache import cache_replacement_string
from .bcache import cache_mode_string
from .bcache import bdev_state_string

from .bcache import SB_IS_BDEV

from .bcache_super_block import read_super_block


def bcache_super_show(sb: cache_sb):
    assert type(sb) is cache_sb

    _match = bytes(sb.magic) == bcache_magic
    _string = "ok" if _match else "bad magic"
    sys.stdout.write(f"sb.magic\t\t{_string}\n")
    if not _match:
        sys.stderr.write("Invalid superblock (bad magic)\n")
        exit(2)

    _match = sb.offset == SB_SECTOR
    _string = "match" if _match else "expected {}".format(SB_SECTOR)
    sys.stdout.write(f"sb.first_sector\t\t{sb.offset} [{_string}]\n")
    if not _match:
        sys.stderr.write("Invalid superblock (bad sector)\n")
        exit(2)

    sys.stdout.write("sb.csum\t\t\t{:016X} [{}]\n".format(sb.csum, "match"))

    _version = bcache_version_string.get(sb.version, "unknown")
    sys.stdout.write(f"sb.version\t\t{sb.version} [{_version}]\n")
    if _version == "unknown":
        exit(0)

    sys.stdout.write("\n")
    sys.stdout.flush()

    sys.stdout.write(f"dev.label\t\t{sb.label}\n")
    sys.stdout.write(f"dev.uuid\t\t{sb.dev_uuid}\n")
    sys.stdout.write(f"dev.sectors_per_block\t{sb.block_size}\n")
    sys.stdout.write(f"dev.sectors_per_bucket\t{sb.bucket_size}\n")
    if not SB_IS_BDEV(sb):
        _first_sector = sb.bucket_size * sb.first_bucket
        _cache_sectors = sb.bucket_size * (sb.nbuckets - sb.first_bucket)
        _total_sectors = sb.bucket_size * sb.nbuckets
        _cache_sync = "yes" if sb.cache_sync else "no"
        _cache_discard = "yes" if sb.cache_discard else "no"
        sys.stdout.write(f"dev.cache.first_sector\t{_first_sector}\n")
        sys.stdout.write(f"dev.cache.cache_sectors\t{_cache_sectors}\n")
        sys.stdout.write(f"dev.cache.total_sectors\t{_total_sectors}\n")
        sys.stdout.write(f"dev.cache.ordered\t{_cache_sync}\n")
        sys.stdout.write(f"dev.cache.discard\t{_cache_discard}\n")
        sys.stdout.write(f"dev.cache.pos\t\t{sb.nr_this_dev}\n")

        _cache_replacement = sb.cache_replacement
        _substr = cache_replacement_string.get(_cache_replacement, "")
        _string = f" [{_substr}]" if _substr else _substr
        sys.stdout.write(
            f"dev.data.replacement\t{_cache_replacement}{_string}\n")
    else:
        if sb.version == BCACHE_SB_VERSION_BDEV:
            _first_sector = BDEV_DATA_START_DEFAULT
        else:
            if sb.keys == 1 or sb.d[0]:
                sys.stderr.write(
                    "Possible experimental format detected, bailing\n")
                exit(3)
            _first_sector = sb.data_offset
        sys.stdout.write(f"dev.data.first_sector\t{sb.data_offset}\n")

        _bdev_cache_mode = sb.bdev_cache_mode
        _substr = cache_mode_string.get(_bdev_cache_mode, "")
        _string = f" [{_substr}]" if _substr else _substr
        sys.stdout.write(f"dev.data.cache_mode\t{_bdev_cache_mode}{_string}\n")

        _bdev_state = sb.bdev_state
        _substr = bdev_state_string.get(_bdev_state, "")
        _string = f" [{_substr}]" if _substr else _substr
        sys.stdout.write(f"dev.data.cache_state\t{_bdev_state}{_string}\n")

    sys.stdout.write("\n")
    sys.stdout.flush()

    sys.stdout.write(f"cset.uuid\t\t{sb.set_uuid}\n")
    sys.stdout.flush()


def main():
    try:
        parser = argparse.ArgumentParser(prog="bcache-super-show")
        parser.add_argument('device',
                            type=str,
                            nargs=1,
                            help="specify bcache device")
        args = parser.parse_args()
        sb = read_super_block(args.device[0])
        bcache_super_show(sb)
    except KeyboardInterrupt:
        pass
