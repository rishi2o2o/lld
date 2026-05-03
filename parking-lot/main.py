from vehicle_type import VehicleType
from vehicle import Vehicle
from parking_spot_type import ParkingSpotType
from parking_spot import ParkingSpot
from floor import Floor
from parking_lot import ParkingLot

# create spots
floor1_spots = [
    ParkingSpot(1, ParkingSpotType.SMALL),
    ParkingSpot(2, ParkingSpotType.MEDIUM),
    ParkingSpot(3, ParkingSpotType.LARGE)
]
floor1 = Floor(1, floor1_spots)
lot = ParkingLot([floor1])

# create vehicles
car = Vehicle("KA01AB1234", VehicleType.CAR)

# park car
ticket = lot.park_vehicle(car)

# unpark car
lot.unpark_vehicle(ticket.id)


