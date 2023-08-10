class Truck:
    def __init__(self, truck_id, speed, current_time, depart_time):
        self.id = truck_id  # Truck's ID
        self.speed = speed  # Average speed in miles per hour
        self.current_location = '4001 South 700 East'  # The hub address
        self.packages = []  # List of packages currently on the truck
        self.all_packages = []
        self.total_distance = 0  # Total distance traveled in miles
        self.current_time = current_time  # Current time for this truck
        self.depart_time = depart_time  # Departure time for this truck

    def add_package(self, package):
        # Add a package to the truck
        self.packages.append(package)
        self.all_packages.append(package)

    def deliver_package(self, package):
        # Remove a package from the truck
        self.packages.remove(package)

    def update_location(self, new_location):
        self.current_location = new_location

    def add_distance(self, distance):
        self.total_distance += distance

    def __str__(self):
        return (f'Truck {self.id}\n'
                f'Current location: {self.current_location}\n'
                f'Total distance traveled: {self.total_distance} miles\n'
                f'Packages: {[str(package) for package in self.packages]}')
