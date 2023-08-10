# Teksong Eap, WGU ID:009489418
import csv
from datetime import datetime, timedelta

from HashTable import HashTable
from Package import Package
from Truck import Truck


# PACKAGE HANDLING
def load_package_data(hash_table):
    with open('packageData.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(package.package_id, package)


package_hash_table = HashTable()
load_package_data(package_hash_table)


# ADDRESS HANDLING
def load_address_data():
    with open('addressData.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file, delimiter=',')
        addresses = [row[1] for row in csv_reader]  # Get the address from each row
    return addresses


# DISTANCE HANDLING
def load_distance_data():
    # Determine the size of the matrix
    with open('distanceData.csv', 'r', encoding='utf-8-sig') as file:
        num_addresses = sum(1 for row in file)

    # Create a zero-filled matrix of the right size
    distance_matrix = [[0] * num_addresses for _ in range(num_addresses)]

    # Fill the matrix with actual distances
    with open('distanceData.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(csv_reader):
            for j, value in enumerate(row):
                if value:  # Only convert non-empty strings
                    distance_matrix[i][j] = float(value)
                    distance_matrix[j][i] = float(value)
    return distance_matrix


def distance_between(from_address, to_address, addresses, distances):
    # Get the indices of the two addresses
    index1 = addresses.index(from_address)
    index2 = addresses.index(to_address)
    # Return the distance between them
    return distances[index1][index2]


# Load the distance data
distance_matrix = load_distance_data()

# Load the address data
address_list = load_address_data()


# PACKAGE LOADING
def load_truck1(truck1, hash_table):
    loaded_package_ids = set()
    together_packages = [[13, 15, 19]]

    for i in range(1, 41):
        package = hash_table.lookup(i)
        if "Can only be on truck 2" not in package.special_notes and \
                "Delayed on flight" not in package.special_notes and \
                "Wrong address listed" not in package.special_notes:
            # Check for packages that must be delivered together
            for group in together_packages:
                if package.package_id in group:
                    all_present = all([hash_table.lookup(pkg_id) for pkg_id in group])
                    if all_present:
                        for pkg_id in group:
                            if len(truck1.packages) < 16:
                                truck1.add_package(hash_table.lookup(pkg_id))
                                loaded_package_ids.add(pkg_id)
            else:
                if package.package_id not in loaded_package_ids and len(truck1.packages) < 16:
                    truck1.add_package(package)
                    loaded_package_ids.add(package.package_id)

    loaded_package_ids.add(39)
    loaded_package_ids.add(20)

    return loaded_package_ids


def load_truck2(truck2, hash_table, loaded_package_ids):
    together_packages = [[13, 15, 19]]

    for i in range(1, 41):
        package = hash_table.lookup(i)
        if package.package_id not in loaded_package_ids:
            if "Can only be on truck 2" in package.special_notes or "Delayed on flight" in package.special_notes:
                truck2.add_package(package)
                loaded_package_ids.add(package.package_id)

            # Check for packages that must be delivered together
            for group in together_packages:
                if package.package_id in group and all([pkg_id not in loaded_package_ids for pkg_id in group]):
                    for pkg_id in group:
                        if len(truck2.packages) < 16:
                            truck2.add_package(hash_table.lookup(pkg_id))
                            loaded_package_ids.add(pkg_id)

    loaded_package_ids.add(40)
    return loaded_package_ids


def load_truck3(truck3, hash_table, loaded_package_ids):
    for i in range(1, 41):
        package = hash_table.lookup(i)
        if package.package_id not in loaded_package_ids and package.package_id != 9 and len(truck3.packages) < 16:
            truck3.add_package(package)
            loaded_package_ids.add(package.package_id)

    return loaded_package_ids


start_time = datetime.strptime('08:00:00', '%H:%M:%S')  # Example start time
delayed_time = datetime.strptime('09:05:00', '%H:%M:%S')

# TRUCK HANDLING
truck1 = Truck(1, 18, start_time, start_time)
truck2 = Truck(2, 18, delayed_time, delayed_time)
truck3 = Truck(3, 18, None, None)

loaded_ids = load_truck1(truck1, package_hash_table)
# print(loaded_ids)
# print(truck1.packages)
loaded_ids = load_truck2(truck2, package_hash_table, loaded_ids)
# print(loaded_ids)
# print(truck2.packages)
loaded_ids = load_truck3(truck3, package_hash_table, loaded_ids)
# print(loaded_ids)
# print(truck3.packages)

# deliver the packages using greedy algorithm with complexity O(n^2)
def deliver_packages(truck, addresses, distances):
    current_location = truck.current_location
    # Mark all packages on the truck as 'En route'
    for package in truck.packages:
        package.update_status("En route")

    while truck.packages:
        # Find the nearest unvisited package
        nearest_distance = float('inf')
        nearest_package = None
        for package in truck.packages:
            distance = distance_between(current_location, package.address, addresses, distances)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        # Update the truck's and package's details
        truck.add_distance(nearest_distance)
        hours_traveled = nearest_distance / truck.speed
        truck.current_time += timedelta(hours=hours_traveled)
        nearest_package.delivery_time = truck.current_time.strftime('%H:%M:%S')
        truck.deliver_package(nearest_package)
        current_location = nearest_package.address

    # Return to the hub and update the distance and time
    distance_to_hub = distance_between(current_location, '4001 South 700 East', addresses, distances)
    truck.add_distance(distance_to_hub)
    hours_traveled = distance_to_hub / truck.speed
    truck.current_time += timedelta(hours=hours_traveled)


# ACTUAL DELIVERY
deliver_packages(truck1, address_list, distance_matrix)
# print(truck1.total_distance)
deliver_packages(truck2, address_list, distance_matrix)
# print(truck2.total_distance)

# The correct address for package 9 has magically appeared!
if truck1.current_time >= datetime.strptime('10:20:00', '%H:%M:%S'):
    truck3.current_time = truck1.current_time
    print(truck3.current_time)
    truck3.depart_time = truck1.current_time
    package = package_hash_table.lookup(9)
    package.address = '410 S State St'
    loaded_ids.add(package.package_id)
    truck3.add_package(package)
    deliver_packages(truck3, address_list, distance_matrix)
else:
    truck3.current_time = truck1.current_time
    print(truck3.current_time)
    truck3.depart_time = truck1.current_time
    deliver_packages(truck3, address_list, distance_matrix)


# Command line interface options and such
def show_menu():
    print("***************************************")
    print("1. Show status of all packages for a specific time.")
    print("2. Get a single package's status with a time.")
    print("3. Show total mileage traveled by all trucks and status of packages at EOD.")
    print("4. Exit the program.")
    print("***************************************")


def show_all_packages_status_for_time(time, trucks):
    time_obj = datetime.strptime(time, '%H:%M:%S')
    for truck in trucks:
        print(f"\nTruck {truck.id} Status at {time}:")
        for package in truck.all_packages:
            package_status = package.status
            if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= time_obj:
                package_status = "Delivered"
            elif package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') > time_obj:
                if "Delayed" in package.special_notes:
                    package_status = "Delayed"
                else:
                    package_status = "En route"
            print(f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status}")


def get_single_package_status(package_id, time, package_hash_table):
    package = package_hash_table.lookup(package_id)
    if not package:
        print("Package not found.")
        return
    package_status = package.status
    if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= datetime.strptime(time,
                                                                                                           '%H:%M:%S'):
        package_status = "Delivered"
    if package_status == "Delivered":
        print(
            f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status} at {package.delivery_time}")
    else:
        print(
            f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status} at {time}")


def show_total_mileage(trucks):
    total_mileage = sum([truck.total_distance for truck in trucks])
    print(f"Total mileage traveled by all trucks: {total_mileage} miles")
    time_obj = datetime.strptime('17:00:00', '%H:%M:%S')
    for truck in trucks:
        print(f"\nTruck {truck.id} Status at EOD:")
        for package in truck.all_packages:
            package_status = package.status
            if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= time_obj:
                package_status = "Delivered"
            elif package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') > time_obj:
                if "Delayed" in package.special_notes:
                    package_status = "Delayed"
                else:
                    package_status = "En route"
            print(
                f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status} at {package.delivery_time}")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            time = input("Enter the time in HH:MM:SS format: ")
            show_all_packages_status_for_time(time, [truck1, truck2, truck3])

        elif choice == "2":
            package_id = int(input("Enter the package ID: "))
            time = input("Enter the time in HH:MM:SS format: ")
            get_single_package_status(package_id, time, package_hash_table)

        elif choice == "3":
            show_total_mileage([truck1, truck2, truck3])

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


main()
