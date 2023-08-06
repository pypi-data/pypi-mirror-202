#!/usr/bin/python3
# coding=utf-8

import uuid

from ctypes import Structure
from ctypes import Union

from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32
from ctypes import c_uint64

uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32
uint64_t = c_uint64

# static const char bcache_magic[] = {
#       0xc6, 0x85, 0x73, 0xf6, 0x4e, 0x1a, 0x45, 0xca,
#       0x82, 0x65, 0xf5, 0x7f, 0x48, 0xba, 0x6d, 0x81 };
bcache_magic =\
        b'\xc6\x85\x73\xf6\x4e\x1a\x45\xca\x82\x65\xf5\x7f\x48\xba\x6d\x81'

# /*
#  * Version 0: Cache device
#  * Version 1: Backing device
#  * Version 2: Seed pointer into btree node checksum
#  * Version 3: Cache device with new UUID format
#  * Version 4: Backing device with data offset
#  */
BCACHE_SB_VERSION_CDEV = 0
BCACHE_SB_VERSION_BDEV = 1
BCACHE_SB_VERSION_CDEV_WITH_UUID = 3
BCACHE_SB_VERSION_BDEV_WITH_OFFSET = 4
BCACHE_SB_MAX_VERSION = 4

SB_SECTOR = 8
SB_START = SB_SECTOR * 512
SB_LABEL_SIZE = 32
SB_JOURNAL_BUCKETS = 256
BDEV_DATA_START_DEFAULT = 16  # sectors

# BITMASK(CACHE_SYNC,           struct cache_sb, flags, 0, 1);
# BITMASK(CACHE_DISCARD,        struct cache_sb, flags, 1, 1);
# BITMASK(CACHE_REPLACEMENT,    struct cache_sb, flags, 2, 3);
CACHE_REPLACEMENT_LRU = 0
CACHE_REPLACEMENT_FIFO = 1
CACHE_REPLACEMENT_RANDOM = 2
# BITMASK(BDEV_CACHE_MODE,      struct cache_sb, flags, 0, 4);
CACHE_MODE_WRITETHROUGH = 0
CACHE_MODE_WRITEBACK = 1
CACHE_MODE_WRITEAROUND = 2
CACHE_MODE_NONE = 3
# BITMASK(BDEV_STATE,           struct cache_sb, flags, 61, 2);
BDEV_STATE_NONE = 0
BDEV_STATE_CLEAN = 1
BDEV_STATE_DIRTY = 2
BDEV_STATE_STALE = 3

bcache_version_string = {
    BCACHE_SB_VERSION_CDEV: "cache device",
    BCACHE_SB_VERSION_CDEV_WITH_UUID: "cache device",
    BCACHE_SB_VERSION_BDEV: "backing device",
    BCACHE_SB_VERSION_BDEV_WITH_OFFSET: "backing device",
}

cache_replacement_string = {
    CACHE_REPLACEMENT_LRU: "lru",
    CACHE_REPLACEMENT_FIFO: "fifo",
    CACHE_REPLACEMENT_RANDOM: "random",
}

cache_mode_string = {
    CACHE_MODE_WRITETHROUGH: "writethrough",
    CACHE_MODE_WRITEBACK: "writeback",
    CACHE_MODE_WRITEAROUND: "writearound",
    CACHE_MODE_NONE: "no caching",
}

bdev_state_string = {
    BDEV_STATE_NONE: "detached",
    BDEV_STATE_CLEAN: "clean",
    BDEV_STATE_DIRTY: "dirty",
    BDEV_STATE_STALE: "inconsistent",
}


