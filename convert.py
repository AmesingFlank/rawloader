import xml.etree.ElementTree as ET
import toml
import os


def load_camera_data():
    all_cameras = []
    tree = ET.parse('cameras.xml')
    cameras = tree.getroot()

    for camera_el in cameras:
        camera = {}
        camera["make"] = camera_el.attrib["make"]
        camera["model"] = camera_el.attrib["model"]
        for el in camera_el:
            if el.tag == "ID":
                camera["clean_make"] = el.attrib["make"]
                camera["clean_model"] = el.attrib["model"]
            elif el.tag == "CFA" or el.tag == "CFA2":
                color_pattern = ""
                for p in el:
                    if p.text in ["RED", "GREEN","BLUE"]:
                        color_pattern = color_pattern + p.text[0]
                    else:
                        color_pattern = color_pattern + p.text
                camera["color_pattern"] = color_pattern
            elif el.tag == "Crop":
                x = int(el.attrib["x"])
                y = int(el.attrib["y"])
                width = int(el.attrib["width"])
                height = int(el.attrib["height"])
                camera["crops"] = [y, -width, -height, x]
            elif el.tag == "Sensor":
                camera["blackpoint"] = int(el.attrib["black"])
                camera["whitepoint"] = int(el.attrib["white"])
            elif el.tag == "ColorMatrices":
                for matrix in el:
                    m = []
                    for row in matrix:
                        row_val = row.text.split()
                        for i in range(3):
                            m.append(int(row_val[i]))
                    camera["color_matrix"] = m
        all_cameras.append(camera)
    return all_cameras

def main():
    all_cameras = load_camera_data()
    for cam in all_cameras:
        if cam["make"] == "FUJIFILM":
            model = cam["clean_model"].lower()
            file_name = f"data/cameras/fuji/{model}.toml"
            if not os.path.isfile(file_name): 
                with open(file_name,"w") as f:
                    toml.dump(cam, f)

if __name__ == "__main__":
    main()