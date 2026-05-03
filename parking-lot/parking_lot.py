from ticket import Ticket

class ParkingLot:
    def __init__(self, floors):
        self.floors = floors
        self.tickets = {}
        self.ticket_counter = 0

    def park_vehicle(self, vehicle):
        for floor in self.floors:
            spot = floor.find_spot(vehicle)
            if spot:
                spot.park(vehicle)
                
                self.ticket_counter += 1
                ticket = Ticket(self.ticket_counter, vehicle, spot)
                self.tickets[ticket.id] = ticket

                print(f"Vehicle parked. Ticket ID: {ticket.id}")
                return ticket
        
        print("Parking Full")
        return None

    def unpark_vehicle(self, ticket_id):
        if ticket_id not in self.tickets:
            print("Invalid ticket")
            return
        
        ticket = self.tickets[ticket_id]
        ticket.close()

        duration = ticket.exit_time - ticket.entry_time
        cost = self.calculate_cost(duration)

        ticket.spot.remove()
        del self.tickets[ticket_id]

        print(f"Vehicle exited. Cost: {cost:.2f}")

    def calculate_cost(self, duration):
        hours = duration / 3600
        return max(10, int(hours * 10))  # simple pricing

