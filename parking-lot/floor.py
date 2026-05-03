class Floor:
    def __init__(self, floor_id, spots):
        self.id = floor_id
        self.spots = spots  # list of parking spots

    def find_spot(self, vehicle):
        for spot in self.spots:
            if spot.is_free() and spot.can_fit(vehicle):
                return spot
        return None