class cache_sb(Structure):

    class _set_uuid(Union):
        _fields_ = [
            ('set_uuid', uint8_t * 16),
            ('set_magic', uint64_t),
        ]

    class _flags(Union):

        class _cache_bit(Structure):
            _fields_ = [
                ('CACHE_SYNC', uint64_t, 1),
                ('CACHE_DISCARD', uint64_t, 1),
                ('CACHE_REPLACEMENT', uint64_t, 3),
            ]

        class _bdev_bit(Structure):
            _fields_ = [
                ('BDEV_CACHE_MODE', uint64_t, 4),
                ('_bit_3_60_', uint64_t, 57),
                ('BDEV_STATE', uint64_t, 2),
            ]

        _fields_ = [
            ('flags', uint64_t),
            ('cache_bit', _cache_bit),
            ('bdev_bit', _bdev_bit),
        ]

    class _device(Union):

        class _cache_device(Structure):
            _fields_ = [
                ('nbuckets', uint64_t),
                ('block_size', uint16_t),
                ('bucket_size', uint16_t),
                ('nr_in_set', uint16_t),
                ('nr_this_dev', uint16_t),
            ]

        class _backing_device(Structure):
            _fields_ = [
                ('data_offset', uint64_t),
            ]

        _fields_ = [
            ('cache', _cache_device),
            ('backing', _backing_device),
        ]

    class _njournal_buckets(Union):
        _fields_ = [
            ('njournal_buckets', uint16_t),
            ('keys', uint16_t),
        ]

    _fields_ = [
        ('csum', uint64_t),
        ('offset', uint64_t),
        ('version', uint64_t),
        ('magic', uint8_t * 16),
        ('uuid', uint8_t * 16),
        ('_set_uuid', _set_uuid),
        ('_label', uint8_t * SB_LABEL_SIZE),
        ('_flags', _flags),
        ('seq', uint64_t),
        ('pad', uint64_t * 8),
        ('_device', _device),
        ('last_mount', uint32_t),
        ('first_bucket', uint16_t),
        ('_njournal_buckets', _njournal_buckets),
        ('d', uint64_t * SB_JOURNAL_BUCKETS),
    ]

    @property
    def label(self) -> str:
        bytes_label = bytes(self._label)
        return bytes_label.decode('utf-8') if bytes_label[0] else "(empty)"

    @property
    def dev_uuid(self) -> uuid.UUID:
        return uuid.UUID(hex=bytes(self.uuid).hex())

    @dev_uuid.setter
    def dev_uuid(self, value: uuid.UUID) -> None:
        assert type(value) is uuid.UUID
        self.uuid = (uint8_t * 16)(*bytes.fromhex(value.hex))

    @property
    def set_uuid(self) -> uuid.UUID:
        return uuid.UUID(hex=bytes(self._set_uuid.set_uuid).hex())

    @set_uuid.setter
    def set_uuid(self, value: uuid.UUID) -> None:
        assert type(value) is uuid.UUID
        self._set_uuid.set_uuid = (uint8_t * 16)(*bytes.fromhex(value.hex))

    @property
    def nbuckets(self) -> uint64_t:
        return self._device.cache.nbuckets

    @nbuckets.setter
    def nbuckets(self, value: uint64_t) -> None:
        self._device.cache.nbuckets = value

    @property
    def block_size(self) -> uint16_t:
        return self._device.cache.block_size

    @block_size.setter
    def block_size(self, value: uint16_t) -> None:
        self._device.cache.block_size = value

    @property
    def bucket_size(self) -> uint16_t:
        return self._device.cache.bucket_size

    @bucket_size.setter
    def bucket_size(self, value: uint16_t) -> None:
        self._device.cache.bucket_size = value

    @property
    def nr_in_set(self) -> uint16_t:
        return self._device.cache.nr_in_set

    @nr_in_set.setter
    def nr_in_set(self, value: uint16_t) -> None:
        self._device.cache.nr_in_set = value

    @property
    def nr_this_dev(self) -> uint16_t:
        return self._device.cache.nr_this_dev

    @nr_this_dev.setter
    def nr_this_dev(self, value: uint16_t) -> None:
        self._device.cache.nr_this_dev = value

    @property
    def data_offset(self) -> uint64_t:
        return self._device.backing.data_offset

    @data_offset.setter
    def data_offset(self, value: uint64_t) -> None:
        self._device.backing.data_offset = value

    @property
    def njournal_buckets(self) -> uint16_t:
        return self._device.njournal_buckets.njournal_buckets

    @njournal_buckets.setter
    def njournal_buckets(self, value: uint16_t) -> None:
        self._device.njournal_buckets.njournal_buckets = value

    @property
    def cache_sync(self) -> uint64_t:
        return self._flags.cache_bit.CACHE_SYNC

    @cache_sync.setter
    def cache_sync(self, value: uint64_t) -> None:
        self._flags.cache_bit.CACHE_SYNC = value

    @property
    def cache_discard(self) -> uint64_t:
        return self._flags.cache_bit.CACHE_DISCARD

    @cache_discard.setter
    def cache_discard(self, value: uint64_t) -> None:
        self._flags.cache_bit.CACHE_DISCARD = value

    @property
    def cache_replacement(self) -> uint64_t:
        return self._flags.cache_bit.CACHE_REPLACEMENT

    @cache_replacement.setter
    def cache_replacement(self, value: uint64_t) -> None:
        self._flags.cache_bit.CACHE_REPLACEMENT = value

    @property
    def bdev_cache_mode(self) -> uint64_t:
        return self._flags.bdev_bit.BDEV_CACHE_MODE

    @bdev_cache_mode.setter
    def bdev_cache_mode(self, value: uint64_t) -> None:
        self._flags.bdev_bit.BDEV_CACHE_MODE = value

    @property
    def bdev_state(self) -> uint64_t:
        return self._flags.bdev_bit.BDEV_STATE

    @bdev_state.setter
    def bdev_state(self, value: uint64_t) -> None:
        self._flags.bdev_bit.BDEV_STATE = value

    @property
    def keys(self) -> uint16_t:
        return self._njournal_buckets.keys


def SB_IS_BDEV(sb: cache_sb) -> bool:
    return sb.version == BCACHE_SB_VERSION_BDEV or\
        sb.version == BCACHE_SB_VERSION_BDEV_WITH_OFFSET


def CACHE_SYNC(sb: cache_sb) -> uint64_t:
    return sb.cache_sync


def SET_CACHE_SYNC(sb: cache_sb, value: uint64_t):
    sb.cache_sync = value


def CACHE_DISCARD(sb: cache_sb) -> uint64_t:
    return sb.cache_discard


def SET_CACHE_DISCARD(sb: cache_sb, value: uint64_t):
    sb.cache_discard = value


def CACHE_REPLACEMENT(sb: cache_sb) -> uint64_t:
    return sb.cache_replacement


def SET_CACHE_REPLACEMENT(sb: cache_sb, value: uint64_t):
    sb.cache_replacement = value


def BDEV_CACHE_MODE(sb: cache_sb) -> uint64_t:
    return sb.bdev_cache_mode


def SET_BDEV_CACHE_MODE(sb: cache_sb, value: uint64_t):
    sb.bdev_cache_mode = value


def BDEV_STATE(sb: cache_sb) -> uint64_t:
    return sb.bdev_state


def SET_BDEV_STATE(sb: cache_sb, value: uint64_t):
    sb.bdev_state = value
