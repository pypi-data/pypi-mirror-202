from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar
import math

Number = TypeVar('Number', float, int)


@dataclass()
class vec2d:
    x: Number = 0
    y: Number = 0

    def __add__(self, other: vec2d) -> vec2d:
        return vec2d(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: vec2d) -> vec2d:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: vec2d) -> vec2d:
        return vec2d(self.x - other.x, self.y - other.y)

    def __isub__(self, other: vec2d):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Number) -> vec2d:
        return vec2d(self.x * other, self.y * other)

    def __imul__(self, other: Number) -> vec2d:
        self.x *= other
        self.y *= other
        return self

    def __rmul__(self, other: Number) -> vec2d:
        return vec2d(self.x * other, self.y * other)

    def __truediv__(self, other: Number) -> vec2d:
        return vec2d(self.x / other, self.y / other)

    def __itruediv__(self, other: vec2d) -> vec2d:
        self.x /= other
        self.y /= other
        return self

    def __eq__(self, other: vec2d) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: vec2d) -> bool:
        return not self == other

    def __neg__(self) -> vec2d:
        self.x = -self.x
        self.y = -self.y
        return self

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __iter__(self):
        yield self.x
        yield self.y

    def to_unit(self: vec2d) -> vec2d:
        """
        Returns the unit vector corresponding to the vector
        :return: The unit vector
        """
        factor = abs(self)
        return vec2d(self.x / factor, self.y / factor)

    def to_unit_ip(self) -> None:
        """
        Converts this vector into its respective unit vector in place
        :return: None
        """

    def proj(self, other: vec2d):
        """
        Projects this vector onto another vector and returns the result
        :param other: Vector to project onto
        :return: Result of the projection
        """
        return (self + other) / abs(other)

    def iproj(self, other: vec2d) -> None:
        """
        Projects this vector onto another vector in place
        :param other: Vector to project onto
        :return: None
        """
        self.x = (self.x + other.x) / abs(other)
        self.y = (self.y + other.y) / abs(other)
