import csv
import os

class CarBase:
    def __init__(self, brand, photo_file_name, carrying, car_type):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext

class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying, 'car')
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying, 'truck')
        body_whl_list = body_whl.split('x')
        if len(body_whl_list) != 3:
            self.body_length = 0.
            self.body_width = 0.
            self.body_height = 0.
        else:
            if isfloat(body_whl_list[0]):
                self.body_length = float(body_whl_list[0])
            else:
                self.body_length = 0.
            if isfloat(body_whl_list[1]):
                self.body_width = float(body_whl_list[1])
            else:
                self.body_width = 0.
            if isfloat(body_whl_list[2]):
                self.body_height = float(body_whl_list[2])
            else:
                self.body_height = 0.
    def get_body_volume(self):
        return self.body_length*self.body_width*self.body_height

def isfloat(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying, 'spec_machine')
        self.extra = extra

def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:       
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                newcar = None
                if len(row) == 0 or row[0] == '':
                    continue            
                newcar = creatObject(row)
                if not newcar is None:
                    car_list.append(newcar)
            except:
                    pass
    return car_list

def creatObject(row):
    newcar = None
    if row[0] == 'car' and row[1] != '' and row[3] != '' and row[5] != '' and row[2] != '':
        newcar = Car(row[1], row[3], row[5], row[2])
    elif row[0] == 'truck' and row[1] != '' and row[3] != '' and row[5] != '':
        newcar = Truck(row[1], row[3], row[5], row[4])
    elif row[0] == 'spec_machine' and row[1] != '' and row[3] != '' and row[5] != '' and row[6] != '':
        newcar = SpecMachine(row[1], row[3], row[5], row[6])

    if newcar.get_photo_file_ext() != '' and len(newcar.photo_file_name.split('.')) == 2:
        return newcar
    return None