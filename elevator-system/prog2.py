"""
-> Has only 1 elevator
-> Has floor buttons inside elevator, pressing
   whom calls the evelator.add_request(floor)
-> Has only call elevator button on each floor
   (not up and down), pressing whom calls the
   elevator.add_request(floor)
-> Uses SCAN algo (also called LOOK algo)
"""

import time
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    def __init__(self, total_floors):
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.total_floors = total_floors
        # Using sets to avoid duplicate requests for the same floor
        self.up_queue = set()
        self.down_queue = set()

    def add_request(self, floor):
        if floor < 0 or floor >= self.total_floors:
            print(f"Error: Floor {floor} is out of bounds.")
            return

        if floor > self.current_floor:
            self.up_queue.add(floor)
            print(f"Request added to up queue: Floor {floor}")

        elif floor < self.current_floor:
            self.down_queue.add(floor)
            print(f"Request added to down queue: Floor {floor}")

        else:
            print(f"Already at floor {floor}.")

        # If IDLE, decide which way to start moving
        if self.direction == Direction.IDLE:
            if floor > self.current_floor:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN

    def process_requests(self):
        while self.up_queue or self.down_queue:
            if self.direction == Direction.UP:
                self._move_up()
            elif self.direction == Direction.DOWN:
                self._move_down()
            
            # Change direction if the current direction's queue is empty
            if self.direction == Direction.UP and not self.up_queue:
                self.direction = Direction.DOWN if self.down_queue else Direction.IDLE

            elif self.direction == Direction.DOWN and not self.down_queue:
                self.direction = Direction.UP if self.up_queue else Direction.IDLE

        print("All requests serviced. Elevator is now IDLE.")

    def _move_up(self):
        print(f"--- Moving UP from {self.current_floor} ---")
        # Find all stops in the UP direction
        stops = sorted([f for f in self.up_queue if f >= self.current_floor])
        
        for floor in range(self.current_floor, (max(stops) + 1 if stops else self.current_floor)):
            self.current_floor = floor
            if self.current_floor in self.up_queue:
                self._stop_at_floor(self.current_floor, self.up_queue)
            time.sleep(0.5) # Simulating travel time

    def _move_down(self):
        print(f"--- Moving DOWN from {self.current_floor} ---")
        # Find all stops in the DOWN direction
        stops = sorted([f for f in self.down_queue if f <= self.current_floor], reverse=True)
        
        for floor in range(self.current_floor, (min(stops) - 1 if stops else self.current_floor), -1):
            self.current_floor = floor
            if self.current_floor in self.down_queue:
                self._stop_at_floor(self.current_floor, self.down_queue)
            time.sleep(0.5)

    def _stop_at_floor(self, floor, queue):
        print(f"[STOP] Reached Floor {floor}. Opening Doors...")
        queue.remove(floor)
        time.sleep(1) # Simulating passengers getting in/out
        print(f"[STOP] Closing Doors.")

# --- Demo Execution ---
if __name__ == "__main__":
    my_elevator = Elevator(total_floors=10)

    # Simulating users pressing buttons
    print("Requests received: Floor 3, Floor 8, Floor 1")
    my_elevator.add_request(3)
    my_elevator.add_request(8)
    my_elevator.add_request(1)

    print("\n=== Processing with SCAN Algorithm ===\n")
    my_elevator.process_requests()


