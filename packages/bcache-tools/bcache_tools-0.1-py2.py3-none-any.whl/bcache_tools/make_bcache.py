#!/usr/bin/python3
# coding=utf-8

import sys
import uuid
import blkid

from ctypes import addressof
from ctypes import memmove
from ctypes import memset
from ctypes import sizeof

from xarg import xarg, Namespace

from .bcache import cache_sb
from .bcache import bcache_magic
from .bcache import SB_SECTOR
from .bcache import BDEV_DATA_START_DEFAULT

from .bcache import BCACHE_SB_VERSION_CDEV
from .bcache import BCACHE_SB_VERSION_BDEV
from .bcache import BCACHE_SB_VERSION_BDEV_WITH_OFFSET

from .bcache import CACHE_MODE_WRITETHROUGH
from .bcache import CACHE_MODE_WRITEBACK

from .bcache import cache_replacement_string

from .bcache import SB_IS_BDEV
from .bcache import SET_CACHE_DISCARD
from .bcache import SET_CACHE_REPLACEMENT
from .bcache import SET_BDEV_CACHE_MODE

from .bcache_util import EXIT_FAILURE
from .bcache_util import hatoi
from .bcache_util import getblocks
from .bcache_util import get_blocksize

from .bcache_super_block import read_super_block
from .bcache_super_block import write_super_block


def make_bcache(device: str, **kwargs) -> None:
    bdev = kwargs.get("bdev", True)
    dev_uuid = uuid.uuid4()
    set_uuid = kwargs.get("cset_uuid", uuid.uuid4())
    block_size = kwargs.get("block_size", 512)
    bucket_size = kwargs.get("bucket_size", 4096)
    data_offset = kwargs.get("data_offset", BDEV_DATA_START_DEFAULT)
    discard = kwargs.get("discard", False)
    writeback = kwargs.get("writeback", False)
    wipe_bcache = kwargs.get("wipe_bcache", False)
    cache_replacement_policy = kwargs.get("cache_replacement_policy", 0)

    sb = read_super_block(device)
    if bytes(sb.magic) == bcache_magic and not wipe_bcache:
        sys.stderr.write(f"Already a bcache device on {device}, "
                         f"overwrite with --wipe-bcache\n")
        exit(EXIT_FAILURE)

    # blikid probe
    pr = blkid.Probe()
    pr.set_device(device)
    pr.enable_partitions(True)
    # pr.enable_superblocks(True)
    # pr.set_superblocks_flags(blkid.SUBLKS_TYPE | blkid.SUBLKS_USAGE | blkid.SUBLKS_UUID)
    if pr.do_safeprobe():
        sys.stderr.write(f"Device {device} already has a non-bcache superblock"
                         f", remove it using wipefs and wipefs -a\n")
        exit(EXIT_FAILURE)

    memset(addressof(sb), 0, sizeof(cache_sb))

    sb.offset = SB_SECTOR
    sb.version = BCACHE_SB_VERSION_BDEV if bdev else BCACHE_SB_VERSION_CDEV

    memmove(addressof(sb.magic), bcache_magic, 16)
    assert type(dev_uuid) is uuid.UUID
    assert type(set_uuid) is uuid.UUID
    sb.dev_uuid = dev_uuid
    sb.set_uuid = set_uuid

    sb.block_size = int(block_size / 512)
    sb.bucket_size = int(bucket_size / 512)

    if SB_IS_BDEV(sb):
        _wb = CACHE_MODE_WRITEBACK if writeback else CACHE_MODE_WRITETHROUGH
        SET_BDEV_CACHE_MODE(sb, _wb)

        if data_offset != BDEV_DATA_START_DEFAULT:
            sb.version = BCACHE_SB_VERSION_BDEV_WITH_OFFSET
            sb.data_offset = data_offset

        sys.stdout.write(f"device:\t\t\t{device}\n"
                         f"UUID:\t\t\t{sb.dev_uuid}\n"
                         f"Set UUID:\t\t{sb.set_uuid}\n"
                         f"version:\t\t{sb.version}\n"
                         f"block_size:\t\t{sb.block_size}\n"
                         f"data_offset:\t\t{sb.data_offset}\n")
    else:
        sb.nbuckets = int(getblocks(device) / sb.bucket_size)
        sb.nr_in_set = 1
        sb.first_bucket = int(23 / sb.bucket_size) + 1

        if sb.nbuckets < 1 << 7:
            sys.stderr.write(
                f"Not enough buckets: {sb.nbuckets}, need {1 << 7}\n")
            exit(EXIT_FAILURE)

        SET_CACHE_DISCARD(sb, discard)
        SET_CACHE_REPLACEMENT(sb, cache_replacement_policy)

        sys.stdout.write(f"device:\t\t\t{device}\n"
                         f"UUID:\t\t\t{sb.dev_uuid}\n"
                         f"Set UUID:\t\t{sb.set_uuid}\n"
                         f"version:\t\t{sb.version}\n"
                         f"nbuckets:\t\t{sb.nbuckets}\n"
                         f"block_size:\t\t{sb.block_size}\n"
                         f"bucket_size:\t\t{sb.bucket_size}\n"
                         f"nr_in_set:\t\t{sb.nr_in_set}\n"
                         f"nr_this_dev:\t\t{sb.nr_this_dev}\n"
                         f"first_bucket:\t\t{sb.first_bucket}\n")

    # write superblock
    write_super_block(device, sb)


