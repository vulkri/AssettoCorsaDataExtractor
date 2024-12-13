import os
import argparse
from pathlib import Path
import json
import re

def main():
    # Argument parser
    parser = argparse.ArgumentParser("ac_location")
    parser.add_argument("-l", help="Assetto Corsa root directory", type=str)
    args = parser.parse_args()
    
    ac_root = args.l

    # Check if valid AC root directory
    if not os.path.isfile(ac_root+"/AssettoCorsa.exe"):
        print("Wrong Assetto Corsa root directory")
        return
    
    content = ac_root + "/content"
    cars_directory = Path(content + "/cars")
    cars_counter = 0
    cars = []

    # Iterate over all directories in content/cars
    for car in Path(cars_directory).iterdir():
        car_code = car.name
        # Ignore traffic cars
        if "traffic" in car_code.lower():
            continue
        car_data = os.path.join(cars_directory, car_code, "ui\\ui_car.json")
        # Get car name
        # Try to open as json file
        try:
            with open(car_data) as f:
                data = json.load(f, strict=False)
            # Ignore traffic cars
            if "raffic" in data["name"]:
                continue
            # Add car brand to name if missing
            if data["brand"] not in data["name"]:
                car_name = data["brand"] + " " + data["name"]
            else:
                car_name = data["name"]
            cars_counter += 1
        # Json error fallback
        except UnicodeDecodeError:
            with open(car_data, "r", encoding="utf-8") as f:
                lines = f.readlines()
                name = lines[1]
                if "name" in name:
                    car_name = name.split(":")[-1]
                    # Ignore traffic cars
                    if "raffic" in car_name:
                        continue
                    cars_counter += 1
                else:
                    continue
        except FileNotFoundError:
            print("ui file not found", car_code)
            continue
        # Cleanup car name
        car_name = re.sub(r"[^A-Za-z0-9\[\]\(\)\{\}\{.\}\- ]", "", car_name)
        car_name = car_name.strip()

        skins = []
        skins_path = os.path.join(cars_directory, car_code, "skins")
        for skin in Path(skins_path).iterdir():
            skins.append(skin.name)

        cars.append({"code": car.name, "name": car_name, "skins": skins})
        
    for car in cars:
        print(car["code"], car["name"], "| skins: ", len(car["skins"]))
    print(cars_counter)



if __name__ == '__main__':

    main()