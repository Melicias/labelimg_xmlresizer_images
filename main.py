from PIL import Image, ImageOps
import os
import argparse
import xml.etree.ElementTree as ET
import shutil

def resize_images(folder_paths, height, width):
    for folder_path in folder_paths:
        output_folder = folder_path + '_resized2'
        os.makedirs('' + output_folder, exist_ok=False)

        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(folder_path, filename)
                output_path = os.path.join(output_folder, filename)

                with Image.open(image_path) as image:
                    image = ImageOps.exif_transpose(image)
                    resized_image = image.resize((width,height), Image.ANTIALIAS)
                    resized_image.save(output_path)
                    print(f"Resized {filename} successfully.")
            if filename.endswith(('.xml')):
                update_xml(os.path.join(folder_path, filename),os.path.join(output_folder, filename), width, height)
                print(f"Resized {filename} successfully.")

        print(f"\nAll images in folder {folder_path} resized successfully.\n")


def update_xml(xml_path,xml_output_path, new_width, new_height):
    shutil.copyfile(xml_path, xml_output_path)
    tree = ET.parse(xml_output_path)
    root = tree.getroot()

    # Update the size elements
    size_elem = root.find('size')
    width_elem = size_elem.find('width')
    height_elem = size_elem.find('height')
    
    width_ratio = new_width / int(width_elem.text)
    height_ratio = new_height / int(height_elem.text)
    
    width_elem.text = str(new_width)
    height_elem.text = str(new_height)
    
    for obj_elem in root.findall('object'):
        bbox_elem = obj_elem.find('bndbox')
        xmin_elem = bbox_elem.find('xmin')
        ymin_elem = bbox_elem.find('ymin')
        xmax_elem = bbox_elem.find('xmax')
        ymax_elem = bbox_elem.find('ymax')

        xmin = int(xmin_elem.text)
        ymin = int(ymin_elem.text)
        xmax = int(xmax_elem.text)
        ymax = int(ymax_elem.text)

        xmin_elem.text = str(int(xmin * width_ratio))
        ymin_elem.text = str(int(ymin * height_ratio))
        xmax_elem.text = str(int(xmax * width_ratio))
        ymax_elem.text = str(int(ymax * height_ratio))
    
    # Save the updated XML
    tree.write(xml_output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-he','--height', dest='height', type=int, help='height to resize')
    parser.add_argument('-w','--width', dest='width', type=int, help='width to resize')
    parser.add_argument('-f','--folders', dest='folders',action="extend", nargs="+", type=str, help='folders')
    args = parser.parse_args()

    resize_images(args.folders, args.height, args.width)