def add_cmd_make_bcache(_arg: xarg) -> None:
    _arg.add_opt('-C',
                 '--cache',
                 nargs='+',
                 default=[],
                 help="Format a cache device")
    _arg.add_opt('-B',
                 '--bdev',
                 nargs='+',
                 default=[],
                 help="Format a backing device")
    _arg.add_opt('-b',
                 '--bucket',
                 type=str,
                 default="1024",
                 help="bucket size")
    _arg.add_opt('-w',
                 '--block',
                 type=str,
                 default="0",
                 help="block size (hard sector size of SSD, often 2k)")
    _arg.add_opt('-o', '--data-offset', help="data offset in sectors")
    _arg.add_opt('-u', '--cset-uuid', help="UUID for the cache set")
    _arg.add_opt_on('--wipe-bcache', help="enable wipe bcache")
    _arg.add_opt_on('--writeback', help="enable writeback")
    _arg.add_opt_on('--discard', help="enable discards")
    _arg.add_opt('--cache_replacement_policy',
                 choices=["lru", "fifo", "random"])


def run_cmd_make_bcache(args: Namespace) -> None:
    if args.debug:
        sys.stdout.write(f"{args}\n")

    block_size = hatoi(args.block)
    bucket_size = hatoi(args.bucket)

    for dev in args.bdev:
        block_size = max(get_blocksize(dev), block_size)
    for dev in args.cache:
        block_size = max(get_blocksize(dev), block_size)

    if bucket_size < block_size:
        sys.stderr.write("Bucket size cannot be smaller than block size\n")
        exit(EXIT_FAILURE)

    kwargs = {
        "block_size": block_size,
        "bucket_size": bucket_size,
        "discard": args.discard,
        "writeback": args.writeback,
        "wipe_bcache": args.wipe_bcache,
    }

    if args.cset_uuid is not None:
        try:
            cset_uuid = uuid.UUID(args.cset_uuid)
            kwargs["cset_uuid"] = cset_uuid
        except Exception:
            sys.stderr.write("Bad uuid\n")
            exit(EXIT_FAILURE)

    if args.cache_replacement_policy is not None:
        for key, value in cache_replacement_string.items():
            if args.cache_replacement_policy == value:
                kwargs["cache_replacement_policy"] = key

    kwargs["bdev"] = True
    for dev in args.bdev:
        make_bcache(dev, **kwargs)

    kwargs["bdev"] = False
    for dev in args.cache:
        make_bcache(dev, **kwargs)


def main():
    try:
        _arg = xarg("make-bcache", epilog="Powered by bcache-tools-python")
        _arg.add_opt_on('-d', '--debug', help="enable debug")
        add_cmd_make_bcache(_arg)
        args = _arg.parse_args()
        run_cmd_make_bcache(args)
    except KeyboardInterrupt:
        pass
