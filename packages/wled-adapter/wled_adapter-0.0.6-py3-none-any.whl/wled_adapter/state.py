from dataclasses import dataclass
from typing import List, Optional, Union

from dataclasses_json import DataClassJsonMixin, config, dataclass_json


class JsonSerializableMixin(DataClassJsonMixin):
    """
    Mixin class for JSON serialization and deserialization of data classes.
    """

    dataclass_json_config = config(exclude=lambda f: f is None)["dataclasses_json"]


@dataclass
class Leds(JsonSerializableMixin):
    """
    Represents LED properties.
    """

    count: Optional[int] = None
    rgbw: Optional[bool] = None
    pin: Optional[List[int]] = None
    pwr: Optional[int] = None
    maxpwr: Optional[int] = None
    maxseg: Optional[int] = None


@dataclass_json
@dataclass
class Info(JsonSerializableMixin):
    """
    Represents information about the WLED device.
    """

    ver: Optional[str] = None
    vid: Optional[int] = None
    leds: Optional[Leds] = None
    name: Optional[str] = None
    udpport: Optional[int] = None
    live: Optional[bool] = None
    fxcount: Optional[int] = None
    palcount: Optional[int] = None
    arch: Optional[str] = None
    core: Optional[str] = None
    freeheap: Optional[int] = None
    uptime: Optional[int] = None
    opt: Optional[int] = None
    brand: Optional[str] = None
    product: Optional[str] = None
    btype: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class Nl(JsonSerializableMixin):
    """
    Represents Nightlight properties.
    """

    on: Optional[bool] = None
    dur: Optional[int] = None
    mode: Optional[int] = None
    tbri: Optional[int] = None
    rem: Optional[int] = None


@dataclass
class Udpn(JsonSerializableMixin):
    """
    Represents UDP notifications properties.
    """

    send: Optional[bool] = None
    recv: Optional[bool] = None
    sgrp: Optional[int] = None
    rgrp: Optional[int] = None


@dataclass
class Seg(JsonSerializableMixin):
    """
    Represents a segment of LEDs.
    """

    id: Optional[int] = None
    start: Optional[int] = None
    stop: Optional[int] = None
    len: Optional[int] = None
    grp: Optional[int] = None
    spc: Optional[int] = None
    of: Optional[int] = None
    on: Optional[bool] = None
    frz: Optional[bool] = None
    bri: Optional[int] = None
    cct: Optional[int] = None
    set: Optional[int] = None
    col: Optional[List[List[int]]] = None
    fx: Optional[int] = None
    sx: Optional[int] = None
    ix: Optional[int] = None
    pal: Optional[int] = None
    c1: Optional[int] = None
    c2: Optional[int] = None
    c3: Optional[int] = None
    sel: Optional[bool] = None
    rev: Optional[bool] = None
    mi: Optional[bool] = None
    o1: Optional[bool] = None
    o2: Optional[bool] = None
    o3: Optional[bool] = None
    si: Optional[int] = None
    m12: Optional[int] = None
    i: Optional[List[Union[int, str]]] = None


@dataclass
class State(JsonSerializableMixin):
    """
    Represents the state of the WLED device.
    """

    off: Optional[bool] = None
    bri: Optional[int] = None
    transition: Optional[int] = None
    ps: Optional[int] = None
    pl: Optional[int] = None
    nl: Optional[Nl] = None
    udpn: Optional[Udpn] = None
    lor: Optional[int] = None
    mainseg: Optional[int] = None
    seg: Optional[List[Seg]] = None


@dataclass
class WledData(JsonSerializableMixin):
    """
    Represents the data structure for WLED device.
    """

    info: Optional[Info] = None
    effects: Optional[List[str]] = None
    palettes: Optional[List[str]] = None
    state: Optional[State] = None
