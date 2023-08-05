# -*- coding: utf-8 -*-
"""
Geometry
"""


from abc import abstractmethod
from functools import lru_cache, reduce
from math import isnan, nan
from operator import add
from struct import pack, unpack
from typing import List, Tuple

from fudgeo.constant import (
    COORDINATES, COUNT_CODE, DOUBLE, EMPTY, ENVELOPE_OFFSET, FOUR_D,
    FOUR_D_PACK_CODE, FOUR_D_UNPACK_CODE, GP_MAGIC, HEADER_OFFSET, HEADER_CODE,
    POINT_PREFIX, QUADRUPLE, THREE_D, THREE_D_PACK_CODE, THREE_D_UNPACK_CODE,
    TRIPLE, TWO_D, TWO_D_PACK_CODE, TWO_D_UNPACK_CODE, WGS84,
    WKB_LINESTRING_M_PRE, WKB_LINESTRING_PRE, WKB_LINESTRING_ZM_PRE,
    WKB_LINESTRING_Z_PRE, WKB_MULTI_LINESTRING_M_PRE, WKB_MULTI_LINESTRING_PRE,
    WKB_MULTI_LINESTRING_ZM_PRE, WKB_MULTI_LINESTRING_Z_PRE,
    WKB_MULTI_POINT_M_PRE, WKB_MULTI_POINT_PRE, WKB_MULTI_POINT_ZM_PRE,
    WKB_MULTI_POINT_Z_PRE, WKB_MULTI_POLYGON_M_PRE, WKB_MULTI_POLYGON_PRE,
    WKB_MULTI_POLYGON_ZM_PRE, WKB_MULTI_POLYGON_Z_PRE, WKB_POINT_M_PRE,
    WKB_POINT_PRE, WKB_POINT_ZM_PRE, WKB_POINT_Z_PRE, WKB_POLYGON_M_PRE,
    WKB_POLYGON_PRE, WKB_POLYGON_ZM_PRE, WKB_POLYGON_Z_PRE)


__all__ = ['Point', 'PointZ', 'PointM', 'PointZM', 'MultiPoint', 'MultiPointZ',
           'MultiPointM', 'MultiPointZM', 'LineString', 'LineStringZ',
           'LineStringM', 'LineStringZM', 'MultiLineString', 'MultiLineStringZ',
           'MultiLineStringM', 'MultiLineStringZM', 'Polygon', 'PolygonZ',
           'PolygonM', 'PolygonZM', 'MultiPolygon', 'MultiPolygonZ',
           'MultiPolygonM', 'MultiPolygonZM']


def _unpack_line(value: bytes, dimension: int,
                 is_ring: bool = False) -> List[Tuple[float, ...]]:
    """
    Unpack Values for LineString
    """
    count, data = _get_count_and_data(value, is_ring=is_ring)
    total = dimension * count
    values: Tuple[float, ...] = unpack(f'<{total}d', data)
    return [values[i:i + dimension] for i in range(0, total, dimension)]
# End _unpack_line function


def _unpack_points(value: bytes, dimension: int) -> List[Tuple[float, ...]]:
    """
    Unpack Values for Multi Point
    """
    offset = 5
    size = (8 * dimension) + offset
    count, data = _get_count_and_data(value)
    if not count:
        return []
    total = dimension * count
    data = [data[i + offset:i + size] for i in range(0, len(data), size)]
    values: Tuple[float, ...] = unpack(f'<{total}d', reduce(add, data))
    return [values[i:i + dimension] for i in range(0, total, dimension)]
# End _unpack_points function


def _pack_points(coordinates: COORDINATES, has_z: bool = False,
                 has_m: bool = False, use_prefix: bool = False) -> bytes:
    """
    Pack Coordinates
    """
    flat = []
    for coords in coordinates:
        flat.extend(coords)
    count = len(coordinates)
    total = count * sum((TWO_D, has_z, has_m))
    data = pack(f'<{total}d', *flat)
    if not use_prefix:
        return pack(COUNT_CODE, count) + data
    length = len(data)
    step = length // count
    prefix = POINT_PREFIX.get((has_z, has_m))
    parts = [prefix + data[i:i + step] for i in range(0, length, step)]
    return pack(COUNT_CODE, count) + EMPTY.join(parts)
