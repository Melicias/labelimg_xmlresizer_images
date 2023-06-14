import os
import xml.etree.ElementTree as ET
import cv2

def create_xml(image_path, output_path):
    # Extract the image name from the file path
    image_name = os.path.basename(image_path)
    
    im = cv2.imread(image_path)
    h, w, c = im.shape
    
    
    # Create the root element
    annotation = ET.Element("annotation")

    # Add the child elements and their contents
    folder = ET.SubElement(annotation, "folder")
    folder.text = ""

    filename = ET.SubElement(annotation, "filename")
    filename.text = image_name

    path = ET.SubElement(annotation, "path")
    path.text = image_name

    source = ET.SubElement(annotation, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = str(w)
    height = ET.SubElement(size, "height")
    height.text = str(h)
    depth = ET.SubElement(size, "depth")
    depth.text = "3"

    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"

    obj = ET.SubElement(annotation, "object")
    name = ET.SubElement(obj, "name")
    name.text = "1"
    pose = ET.SubElement(obj, "pose")
    pose.text = "Unspecified"
    truncated = ET.SubElement(obj, "truncated")
    truncated.text = "1"
    difficult = ET.SubElement(obj, "difficult")
    difficult.text = "0"
    bndbox = ET.SubElement(obj, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = "1"
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = "1"
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(w)
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(h)

    # Create the XML tree
    tree = ET.ElementTree(annotation)

    # Write the XML tree to a file
    xml_file = os.path.join(output_path, f"{os.path.splitext(image_name)[0]}.xml")
    tree.write(xml_file)

# Directory containing the images
image_directory = "splited/test/1c"

# Directory where the XML files will be saved
output_directory = "splited/test/1c"

# Iterate over each image in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_directory, filename)
        create_xml(image_path, output_directory)
