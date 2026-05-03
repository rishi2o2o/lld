from vehicle_type import VehicleType
from vehicle import Vehicle
from spot_type import SpotType
from spot import Spot
from floor import Floor
from parking_lot import ParkingLot

# create spots
floor1_spots = [
    Spot(1, SpotType.SMALL),
    Spot(2, SpotType.MEDIUM),
    Spot(3, SpotType.LARGE)
]
floor1 = Floor(1, floor1_spots)
lot = ParkingLot([floor1])

# create vehicles
car = Vehicle("KA01AB1234", VehicleType.CAR)

# park car
ticket = lot.park_vehicle(car)

# unpark car
lot.unpark_vehicle(ticket.id)