# End _pack_points function


def _unpack_lines(value: bytes, dimension: int, is_ring: bool = False) \
        -> List[List[Tuple[float, ...]]]:
    """
    Unpack Values for Multi LineString and Polygons
    """
    size, last_end = 8 * dimension, 0
    offset, unit = (4, COUNT_CODE) if is_ring else (9, '<BII')
    count, data = _get_count_and_data(value)
    lines = []
    for _ in range(count):
        *_, length = unpack(unit, data[last_end:last_end + offset])
        end = last_end + offset + (size * length)
        # noinspection PyTypeChecker
        points: List[Tuple[float, ...]] = _unpack_line(
            data[last_end:end], dimension, is_ring=is_ring)
        last_end = end
        lines.append(points)
    return lines
# End _unpack_lines function


def _unpack_polygons(value: bytes, dimension: int) \
        -> List[List[List[Tuple[float, ...]]]]:
    """
    Unpack Values for Multi Polygon Type Containing Polygons
    """
    size, last_end = 8 * dimension, 0
    count, data = _get_count_and_data(value)
    polygons = []
    for _ in range(0, count):
        points = _unpack_lines(data[last_end:], dimension, is_ring=True)
        point_count = sum(len(x) for x in points)
        last_end += (point_count * size) + (len(points) * 4) + 9
        polygons.append(points)
    return polygons
# End _unpack_polygons method


def _get_count_and_data(value: bytes, is_ring: bool = False) \
        -> Tuple[int, bytes]:
    """
    Get Count from header and return the value portion of the stream
    """
    first, second = (0, 4) if is_ring else (5, 9)
    header, data = value[first: second], value[second:]
    count, = unpack(COUNT_CODE, header)
    return count, data
# End _get_count_and_data function


@lru_cache(maxsize=None)
def _make_header(srs_id: int, is_empty: bool) -> bytes:
    """
    Cached Creation of a GeoPackage Geometry Header
    """
    flags = 1
    if is_empty:
        flags |= (1 << 4)
    return pack(HEADER_CODE, GP_MAGIC, 0, flags, srs_id)
# End _make_header function


@lru_cache(maxsize=None)
def _unpack_header(value: bytes) -> Tuple[int, int, bool]:
    """
    Cached Unpacking of a GeoPackage Geometry Header
    """
    _, _, flags, srs_id = unpack(HEADER_CODE, value)
    envelope_code = (flags & (0x07 << 1)) >> 1
    is_empty = bool((flags & (0x01 << 4)) >> 4)
    return srs_id, ENVELOPE_OFFSET[envelope_code], is_empty
# End _unpack_header function


class AbstractGeometry:
    """
    Abstract Geometry
    """
    __slots__ = 'srs_id',

    def __init__(self, srs_id: int) -> None:
        """
        Initialize the Point class
        """
        super().__init__()
        self.srs_id: int = srs_id
    # End init built-in

    @staticmethod
    def _join_geometries(geoms: List['AbstractGeometry']) -> bytes:
        """
        Join Geometries
        """
        return reduce(add, [geom.to_wkb() for geom in geoms], EMPTY)
    # End _join_geometries method

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        pass
    # End is_empty property

    @abstractmethod
    def to_wkb(self, use_prefix: bool = True) -> bytes:  # pragma: nocover
        """
        To WKB
        """
        pass
    # End to_wkb method

    @classmethod
    @abstractmethod
    def from_wkb(cls, wkb: bytes) -> 'AbstractGeometry':  # pragma: nocover
        """
        From WKB
        """
        pass
    # End from_wkb method

    def to_gpkg(self) -> bytes:
        """
        To Geopackage
        """
        return (
            _make_header(srs_id=self.srs_id, is_empty=self.is_empty) +
            self.to_wkb())
    # End to_gpkg method

    @classmethod
    @abstractmethod
    def from_gpkg(cls, value: bytes) -> 'AbstractGeometry':  # pragma: nocover
        """
        From Geopackage
        """
        pass
    # End from_gpkg method
