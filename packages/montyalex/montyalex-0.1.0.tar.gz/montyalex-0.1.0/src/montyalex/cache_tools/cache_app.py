from typer import Option, Typer

from montyalex.typer_tools import MtaxOrder
from .mtax_cache import MtaxCache
from .timecache_app import time_


cache_: Typer = Typer(name='cache', cls=MtaxOrder)
cache_.add_typer(time_)

@cache_.command(name='add', hidden=True)
def add_(
    *,
    key: str,
    value: str,
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console'),
    timezone: str = 'Etc/Greenwich'):
    """Add a key-value pair in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.add_item((key, value), silent)

@cache_.command(name='incr', hidden=True)
def incr_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Increment an item count in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    return mtax.incr_item(key, silent)

@cache_.command(name='set', hidden=True)
def set_(
    *,
    key: str,
    value: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Sets a key-value pair in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.set_item((key, value), silent)

@cache_.command(name='get', hidden=True)
def get_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Gets a key-value pair from the cache if the key exists"""
    mtax: MtaxCache = MtaxCache(timezone)
    return mtax.get_item(key, silent)

@cache_.command(name='decr', hidden=True)
def decr_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Decrement an item count in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    return mtax.decr_item(key, silent)

@cache_.command(name='clear')
def clear_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Clear all the key-value pairs in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.clear(silent)

@cache_.command(name='reset')
def reset_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
    False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Reset stuck key-value pairs in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.reset(silent)

@cache_.command(name='remove', hidden=True)
def remove_(
    *,
    key: str,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Remove the matching key from the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.remove(key, silent)

@cache_.command(name='list')
def list_(
    *,
    timezone: str = 'Etc/Greenwich',
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """List the key-value pairs stored in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.list_k_v_pairs(silent)

@cache_.command(name='info')
def info_(
    *,
    timezone: str = 'Etc/Greenwich',
    list_items: bool = Option(
        False, '-list', help='List the key-value pairs stored in the cache (list command)'),
    silent: bool = Option(
        False, '-s', show_default='-!s', help='Silence extreneous messages in console')):
    """Shows various info and current size of caches"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax.info(list_items, silent)
