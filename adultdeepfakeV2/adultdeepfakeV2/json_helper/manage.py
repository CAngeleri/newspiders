import json
import os
import uuid

limit = 10000


class JSONHelper:
    def __init__(self, base_path, domain, threshold=limit) -> None:
        self.threshold = threshold
        self.data_array = []
        self.total_records = 0
        self.domain_name = domain
        self.base_path = base_path

    def add_data(self, data):
        if (self.total_records >= self.threshold):
            self.write_file()
            self.generate_new_file()

        self.data_array.append(data)
        self.total_records += 1

    def write_file(self):
        try:
            folder = self.base_path + self.domain_name
            filename = self.domain_name + "-" + uuid.uuid1().hex + '.json'

            if not os.path.exists(folder):
                print("Creating directory")
                os.makedirs(folder)
            with open(os.path.join(folder, filename), 'w') as out:
                json.dump(self.data_array, out, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)

    def generate_new_file(self):
        self.data_array = []
        self.total_records = 0