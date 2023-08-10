# Teksong Eap, WGU ID:009489418
import csv
from datetime import datetime, timedelta

from HashTable import HashTable
from Package import Package
from Truck import Truck


# PACKAGE HANDLING
# loud package data
def load_package_data(hash_table):
    with open('packageData.csv', 'r') as file:  # get from package data
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            # create new package object
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(package.package_id, package)


package_hash_table = HashTable()
load_package_data(package_hash_table)


# ADDRESS HANDLING
# load address data
def load_address_data():
    with open('addressData.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file, delimiter=',')
        addresses = [row[1] for row in csv_reader]  # Get the address from each row
    return addresses


# DISTANCE HANDLING
# load distance data that is a triangular matrix
def load_distance_data():
    # Determine the size of the matrix
    with open('distanceData.csv', 'r', encoding='utf-8-sig') as file:
        num_addresses = sum(1 for row in file)

    # Create a zero-filled matrix of the right size
    distance_matrix = [[0] * num_addresses for _ in range(num_addresses)]

    # Fill the matrix with actual distances (making the triangle a square)
    with open('distanceData.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(csv_reader):
            for j, value in enumerate(row):
                if value:  # Only convert non-empty strings
                    distance_matrix[i][j] = float(value)
                    distance_matrix[j][i] = float(value)
    return distance_matrix


# get distance between two addresses within matrix
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
# load truck 1 manually
def load_truck1(truck1, hash_table):
    packages_to_load = [1, 4, 5, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 39, 40]
    for i in packages_to_load:
        package = hash_table.lookup(i)
        truck1.add_package(package)

    # together_packages = [[13, 15, 19]]
    #
    # for i in range(1, 41):
    #     package = hash_table.lookup(i)
    #     if "Can only be on truck 2" not in package.special_notes and \
    #             "Delayed on flight" not in package.special_notes and \
    #             "Wrong address listed" not in package.special_notes:
    #         # Check for packages that must be delivered together
    #         for group in together_packages:
    #             if package.package_id in group:
    #                 all_present = all([hash_table.lookup(pkg_id) for pkg_id in group])
    #                 if all_present:
    #                     for pkg_id in group:
    #                         if len(truck1.packages) < 16:
    #                             truck1.add_package(hash_table.lookup(pkg_id))
    #                             loaded_package_ids.add(pkg_id)
    #         else:
    #             if package.package_id not in loaded_package_ids and len(truck1.packages) < 16:
    #                 truck1.add_package(package)
    #                 loaded_package_ids.add(package.package_id)
    #
    # loaded_package_ids.add(39)
    # loaded_package_ids.add(20)

    # return loaded_package_ids


# load truck 2 manually
def load_truck2(truck2, hash_table):
    packages_to_load = [2, 3, 6, 7, 10, 11, 12, 17, 18, 25, 28, 32, 35, 36, 37, 38]
    for i in packages_to_load:
        package = hash_table.lookup(i)
        truck2.add_package(package)

    # together_packages = [[13, 15, 19]]
    #
    # for i in range(1, 41):
    #     package = hash_table.lookup(i)
    #     if package.package_id not in loaded_package_ids:
    #         if "Can only be on truck 2" in package.special_notes or "Delayed on flight" in package.special_notes:
    #             truck2.add_package(package)
    #             loaded_package_ids.add(package.package_id)
    #
    #         # Check for packages that must be delivered together
    #         for group in together_packages:
    #             if package.package_id in group and all([pkg_id not in loaded_package_ids for pkg_id in group]):
    #                 for pkg_id in group:
    #                     if len(truck2.packages) < 16:
    #                         truck2.add_package(hash_table.lookup(pkg_id))
    #                         loaded_package_ids.add(pkg_id)
    #
    # loaded_package_ids.add(40)
    # return loaded_package_ids


# load truck 3 manually
def load_truck3(truck3, hash_table):
    packages_to_load = [8, 9, 22, 23, 24, 26, 27, 33]
    for i in packages_to_load:
        package = hash_table.lookup(i)
        truck3.add_package(package)

    # for i in range(1, 41):  # load the rest of the packages leftover
    #     package = hash_table.lookup(i)
    #     if package.package_id not in loaded_package_ids and package.package_id != 9 and len(truck3.packages) < 16:
    #         truck3.add_package(package)
    #         loaded_package_ids.add(package.package_id)
    #
    # return loaded_package_ids


start_time = datetime.strptime('08:00:00', '%H:%M:%S')  # Example start time
delayed_time = datetime.strptime('09:05:00', '%H:%M:%S')

# TRUCK HANDLING
truck1 = Truck(1, 18, start_time, start_time)
truck2 = Truck(2, 18, delayed_time, delayed_time)
truck3 = Truck(3, 18, None, None)

# load the previous ids to keep track of loaded packages
load_truck1(truck1, package_hash_table)
load_truck2(truck2, package_hash_table)
load_truck3(truck3, package_hash_table)


# simulate delivery of the packages using greedy algorithm with time complexity n^2
def deliver_packages(truck, addresses, distances):
    current_location = truck.current_location
    # Mark all packages on the truck as 'En route'
    # for package in truck.packages:
    #     package.update_status("En route")

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


# SIMULATE DELIVERY
deliver_packages(truck1, address_list, distance_matrix)
# print(truck1.total_distance)
deliver_packages(truck2, address_list, distance_matrix)
# print(truck2.total_distance)

# The correct address for package 9 has magically appeared!
if truck1.current_time >= datetime.strptime('10:20:00', '%H:%M:%S'):
    truck3.current_time = truck1.current_time
    truck3.depart_time = truck1.current_time
    package = package_hash_table.lookup(9)
    package.address = '410 S State St'
    truck3.add_package(package)
    deliver_packages(truck3, address_list, distance_matrix)
else:
    truck3.current_time = truck1.current_time
    truck3.depart_time = truck1.current_time
    deliver_packages(truck3, address_list, distance_matrix)


# Command line interface options and such
def show_menu():
    print("****************************************************************************")
    print("1. Show status of all packages for a specific time.")
    print("2. Get a single package's status with a time.")
    print("3. Show total mileage traveled by all trucks and status of packages at EOD.")
    print("4. Exit the program.")
    print("****************************************************************************")


# shows all package statuses with time info according to specified time (simulated)
def show_all_packages_status_for_time(time, trucks):
    time_obj = datetime.strptime(time, '%H:%M:%S')
    for truck in trucks:
        print(f"\nTruck {truck.id} Status at {time}:")
        for package in truck.all_packages:
            package_status = package.status
            status_time_str = time  # Default to the provided time for non-delivered packages

            # Check if package has id of 9
            if package.package_id == 9 and datetime.strptime('10:20:00', '%H:%M:%S') > time_obj:
                print(
                    f"Package ID: {package.package_id}, Address: 300 State St (wrong address), Status: {package_status} at {status_time_str}, Address will be corrected at 10:20 AM")
            else:
                # Check if the truck has not yet departed and or package delayed
                if time_obj < truck.depart_time and "Delayed" in package.special_notes:
                    package_status = "Delayed"
                elif time_obj < truck.depart_time:
                    package_status = "At Hub"
                else:  # Show delivered if time is at or after delivery time
                    if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= time_obj:
                        package_status = "Delivered"
                        status_time_str = package.delivery_time
                    elif package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') > time_obj:
                        package_status = "En route"  # Show en route if time is before delivery time
                print(
                    f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status} at {status_time_str}")


# shows single package status with time info according to specified time (simulated)
def get_single_package_status(package_id, time, trucks):
    time_obj = datetime.strptime(time, '%H:%M:%S')
    package_found = 0
    for truck in trucks:
        for package in truck.all_packages:
            if package.package_id == package_id:
                package_found = 1
                package_status = package.status
                status_time_str = time  # Default to the provided time for non-delivered packages

                # Check if the truck has not yet departed and or package delayed
                if package.package_id == 9 and datetime.strptime('10:20:00', '%H:%M:%S') > time_obj:
                    print(
                        f"Package ID: {package.package_id}, Address: 300 State St (wrong address), Status: {package_status} at {status_time_str}, Address will be corrected at 10:20 AM")
                else:
                    # Check if the truck has not yet departed and or package delayed
                    if time_obj < truck.depart_time and "Delayed" in package.special_notes:
                        package_status = "Delayed"
                    elif time_obj < truck.depart_time:
                        package_status = "At Hub"
                    else:  # Show delivered if time is at or after delivery time
                        if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= time_obj:
                            package_status = "Delivered"
                            status_time_str = package.delivery_time
                        elif package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') > time_obj:
                            package_status = "En route"  # Show en route if time is before delivery time
                    print(
                        f"Package ID: {package.package_id}, Address: {package.address}, Status: {package_status} at {status_time_str}")
    #  prints package not found if no package ID is found
    if package_found == 0:
        print("Package not found")


# shows all status of packages at end of day (simulated)
def show_total_mileage(trucks):
    total_mileage = sum([truck.total_distance for truck in trucks])
    print(f"Total mileage traveled by all trucks: {total_mileage} miles")
    time_obj = datetime.strptime('17:00:00', '%H:%M:%S')
    for truck in trucks:
        print(f"\nTruck {truck.id} Status at EOD:")
        for package in truck.all_packages:
            if package.delivery_time and datetime.strptime(package.delivery_time, '%H:%M:%S') <= time_obj:
                print(
                    f"Package ID: {package.package_id}, Address: {package.address}, Status: Delivered at {package.delivery_time}")


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
            get_single_package_status(package_id, time, [truck1, truck2, truck3])

        elif choice == "3":
            show_total_mileage([truck1, truck2, truck3])

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


main()
