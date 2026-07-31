from dataclasses import dataclass
from abc import ABC, abstractmethod

# Dataclass
@dataclass
class Trip:
    pickup: str
    dropoff: str
    distance_km: float
    duration_min: int

    def __repr__(self):
        return (f"Trip(Pickup={self.pickup}, Dropoff={self.dropoff}, "
                f"Distance={self.distance_km} km, Duration={self.duration_min} min)")


# Property
class Vehicle:
    def __init__(self, vehicle_no, fuel_level):
        self.vehicle_no = vehicle_no
        self.fuel_level = fuel_level

    @property
    def fuel_level(self):
        return self._fuel_level

    @fuel_level.setter
    def fuel_level(self, value):
        if value < 0 or value > 100:
            raise ValueError("Fuel level must be between 0 and 100.")
        self._fuel_level = value


# Abstract Base Class
class FareStrategy(ABC):

    @abstractmethod
    def calculate_fare(self, trip):
        pass


class StandardFare(FareStrategy):
    def calculate_fare(self, trip):
        return trip.distance_km * 15


class PremiumFare(FareStrategy):
    def calculate_fare(self, trip):
        return trip.distance_km * 25


class PoolFare(FareStrategy):
    def calculate_fare(self, trip):
        return trip.distance_km * 10


# Composition
class RideBooking:
    def __init__(self, trip, vehicle, strategy):
        self.trip = trip
        self.vehicle = vehicle
        self.strategy = strategy

    def calculate_total_fare(self):
        return self.strategy.calculate_fare(self.trip)


# Magic Methods
class RideHistory:
    def __init__(self):
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)

    def __len__(self):
        return len(self.trips)

    def __getitem__(self, index):
        return self.trips[index]


# Main Program
trip = Trip("Home", "Office", 12, 25)

vehicle = Vehicle("KA01AB1234", 80)

strategy = PremiumFare()

booking = RideBooking(trip, vehicle, strategy)

print(trip)
print("Fuel Level:", vehicle.fuel_level)
print("Fare:", booking.calculate_total_fare())

history = RideHistory()
history.add_trip(trip)

print("Total Trips:", len(history))
print("First Trip:", history[0])
