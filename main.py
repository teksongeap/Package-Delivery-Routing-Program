# Teksong Eap, WGU ID:009489418
import csv

from Package import Package


def load_package_data(hash_table):
    with open('packageData', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5])
            hash_table.insert(package.id, package)


def print_all_package_status_and_total_mileage():
    print("Printing all package status and total mileage...")


def get_single_package_status_with_time():
    print("Getting a single package status with a time...")


def get_all_package_status_with_time():
    print("Getting all package status with a time...")


def cli_main_menu():
    while True:
        print("WGUPS Delivery Route Program")
        print("----------------------------------------------")
        print("1. Print All Package Statuses and Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Statuses with a Time")
        print("4. Exit the Program")
        print("----------------------------------------------")

        choice = input("Please enter your choice (1-4): ")

        if choice == '1':
            print_all_package_status_and_total_mileage()
        elif choice == '2':
            get_single_package_status_with_time()
        elif choice == '3':
            get_all_package_status_with_time()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


# Running the CLI main menu
cli_main_menu()
