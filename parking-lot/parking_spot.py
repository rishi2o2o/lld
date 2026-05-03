from vehicle_type import VehicleType
from parking_spot_type import ParkingSpotType

class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.id = spot_id
        self.type = spot_type
        self.vehicle = None

    def is_free(self):
        return self.vehicle is None

    def can_fit(self, vehicle):
        if vehicle.type == VehicleType.BIKE:
            return True
        if vehicle.type == VehicleType.CAR:
            return self.type in [ParkingSpotType.MEDIUM, ParkingSpotType.LARGE]
        if vehicle.type == VehicleType.TRUCK:
            return self.type == ParkingSpotType.LARGE
        return False

    def park(self, vehicle):
        self.vehicle = vehicle

    def remove(self):
        self.vehicle = None


