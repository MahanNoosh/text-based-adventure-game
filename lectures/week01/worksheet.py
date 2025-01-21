from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Vendor:
    """A vendor that sells groceries or meals.

    This could be a grocery store or restaurant.

    Instance Attributes:
      - name: the name of the vendor
      - address: the address of the vendor
      - menu: the menu of the vendor with the name of the food item mapping to
              its price
      - location: the location of the vendor as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - self.address != ''
      - all(self.menu[item] >= 0 for item in self.menu)
      - -90.0 <= self.location[0] <= 90.0
      - -180.0 <= self.location[1] <= 180.0
    """
    name: str
    address: str
    menu: dict[str, float]
    location: tuple[float, float]  # (lat, lon) coordinates


@dataclass
class Customer:
    """A person who orders food.

    Instance Attributes:
      - name: the name of the customer
      - location: the location of the customer as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - -90 <= self.location[0] <= 90
      - -180 <= self.location[1] <= 180
    """
    name: str
    location: tuple[float, float]


@dataclass
class Order:
    """A food order from a customer.

    Instance Attributes:
      - customer: the customer who placed this order
      - vendor: the vendor that the order is placed for
      - food_items: a mapping from names of food to the quantity being ordered
      - start_time: the time the order was placed
      - courier: the courier assigned to this order (initially None)
      - end_time: the time the order was completed by the courier (initially None)

    Representation Invariants:
      - all(self.food_items[item] >= 1 for item in self.food_items)
    """
    customer: Customer
    vendor: Vendor
    food_items: dict[str, int]
    start_time: datetime.datetime
    courier: Optional[Courier] = None
    end_time: Optional[datetime.datetime] = None


@dataclass
class Courier:
    """A person who delivers food orders from vendors to customers.

    Instance Attributes:
        - name: name of courier
        - location: the location of the courier as (latitude, longitude)
        - current_order: orders assigned to the courier
        - vehicle: the vehicle used for delivery

    Representation Invariants:
        - self.name != ''
        - self.current_order is None or self.current_order is self
        - -90.0 <= self.location[0] <= 90.0
        - -180.0 <= self.location[1] <= 180.0

    >>> c = Courier("Mahan", (22.2, 33.3))
    >>> c.name
    'Mahan'
    >>> c.location
    (22.2, 33.3)
    >>> print(c.current_order)
    None
    >>> print(c.vehicle)
    None
    """
    name: str
    location: (float, float)
    current_order: Optional[Order] = None
    vehicle: Optional[str] = None
