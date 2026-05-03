from vehicle_type import VehicleType
from spot_type import SpotType

class Spot:
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
            return self.type in [SpotType.MEDIUM, SpotType.LARGE]
        if vehicle.type == VehicleType.TRUCK:
            return self.type == SpotType.LARGE
        return False

    def park(self, vehicle):
        self.vehicle = vehicle

    def remove(self):
        self.vehicle = None


