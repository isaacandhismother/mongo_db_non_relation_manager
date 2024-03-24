from pymongo import MongoClient
from faker import Faker
import json


# You can read a data from JSON file #
def regions():
    with open("Data\\data.json", "r") as f:
        data = json.load(f)
    return list(data.keys())


# Function to print every person's info
def print_persons(data):
    for person in data:
        for key, value in person.items():
            print(f'{key},{value}')
        print('\n')


# Main database manager class that uses pymongo to interact with DB #
class Manager:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["Database"]

    # The add_data function will take a keywords arguments as arguments
    # ,so you can add as much data as you want
    def add_data(self, collection_name, **kwargs):
        self.db[collection_name].insert_one(kwargs)

    def delete_row(self, collection_name, row_id):
        if collection_name == "advisors":
            self.db[collection_name].delete_one({"advisor_id": row_id})
        elif collection_name == "students":
            self.db[collection_name].delete_one({"student_id": row_id})

    def load_data(self, collection_name):
        return list(self.db[collection_name].find())

    def search(self, collection_name, data):
        return list(self.db[collection_name].find(data))

    def update(self, collection_name, data, new_data):
        self.db[collection_name].update_one(data, {"$set": new_data})

    def check_bd(self, collection_name):
        return self.db[collection_name].count_documents({}) > 0


if __name__ == '__main__':
    db_manager = Manager()

    # # You can get data from JSON file here

    # regions_list = regions()
    # for region in regions_list:
    #     db_manager.add_data("regions", name=region)

    # But I will use my favorite Faker library to create one
    fake = Faker()

    students_count = 100
    advisors_count = 20

    # Creating students random data
    for _ in range(students_count):
        student_data = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "age": fake.random_int(min=18, max=28)
        }
        db_manager.add_data("students", **student_data)

    # Delete a row from the students collection
    db_manager.delete_row("students", {"name": "Mary", "surname": "Jane"})

    # Printing the youngest students
    youngest_students = db_manager.search("students", {"age": 18})
    print("Youngest students are:")
    print_persons(youngest_students)

    db_manager.update("advisors", {"name": "Saba"}, {"age": 45})

    # Checking if database is empty
    print(f'Is the database filled with data?: {db_manager.check_bd("students")}')

    # Printing the students
    students = db_manager.load_data("students")
    print("Students:")
    print_persons(students)
