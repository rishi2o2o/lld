"""
-> Has only 1 elevator
-> Has floor buttons inside elevator, pressing
   whom calls the evelator.add_car_call(floor)
-> Has up and down buttons on each floor, pressing
   whom calls the elevator.add_hall_call(floor, direction)
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
        # Separate queues for hall calls (with direction) and car calls
        self.up_requests = set()  # Floors where people pressed UP button
        self.down_requests = set()  # Floors where people pressed DOWN button
        self.car_calls = set()  # Destination floors from inside elevator

    def add_hall_call(self, floor, direction):
        # Someone on 'floor' wants to go 'direction' (UP or DOWN)

        if floor < 0 or floor >= self.total_floors:
            print(f"Error: Floor {floor} is out of bounds.")
            return

        if floor == self.current_floor:
            print(f"Already at floor {floor}.")
            return

        if direction == Direction.UP:
            self.up_requests.add(floor)
            print(f"Hall call added: Floor {floor} [UP button]")

        elif direction == Direction.DOWN:
            self.down_requests.add(floor)
            print(f"Hall call added: Floor {floor} [DOWN button]")

        # If IDLE, decide which way to start moving
        if self.direction == Direction.IDLE:
            if floor > self.current_floor:
                self.direction = Direction.UP

            elif floor < self.current_floor:
                self.direction = Direction.DOWN

    def add_car_call(self, floor):
        # Someone inside elevator wants to go to 'floor'

        if floor < 0 or floor >= self.total_floors:
            print(f"Error: Floor {floor} is out of bounds.")
            return

        if floor == self.current_floor:
            print(f"Already at floor {floor}.")
            return

        self.car_calls.add(floor)
        print(f"Car call added: Floor {floor} [inside elevator button]")

        # If IDLE, decide which way to start moving
        if self.direction == Direction.IDLE:
            if floor > self.current_floor:
                self.direction = Direction.UP

            elif floor < self.current_floor:
                self.direction = Direction.DOWN

    def process_requests(self):
        while self.up_requests or self.down_requests or self.car_calls:
            if self.direction == Direction.UP:
                self._move_up()

            elif self.direction == Direction.DOWN:
                self._move_down()
            
            # Change direction if current direction has no more requests
            if self.direction == Direction.UP:
                if not self._has_up_requests():
                    self.direction = Direction.DOWN if self._has_down_requests() else Direction.IDLE

            elif self.direction == Direction.DOWN:
                if not self._has_down_requests():
                    self.direction = Direction.UP if self._has_up_requests() else Direction.IDLE

        print("All requests serviced. Elevator is now IDLE.")

    def _has_up_requests(self):
        """Check if there are any requests above current floor"""
        return (any(f > self.current_floor for f in self.up_requests) or
                any(f > self.current_floor for f in self.car_calls))

    def _has_down_requests(self):
        """Check if there are any requests below current floor"""
        return (any(f < self.current_floor for f in self.down_requests) or
                any(f < self.current_floor for f in self.car_calls))

    def _move_up(self):
        print(f"--- Moving UP from {self.current_floor} ---")
        
        # Find all stops in the UP direction
        up_stops = {f for f in self.up_requests if f > self.current_floor}
        car_stops_up = {f for f in self.car_calls if f > self.current_floor}
        all_stops = sorted(up_stops | car_stops_up)
        
        if not all_stops:
            return
        
        for floor in range(self.current_floor, max(all_stops) + 1):
            self.current_floor = floor
            
            # Stop if there's an UP hall call or car call at this floor
            should_stop = False
            stop_reason = []
            
            if self.current_floor in self.up_requests:
                should_stop = True
                stop_reason.append("UP hall call")
                self.up_requests.remove(self.current_floor)
            
            if self.current_floor in self.car_calls:
                should_stop = True
                stop_reason.append("car call")
                self.car_calls.remove(self.current_floor)
            
            if should_stop:
                self._stop_at_floor(self.current_floor, stop_reason)
            
            time.sleep(0.5)  # Simulating travel time

    def _move_down(self):
        print(f"--- Moving DOWN from {self.current_floor} ---")
        
        # Find all stops in the DOWN direction
        down_stops = {f for f in self.down_requests if f < self.current_floor}
        car_stops_down = {f for f in self.car_calls if f < self.current_floor}
        all_stops = sorted(down_stops | car_stops_down, reverse=True)
        
        if not all_stops:
            return
        
        for floor in range(self.current_floor, min(all_stops) - 1, -1):
            self.current_floor = floor
            
            # Stop if there's a DOWN hall call or car call at this floor
            should_stop = False
            stop_reason = []
            
            if self.current_floor in self.down_requests:
                should_stop = True
                stop_reason.append("DOWN hall call")
                self.down_requests.remove(self.current_floor)
            
            if self.current_floor in self.car_calls:
                should_stop = True
                stop_reason.append("car call")
                self.car_calls.remove(self.current_floor)
            
            if should_stop:
                self._stop_at_floor(self.current_floor, stop_reason)
            
            time.sleep(0.5)

    def _stop_at_floor(self, floor, reasons):
        reason_str = " & ".join(reasons)
        print(f"[STOP] Reached Floor {floor}. Opening Doors... ({reason_str})")
        time.sleep(1)  # Simulating passengers getting in/out
        print(f"[STOP] Closing Doors.")


# --- Demo Execution ---
if __name__ == "__main__":
    my_elevator = Elevator(total_floors=10)

    print("=== Scenario: Realistic elevator usage ===\n")
    
    # Person on floor 5 wants to go UP
    my_elevator.add_hall_call(5, Direction.UP)
    
    # Person on floor 3 wants to go DOWN
    my_elevator.add_hall_call(3, Direction.DOWN)
    
    # Person on floor 7 wants to go UP
    my_elevator.add_hall_call(7, Direction.UP)
    
    # Someone inside elevator presses floor 8
    my_elevator.add_car_call(8)
    
    # Person on floor 2 wants to go UP
    my_elevator.add_hall_call(2, Direction.UP)

    print("\n=== Processing with SCAN Algorithm (with directional awareness) ===\n")
    my_elevator.process_requests()
    

    print("\n" + "="*60)
    print("=== Scenario 2: Demonstrating direction-aware stops ===\n")
    
    my_elevator2 = Elevator(total_floors=10)
    
    # Elevator starts at floor 0
    # Person on floor 5 wants to go DOWN (elevator should skip this while going UP)
    my_elevator2.add_hall_call(5, Direction.DOWN)
    
    # Person inside presses floor 8
    my_elevator2.add_car_call(8)
    
    # Person on floor 6 wants to go UP (elevator should stop here while going UP)
    my_elevator2.add_hall_call(6, Direction.UP)
    
    print("\n=== Processing ===\n")
    my_elevator2.process_requests()
    
    print("\nNotice: Elevator went UP (0→6→8), then came DOWN (8→5)")
    print("It skipped floor 5 while going UP because the DOWN button was pressed there.")


