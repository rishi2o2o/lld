from vehicle_type import VehicleType
from vehicle import Vehicle
from spot_type import SpotType
from spot import Spot
from floor import Floor
from parking_lot import ParkingLot

# create some parking spots
floor1_spots = [
    Spot(1, SpotType.SMALL),
    Spot(2, SpotType.MEDIUM),
    Spot(3, SpotType.LARGE)
]

# create a floor with those parking spots
floor1 = Floor(1, floor1_spots)

# create a parking lot with one floor
lot = ParkingLot([floor1])

# create a vehicle to park
car = Vehicle("KA01AB1234", VehicleType.CAR)

# park vehicle
ticket = lot.park_vehicle(car)

# unpark vehicle
lot.unpark_vehicle(ticket.id)



