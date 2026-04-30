"""Geometry primitives and transformation utilities for CadQuery.

This module provides Vector, Matrix, and Plane classes that form the
geometric foundation for all CadQuery operations.
"""

from typing import Optional, Tuple, Union, overload
import math

from OCP.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
)

Real = Union[int, float]


class Vector:
    """A 3D vector with OCC backend.

    Wraps gp_Vec and gp_Pnt for convenient arithmetic and geometric operations.

    Examples::

        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        v3 = v1 + v2          # Vector(1, 1, 0)
        v4 = v1.cross(v2)     # Vector(0, 0, 1)
    """

    def __init__(
        self,
        x: Union[Real, gp_Vec, gp_Pnt, gp_Dir, Tuple] = 0,
        y: Real = 0,
        z: Real = 0,
    ):
        if isinstance(x, gp_Vec):
            self._wrapped = x
        elif isinstance(x, gp_Pnt):
            self._wrapped = gp_Vec(x.X(), x.Y(), x.Z())
        elif isinstance(x, gp_Dir):
            self._wrapped = gp_Vec(x.X(), x.Y(), x.Z())
        elif isinstance(x, (list, tuple)):
            self._wrapped = gp_Vec(*x)
        else:
            self._wrapped = gp_Vec(x, y, z)

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def Length(self) -> float:
        """Return the magnitude of this vector."""
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def dot(self, other: "Vector") -> float:
        """Dot product with another vector."""
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        """Cross product with another vector."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def add(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def sub(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def multiply(self, scale: Real) -> "Vector":
        return Vector(self._wrapped.Multiplied(scale))

    def toTuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def toPnt(self) -> gp_Pnt:
        return gp_Pnt(self.x, self.y, self.z)

    def toDir(self) -> gp_Dir:
        return gp_Dir(self._wrapped)

    def distanceTo(self, other: "Vector") -> float:
        """Return the Euclidean distance from this vector to another."""
        return (self - other).Length()

    def __add__(self, other: "Vector") -> "Vector":
        return self.add(other)

    def __sub__(self, other: "Vector") -> "Vector":
        return self.sub(other)

    def __mul__(self, scale: Real) -> "Vector":
        return self.multiply(scale)

    def __rmul__(self, scale: Real) -> "Vector":
        return self.multiply(scale)

    def __neg__(self) -> "Vector":
        return Vector(self._wrapped.Reversed())

    def __abs__(self) -> float:
        return self.Length()

    def __repr__(self) -> str:
        return f"Vector({self.x},
