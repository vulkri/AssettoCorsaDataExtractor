import os
import argparse
from pathlib import Path
import json
import re
import shutil
import time

# Get car name
def get_car_name(car_data, car_code):
    # Try to open as json file
    try:
        with open(car_data) as f:
            data = json.load(f, strict=False)
        # Ignore traffic cars
        if "raffic" in data["name"]:
            return("error: traffic car")
        # Add car brand to name if missing
        if data["brand"] not in data["name"]:
            car_name = data["brand"] + " " + data["name"]
        else:
            car_name = data["name"]
    # Json error fallback
    except UnicodeDecodeError:
        with open(car_data, "r", encoding="utf-8") as f:
            lines = f.readlines()
            name = lines[1]
            if "name" in name:
                car_name = name.split(":")[-1]
                # Ignore traffic cars
                if "raffic" in car_name:
                    return("error: traffic car")
            else:
                return("error: car name not found")
    except FileNotFoundError:
        return("error: ui file not found")
    # Cleanup car name
    car_name = re.sub(r"[^A-Za-z0-9\[\]\(\)\{\}\{.\}\- ]", "", car_name)
    car_name = car_name.strip()
    return car_name

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
    temp_dir = "temp"
    temp_skins_dir = os.path.join(temp_dir, "skins")

    # Delete temp dirs
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    # Create temp dirs
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if not os.path.exists(temp_skins_dir):
        os.makedirs(temp_skins_dir)

    # Iterate over all directories in content/cars
    for car in Path(cars_directory).iterdir():
        car_code = car.name
        # Ignore traffic cars
        if "traffic" in car_code.lower():
            continue
        car_data = os.path.join(cars_directory, car_code, "ui\\ui_car.json")
        car_name = get_car_name(car_data, car_code)
        if "error" in car_name:
            print(car_name, car_code)
            continue
        cars_counter += 1
        # Get car skins
        skins = []
        skins_path = os.path.join(cars_directory, car_code, "skins")
        for skin in Path(skins_path).iterdir():
            skins_temp_dir = os.path.join(temp_skins_dir, car_code)
            livery = os.path.join(skin.absolute(), "livery.png")
            skin_temp_path = os.path.join(temp_skins_dir, car_code, skin.name + ".png")
            if not os.path.exists(skins_temp_dir):
                os.makedirs(skins_temp_dir)
            if os.path.exists(livery):
                shutil.copy(livery, skin_temp_path)
            skins.append(skin.name)

        cars.append({"code": car_code, "name": car_name, "skins": skins})
        
    #for car in cars:
    #    print(car["code"], car["name"], "| skins: ", len(car["skins"]))
    print(cars_counter)



if __name__ == '__main__':

    main()