# End AbstractGeometry class


class Point(AbstractGeometry):
    """
    Point
    """
    __slots__ = 'x', 'y'

    def __init__(self, *, x: float, y: float, srs_id: int = WGS84) -> None:
        """
        Initialize the Point class
        """
        super().__init__(srs_id=srs_id)
        self.x: float = x
        self.y: float = y
    # End init built-in

    def __eq__(self, other: 'Point') -> bool:
        """
        Equals
        """
        if not isinstance(other, Point):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return (self.x, self.y) == (other.x, other.y)
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return isnan(self.x) and isnan(self.y)
    # End is_empty property

    @staticmethod
    def _unpack(value: bytes) -> DOUBLE:
        """
        Unpack Values
        """
        *_, x, y = unpack(TWO_D_UNPACK_CODE, value)
        return x, y
    # End _unpack method

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        pre = WKB_POINT_PRE if use_prefix else EMPTY
        return pre + pack(TWO_D_PACK_CODE, self.x, self.y)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'Point':
        """
        From WKB
        """
        x, y = cls._unpack(wkb)
        return cls(x=x, y=y)
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'Point':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls.empty(srs_id)
        x, y = cls._unpack(value[offset:])
        return cls(x=x, y=y, srs_id=srs_id)
    # End from_gpkg method

    @classmethod
    def from_tuple(cls, xy: DOUBLE, srs_id: int = WGS84) -> 'Point':
        """
        From Tuple
        """
        x, y = xy
        return cls(x=x, y=y, srs_id=srs_id)
    # End from_tuple method

    @classmethod
    def empty(cls, srs_id: int = WGS84) -> 'Point':
        """
        Empty Point
        """
        return cls(x=nan, y=nan, srs_id=srs_id)
    # End empty method
# End Point class


