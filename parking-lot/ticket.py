import time

class Ticket:
    def __init__(self, ticket_id, vehicle, spot):
        self.id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()
        self.exit_time = None

    def close(self):
        self.exit_time = time.time()

