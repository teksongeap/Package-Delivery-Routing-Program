class Truck:
    def __init__(self, truck_id, current_location="AtHub"):
        self.truck_id = truck_id
        self.packages = []
        self.current_location = current_location
        self.total_distance = 0

    def load_package(self, package):
        self.packages.append(package)
        package.status = f"InRoute by Truck-{self.truck_id}"

    def unload_package(self, package_id):
        for package in self.packages:
            if package.package_id == package_id:
                self.packages.remove(package)
                package.status = "Delivered by Truck-" + self.truck_id
                return True
        return False

    def deliver_packages(self):
        for package in self.packages[:]:
            self.unload_package(package.package_id)

    def __str__(self):
        return f"Truck-{self.truck_id}, Packages: {[pkg.package_id for pkg in self.packages]}, Distance: {self.total_distance} miles"