class PointZ(AbstractGeometry):
    """
    Point Z
    """
    __slots__ = 'x', 'y', 'z'

    def __init__(self, *, x: float, y: float, z: float,
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PointZ class
        """
        super().__init__(srs_id=srs_id)
        self.x: float = x
        self.y: float = y
        self.z: float = z
    # End init built-in

    def __eq__(self, other: 'PointZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, PointZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return isnan(self.x) and isnan(self.y) and isnan(self.z)
    # End is_empty property

    @staticmethod
    def _unpack(value: bytes) -> TRIPLE:
        """
        Unpack Values
        """
        *_, x, y, z = unpack(THREE_D_UNPACK_CODE, value)
        return x, y, z
    # End _unpack method

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        pre = WKB_POINT_Z_PRE if use_prefix else EMPTY
        return pre + pack(THREE_D_PACK_CODE, self.x, self.y, self.z)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PointZ':
        """
        From WKB
        """
        x, y, z = cls._unpack(wkb)
        return cls(x=x, y=y, z=z)
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PointZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls.empty(srs_id)
        x, y, z = cls._unpack(value[offset:])
        return cls(x=x, y=y, z=z, srs_id=srs_id)
    # End from_gpkg method

    @classmethod
    def from_tuple(cls, xyz: TRIPLE, srs_id: int = WGS84) -> 'PointZ':
        """
        From Tuple
        """
        x, y, z = xyz
        return cls(x=x, y=y, z=z, srs_id=srs_id)
    # End from_tuple method

    @classmethod
    def empty(cls, srs_id: int = WGS84) -> 'PointZ':
        """
        Empty PointZ
        """
        return cls(x=nan, y=nan, z=nan, srs_id=srs_id)
    # End empty method
# End PointZ class


class PointM(AbstractGeometry):
    """
    Point M
    """
    __slots__ = 'x', 'y', 'm'

    def __init__(self, *, x: float, y: float, m: float,
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PointM class
        """
        super().__init__(srs_id=srs_id)
        self.x: float = x
        self.y: float = y
        self.m: float = m
    # End init built-in

    def __eq__(self, other: 'PointM') -> bool:
        """
        Equals
        """
        if not isinstance(other, PointM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return (self.x, self.y, self.m) == (other.x, other.y, other.m)
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return isnan(self.x) and isnan(self.y) and isnan(self.m)
    # End is_empty property

    @staticmethod
    def _unpack(value: bytes) -> TRIPLE:
        """
        Unpack Values
        """
        *_, x, y, m = unpack(THREE_D_UNPACK_CODE, value)
        return x, y, m
    # End _unpack method

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        pre = WKB_POINT_M_PRE if use_prefix else EMPTY
        return pre + pack(THREE_D_PACK_CODE, self.x, self.y, self.m)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PointM':
        """
        From WKB
        """
        x, y, m = cls._unpack(wkb)
        return cls(x=x, y=y, m=m)
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PointM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls.empty(srs_id)
        x, y, m = cls._unpack(value[offset:])
        return cls(x=x, y=y, m=m, srs_id=srs_id)
    # End from_gpkg method

    @classmethod
    def from_tuple(cls, xym: TRIPLE, srs_id: int = WGS84) -> 'PointM':
        """
        From Tuple
        """
        x, y, m = xym
        return cls(x=x, y=y, m=m, srs_id=srs_id)
    # End from_tuple method

    @classmethod
    def empty(cls, srs_id: int = WGS84) -> 'PointM':
        """
        Empty PointM
        """
        return cls(x=nan, y=nan, m=nan, srs_id=srs_id)
    # End empty method
# End PointM class


class PointZM(AbstractGeometry):
    """
    Point ZM
    """
    __slots__ = 'x', 'y', 'z', 'm'

    def __init__(self, *, x: float, y: float, z: float, m: float,
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PointZM class
        """
        super().__init__(srs_id=srs_id)
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.m: float = m
    # End init built-in

    def __eq__(self, other: 'PointZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, PointZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return (self.x, self.y, self.z, self.m) == (
            other.x, other.y, other.z, other.m)
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return (isnan(self.x) and isnan(self.y) and
                isnan(self.z) and isnan(self.m))
    # End is_empty property

    @staticmethod
    def _unpack(value: bytes) -> QUADRUPLE:
        """
        Unpack Values
        """
        *_, x, y, z, m = unpack(FOUR_D_UNPACK_CODE, value)
        return x, y, z, m
    # End _unpack method

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        pre = WKB_POINT_ZM_PRE if use_prefix else EMPTY
        return pre + pack(FOUR_D_PACK_CODE, self.x, self.y, self.z, self.m)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PointZM':
        """
        From WKB
        """
        x, y, z, m = cls._unpack(wkb)
        return cls(x=x, y=y, z=z, m=m)
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PointZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls.empty(srs_id)
        x, y, z, m = cls._unpack(value[offset:])
        return cls(x=x, y=y, z=z, m=m, srs_id=srs_id)
    # End from_gpkg method

    @classmethod
    def from_tuple(cls, xyzm: QUADRUPLE, srs_id: int = WGS84) -> 'PointZM':
        """
        From Tuple
        """
        x, y, z, m = xyzm
        return cls(x=x, y=y, z=z, m=m, srs_id=srs_id)
    # End from_tuple method

    @classmethod
    def empty(cls, srs_id: int = WGS84) -> 'PointZM':
        """
        Empty Point
        """
        return cls(x=nan, y=nan, z=nan, m=nan, srs_id=srs_id)
    # End empty method
# End PointZM class


class MultiPoint(AbstractGeometry):
    """
    Multi Point
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[DOUBLE], srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPoint class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[DOUBLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'MultiPoint') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPoint):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[Point]:
        """
        Points
        """
        return [Point(x=x, y=y) for x, y in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_MULTI_POINT_PRE + _pack_points(
            self.coordinates, use_prefix=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPoint':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_points(wkb, dimension=TWO_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPoint':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_points(
            value[offset:], dimension=TWO_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPoint class


class MultiPointZ(AbstractGeometry):
    """
    Multi Point Z
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPointZ class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'MultiPointZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPointZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointZ]:
        """
        Points
        """
        return [PointZ(x=x, y=y, z=z) for x, y, z in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_MULTI_POINT_Z_PRE + _pack_points(
            self.coordinates, has_z=True, use_prefix=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPointZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_points(wkb, dimension=3))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPointZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_points(value[offset:], dimension=3), srs_id=srs_id)
    # End from_gpkg method
# End MultiPointZ class


class MultiPointM(AbstractGeometry):
    """
    Multi Point M
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPointM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'MultiPointM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPointM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointM]:
        """
        Points
        """
        return [PointM(x=x, y=y, m=m) for x, y, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_MULTI_POINT_M_PRE + _pack_points(
            self.coordinates, has_m=True, use_prefix=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPointM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_points(wkb, dimension=3))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPointM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_points(value[offset:], dimension=3), srs_id=srs_id)
    # End from_gpkg method
# End MultiPointM class


class MultiPointZM(AbstractGeometry):
    """
    Multi Point ZM
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[QUADRUPLE],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPointZM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[QUADRUPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'MultiPointZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPointZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointZM]:
        """
        Points
        """
        return [PointZM(x=x, y=y, z=z, m=m) for x, y, z, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_MULTI_POINT_ZM_PRE + _pack_points(
            self.coordinates, has_z=True, has_m=True, use_prefix=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPointZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_points(wkb, dimension=FOUR_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPointZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_points(
            value[offset:], dimension=FOUR_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPointZM class


class LineString(AbstractGeometry):
    """
    LineString
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[DOUBLE], srs_id: int = WGS84) -> None:
        """
        Initialize the LineString class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[DOUBLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LineString') -> bool:
        """
        Equals
        """
        if not isinstance(other, LineString):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[Point]:
        """
        Points
        """
        return [Point(x=x, y=y) for x, y in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_LINESTRING_PRE + _pack_points(self.coordinates)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LineString':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=TWO_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LineString':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_line(value[offset:], dimension=TWO_D), srs_id=srs_id)
    # End from_gpkg method
# End LineString class


class LineStringZ(AbstractGeometry):
    """
    LineStringZ
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the LineStringZ class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LineStringZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, LineStringZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointZ]:
        """
        Points
        """
        return [PointZ(x=x, y=y, z=z) for x, y, z in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_LINESTRING_Z_PRE + _pack_points(self.coordinates, has_z=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LineStringZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=3))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LineStringZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_line(value[offset:], dimension=3), srs_id=srs_id)
    # End from_gpkg method
# End LineStringZ class


class LineStringM(AbstractGeometry):
    """
    LineStringM
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the LineStringM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LineStringM') -> bool:
        """
        Equals
        """
        if not isinstance(other, LineStringM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointM]:
        """
        Points
        """
        return [PointM(x=x, y=y, m=m) for x, y, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_LINESTRING_M_PRE + _pack_points(self.coordinates, has_m=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LineStringM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=3))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LineStringM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_line(
            value[offset:], dimension=THREE_D), srs_id=srs_id)
    # End from_gpkg method
# End LineStringM class


class LineStringZM(AbstractGeometry):
    """
    LineStringZM
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[QUADRUPLE],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the LineStringZM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[QUADRUPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LineStringZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, LineStringZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointZM]:
        """
        Points
        """
        return [PointZM(x=x, y=y, z=z, m=m) for x, y, z, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return WKB_LINESTRING_ZM_PRE + _pack_points(
            self.coordinates, has_z=True, has_m=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LineStringZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=FOUR_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LineStringZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_line(
            value[offset:], dimension=FOUR_D), srs_id=srs_id)
    # End from_gpkg method
# End LineStringZM class


class MultiLineString(AbstractGeometry):
    """
    Multi LineString
    """
    __slots__ = 'lines',

    def __init__(self, coordinates: List[List[DOUBLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiLineString class
        """
        super().__init__(srs_id=srs_id)
        self.lines: List[LineString] = [
            LineString(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiLineString') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiLineString):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.lines == other.lines
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.lines)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.lines
        return (WKB_MULTI_LINESTRING_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiLineString':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=TWO_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiLineString':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=TWO_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiLineString class


class MultiLineStringZ(AbstractGeometry):
    """
    Multi LineString Z
    """
    __slots__ = 'lines',

    def __init__(self, coordinates: List[List[TRIPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiLineStringZ class
        """
        super().__init__(srs_id=srs_id)
        self.lines: List[LineStringZ] = [
            LineStringZ(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiLineStringZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiLineStringZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.lines == other.lines
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.lines)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.lines
        return (WKB_MULTI_LINESTRING_Z_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiLineStringZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=THREE_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiLineStringZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=THREE_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiLineStringZ class


class MultiLineStringM(AbstractGeometry):
    """
    Multi LineString M
    """
    __slots__ = 'lines',

    def __init__(self, coordinates: List[List[TRIPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiLineStringM class
        """
        super().__init__(srs_id=srs_id)
        self.lines: List[LineStringM] = [
            LineStringM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiLineStringM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiLineStringM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.lines == other.lines
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.lines)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.lines
        return (WKB_MULTI_LINESTRING_M_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiLineStringM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=THREE_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiLineStringM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=THREE_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiLineStringM class


class MultiLineStringZM(AbstractGeometry):
    """
    Multi LineString ZM
    """
    __slots__ = 'lines',

    def __init__(self, coordinates: List[List[QUADRUPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiLineStringZM class
        """
        super().__init__(srs_id=srs_id)
        self.lines: List[LineStringZM] = [
            LineStringZM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiLineStringZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiLineStringZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.lines == other.lines
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.lines)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.lines
        return (WKB_MULTI_LINESTRING_ZM_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiLineStringZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=FOUR_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiLineStringZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=FOUR_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiLineStringZM class


class LinearRing(AbstractGeometry):
    """
    Linear Ring
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[DOUBLE],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the LinearRing class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[DOUBLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LinearRing') -> bool:
        """
        Equals
        """
        if not isinstance(other, LinearRing):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[Point]:
        """
        Points
        """
        return [Point(x=x, y=y) for x, y in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return _pack_points(self.coordinates)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LinearRing':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=TWO_D, is_ring=True))
    # End from_wkb method

    def to_gpkg(self) -> bytes:
        """
        To Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End to_gpkg method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LinearRing':
        """
        From Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End from_gpkg method
# End LinearRing class


class LinearRingZ(AbstractGeometry):
    """
    Linear Ring Z
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the LinearRingZ class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LinearRingZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, LinearRingZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointZ]:
        """
        Points
        """
        return [PointZ(x=x, y=y, z=z) for x, y, z in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return _pack_points(self.coordinates, has_z=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LinearRingZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=THREE_D, is_ring=True))
    # End from_wkb method

    def to_gpkg(self) -> bytes:
        """
        To Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End to_gpkg method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LinearRingZ':
        """
        From Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End from_gpkg method
# End LinearRingZ class


class LinearRingM(AbstractGeometry):
    """
    Linear Ring M
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[TRIPLE], srs_id: int = WGS84) -> None:
        """
        Initialize the LinearRingM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[TRIPLE] = coordinates
    # End init built-in

    def __eq__(self, other: 'LinearRingM') -> bool:
        """
        Equals
        """
        if not isinstance(other, LinearRingM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    @property
    def points(self) -> List[PointM]:
        """
        Points
        """
        return [PointM(x=x, y=y, m=m) for x, y, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return _pack_points(self.coordinates, has_m=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LinearRingM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=THREE_D, is_ring=True))
    # End from_wkb method

    def to_gpkg(self) -> bytes:
        """
        To Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End to_gpkg method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LinearRingM':
        """
        From Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End from_gpkg method
# End LinearRingM class


class LinearRingZM(AbstractGeometry):
    """
    Linear Ring ZM
    """
    __slots__ = 'coordinates',

    def __init__(self, coordinates: List[QUADRUPLE],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the LinearRingZM class
        """
        super().__init__(srs_id=srs_id)
        self.coordinates: List[QUADRUPLE] = coordinates
    # End init built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.coordinates)
    # End is_empty property

    def __eq__(self, other: 'LinearRingZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, LinearRingZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.points == other.points
    # End eq built-in

    @property
    def points(self) -> List[PointZM]:
        """
        Points
        """
        return [PointZM(x=x, y=y, z=z, m=m) for x, y, z, m in self.coordinates]
    # End points property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        return _pack_points(self.coordinates, has_z=True, has_m=True)
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'LinearRingZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_line(wkb, dimension=FOUR_D, is_ring=True))
    # End from_wkb method

    def to_gpkg(self) -> bytes:
        """
        To Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End to_gpkg method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'LinearRingZM':
        """
        From Geopackage
        """
        raise NotImplementedError('Linear Rings not supported for Geopackage')
    # End from_gpkg method
# End LinearRingZM class


class Polygon(AbstractGeometry):
    """
    Polygon
    """
    __slots__ = 'rings',

    def __init__(self, coordinates: List[List[DOUBLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the Polygon class
        """
        super().__init__(srs_id=srs_id)
        self.rings: List[LinearRing] = [
            LinearRing(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'Polygon') -> bool:
        """
        Equals
        """
        if not isinstance(other, Polygon):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.rings == other.rings
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.rings)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.rings
        return (WKB_POLYGON_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'Polygon':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=TWO_D, is_ring=True))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'Polygon':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=TWO_D, is_ring=True), srs_id=srs_id)
    # End from_gpkg method
# End Polygon class


class PolygonZ(AbstractGeometry):
    """
    Polygon Z
    """
    __slots__ = 'rings',

    def __init__(self, coordinates: List[List[TRIPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PolygonZ class
        """
        super().__init__(srs_id=srs_id)
        self.rings: List[LinearRingZ] = [
            LinearRingZ(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'PolygonZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, PolygonZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.rings == other.rings
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.rings)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.rings
        return (WKB_POLYGON_Z_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PolygonZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=THREE_D, is_ring=True))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PolygonZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=THREE_D, is_ring=True), srs_id=srs_id)
    # End from_gpkg method
# End PolygonZ class


class PolygonM(AbstractGeometry):
    """
    Polygon M
    """
    __slots__ = 'rings',

    def __init__(self, coordinates: List[List[TRIPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PolygonM class
        """
        super().__init__(srs_id=srs_id)
        self.rings: List[LinearRingM] = [
            LinearRingM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'PolygonM') -> bool:
        """
        Equals
        """
        if not isinstance(other, PolygonM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.rings == other.rings
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.rings)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.rings
        return (WKB_POLYGON_M_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PolygonM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=THREE_D, is_ring=True))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PolygonM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=THREE_D, is_ring=True), srs_id=srs_id)
    # End from_gpkg method
# End PolygonM class


class PolygonZM(AbstractGeometry):
    """
    Polygon ZM
    """
    __slots__ = 'rings',

    def __init__(self, coordinates: List[List[QUADRUPLE]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the PolygonZM class
        """
        super().__init__(srs_id=srs_id)
        self.rings: List[LinearRingZM] = [
            LinearRingZM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'PolygonZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, PolygonZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.rings == other.rings
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.rings)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.rings
        return (WKB_POLYGON_ZM_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'PolygonZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_lines(wkb, dimension=FOUR_D, is_ring=True))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'PolygonZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_lines(
            value[offset:], dimension=FOUR_D, is_ring=True), srs_id=srs_id)
    # End from_gpkg method
# End PolygonZM class


class MultiPolygon(AbstractGeometry):
    """
    Multi Polygon
    """
    __slots__ = 'polygons',

    def __init__(self, coordinates: List[List[List[DOUBLE]]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPolygon class
        """
        super().__init__(srs_id=srs_id)
        self.polygons: List[Polygon] = [
            Polygon(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiPolygon') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPolygon):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.polygons == other.polygons
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.polygons)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.polygons
        return (WKB_MULTI_POLYGON_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPolygon':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(wkb, dimension=TWO_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPolygon':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(
            value[offset:], dimension=TWO_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPolygon class


class MultiPolygonZ(AbstractGeometry):
    """
    Multi Polygon Z
    """
    __slots__ = 'polygons',

    def __init__(self, coordinates: List[List[List[TRIPLE]]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPolygonZ class
        """
        super().__init__(srs_id=srs_id)
        self.polygons: List[PolygonZ] = [
            PolygonZ(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiPolygonZ') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPolygonZ):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.polygons == other.polygons
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.polygons)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.polygons
        return (WKB_MULTI_POLYGON_Z_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPolygonZ':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(wkb, dimension=THREE_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPolygonZ':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(
            value[offset:], dimension=THREE_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPolygonZ class


class MultiPolygonM(AbstractGeometry):
    """
    Multi Polygon M
    """
    __slots__ = 'polygons',

    def __init__(self, coordinates: List[List[List[TRIPLE]]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPolygonM class
        """
        super().__init__(srs_id=srs_id)
        self.polygons: List[PolygonM] = [
            PolygonM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiPolygonM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPolygonM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.polygons == other.polygons
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.polygons)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.polygons
        return (WKB_MULTI_POLYGON_M_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPolygonM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(wkb, dimension=THREE_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPolygonM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(
            value[offset:], dimension=THREE_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPolygonM class


class MultiPolygonZM(AbstractGeometry):
    """
    Multi Polygon M
    """
    __slots__ = 'polygons',

    def __init__(self, coordinates: List[List[List[QUADRUPLE]]],
                 srs_id: int = WGS84) -> None:
        """
        Initialize the MultiPolygonZM class
        """
        super().__init__(srs_id=srs_id)
        self.polygons: List[PolygonZM] = [
            PolygonZM(coords) for coords in coordinates]
    # End init built-in

    def __eq__(self, other: 'MultiPolygonZM') -> bool:
        """
        Equals
        """
        if not isinstance(other, MultiPolygonZM):  # pragma: nocover
            return NotImplemented
        if self.srs_id != other.srs_id:
            return False
        return self.polygons == other.polygons
    # End eq built-in

    @property
    def is_empty(self) -> bool:
        """
        Is Empty
        """
        return not len(self.polygons)
    # End is_empty property

    def to_wkb(self, use_prefix: bool = True) -> bytes:
        """
        To WKB
        """
        geoms = self.polygons
        return (WKB_MULTI_POLYGON_ZM_PRE + pack(COUNT_CODE, len(geoms)) +
                self._join_geometries(geoms))
    # End to_wkb method

    @classmethod
    def from_wkb(cls, wkb: bytes) -> 'MultiPolygonZM':
        """
        From WKB
        """
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(wkb, dimension=FOUR_D))
    # End from_wkb method

    @classmethod
    def from_gpkg(cls, value: bytes) -> 'MultiPolygonZM':
        """
        From Geopackage
        """
        srs_id, offset, is_empty = _unpack_header(value[:HEADER_OFFSET])
        if is_empty:
            return cls([], srs_id=srs_id)
        # noinspection PyTypeChecker
        return cls(_unpack_polygons(
            value[offset:], dimension=FOUR_D), srs_id=srs_id)
    # End from_gpkg method
# End MultiPolygonZM class


if __name__ == '__main__':
    pass
