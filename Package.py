class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight_kilo = weight_kilo
        self.special_notes = special_notes
        self.status = "AtHub"  # Default status
        self.depart_time = None  # Default depart time
        self.delivery_time = None  # Default delivery time

    def __str__(self):
        return f"Package ID: {self.package_id}, Address: {self.address}, Status: {self.status}"

    def update_status(self, status, delivery_time=None):
        self.status = status
        if delivery_time:
            self.delivery_time = delivery_time
