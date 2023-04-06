"""
pandas_raw_dataframe:
env_name, brain_name, search_seed, env_seed, env_sdf(string), goal(x,10), robot_urdf(string), score(x,1.15),

transformed_dataframe:
env_grid_map, (4x4) 
goal, (1x3)
robor_urdf (node_name, link_type, link_size, sensor_tag) 
1 (parent_name, node_name, joint_axis, joint_type)  (node_name, link_type, link_size, sensor_tag)
2 (parent_name, joint_axis, joint_type, node_name, link_type, link_size, sensor_tag, sensor_tag)
score_pos, (1x3)

tokenize_dataframe:
"""

import numpy as np
import xml.etree.ElementTree as ET

from src.utils.data_utils import PreprocessedData as PreprocessedData
from src.utils.data_utils import read_data as read_data
from src.utils.data_utils import save_data as save_data

class DataTransformer:
    def __init__(self):
        pass
    
    def generate_sequence(self, data_file, save_dir="./data/preprocessed", subset=None, precision=None):   
        raw_data = read_data(data_file)
        processed_data = []
        for single_data in raw_data[0:subset]:
            sdf_sequence = convert_sdf_to_gridmap(single_data.env_sdf, return_submap=True)
            goal_sequence = single_data.goal
            urdf_sequence = convert_urdf_to_sequence_v2(single_data.robot_urdf)
            score_sequence = single_data.score
            processed_data.append(PreprocessedData(sdf_sequence, goal_sequence, urdf_sequence, score_sequence))
        if precision:
            print(f"Handling precision {precision}")
            processed_data = [PreprocessedData(*seq.round_sequence(precision)) for seq in processed_data]
        file_path = save_data(save_dir, processed_data)
        return file_path

def find_direction(input_string):
    values = [float(x) for x in input_string.split()]
    direction = [0, 0, 0]
    
    for i, value in enumerate(values):
        if value > 0:
            direction[i] = 1
        elif value < 0:
            direction[i] = -1
            
    return ' '.join(map(str, direction))

def convert_urdf_to_sequence_v2(urdf_string):
    """
    output a list of dictionary, more informative but longer sequence 
    """
    root = ET.fromstring(urdf_string)
    # Extract the desired information
    sequence = []
    for element in root:
        if element.tag == "joint":
            parent_name = element.find("parent").attrib["link"]
            child_link_name = element.find("child").attrib["link"]
            joint_axis = element.find("axis").attrib["xyz"]
            joint_type = element.attrib["type"]
            joint_direction = find_direction(element.find("origin").attrib["xyz"])
            # sequence.append((parent_name, node_name, joint_axis, joint_type, joint_direction))
            joint_dict = {
                'parent_name': parent_name,
                'link_name': child_link_name,
                'joint_axis': joint_axis,
                'joint_type': joint_type,
                'joint_direction': joint_direction,
            }
            sequence.append(joint_dict)
        elif element.tag == "link":
            link_name = element.attrib["name"]
            # Extract the link type and size from the visual geometry
            visual_geometry = element.find("visual/geometry")
            link_type = None
            link_size = None
            if visual_geometry is not None:
                link_type = list(visual_geometry)[0].tag
                if link_type == "sphere":
                    radius = float(visual_geometry.find("sphere").attrib["radius"])
                    link_size = (radius,radius,radius)
                elif link_type == "box":
                    size_str = visual_geometry.find("box").attrib["size"]
                    link_size = tuple([float(s) for s in size_str.split()])
                elif link_type == "cylinder":
                    length = float(visual_geometry.find("cylinder").attrib["length"])
                    radius = float(visual_geometry.find("cylinder").attrib["radius"])
                    link_size = (radius,radius,length)

            # Extract the sensor tag (assuming it's stored in the material name attribute)
            sensor_color = element.find("visual/material").attrib["name"] if element.find("visual/material") is not None else "unknown"
            sensor_tag = True if "sensored" in sensor_color else False
            # sequence.append((node_name, link_type, link_size, sensor_tag))
            link_dict = {
                'link_name': link_name,
                'link_type': link_type,
                'link_size': link_size,
                'sensor_tag': sensor_tag,
            }
            sequence.append(link_dict)
    return sequence

def convert_urdf_to_sequence(urdf_string):
    """
    output a list of tuple
    """
    root = ET.fromstring(urdf_string)
    # Extract the desired information
    sequence = []
    for element in root:
        if element.tag == "joint":
            parent_name = element.find("parent").attrib["link"]
            node_name = element.find("child").attrib["link"]
            joint_axis = element.find("axis").attrib["xyz"]
            joint_type = element.attrib["type"]
            sequence.append((parent_name, node_name, joint_axis, joint_type))
        elif element.tag == "link":
            node_name = element.attrib["name"]
            # Extract the link type and size from the visual geometry
            visual_geometry = element.find("visual/geometry")
            link_type = None
            link_size = None
            if visual_geometry is not None:
                link_type = list(visual_geometry)[0].tag
                if link_type == "sphere":
                    radius = float(visual_geometry.find("sphere").attrib["radius"])
                    link_size = (radius,radius,radius)
                elif link_type == "box":
                    size_str = visual_geometry.find("box").attrib["size"]
                    link_size = tuple([float(s) for s in size_str.split()])
                elif link_type == "cylinder":
                    length = float(visual_geometry.find("cylinder").attrib["length"])
                    radius = float(visual_geometry.find("cylinder").attrib["radius"])
                    link_size = (radius,radius,length)

            # Extract the sensor tag (assuming it's stored in the material name attribute)
            sensor_color = element.find("visual/material").attrib["name"] if element.find("visual/material") is not None else "unknown"
            sensor_tag = True if "sensored" in sensor_color else False
            sequence.append((node_name, link_type, link_size, sensor_tag))
    return sequence

def convert_sdf_to_gridmap(sdf_string, return_submap=False):
    # Parse the SDF string
    root = ET.fromstring(sdf_string)
    # Create a grid map representation
    grid_resolution = 1  # Adjust as needed
    grid_size = [10, 10]  # Adjust as needed (this should be large enough to cover the entire space)
    grid_map = np.zeros(grid_size, dtype=np.double) #grid_map = np.zeros(grid_size, dtype=np.uint8)
    # Iterate over each model in the SDF file
    for model in root.findall(".//model"):
        # Extract box dimensions and pose
        box_size = model.find(".//box/size").text.split()
        box_size = [float(dim) for dim in box_size]
        box_pose = model.find(".//pose").text.split()
        box_position = [float(coord) for coord in box_pose[:3]]
        box_rotation = [float(angle) for angle in box_pose[3:]]
        # Fill in the grid cells corresponding to the box
        offset = [int(coord / grid_resolution + size / 2) for (coord, size) in zip(box_position[0:2],grid_size)]
        for i in range(offset[0], min(grid_size[0], offset[0] + int(box_size[0] / grid_resolution))):
            for j in range(offset[1], min(grid_size[1], offset[1] + int(box_size[1] / grid_resolution))):
                grid_map[i, j] = box_size[2] #1
    if return_submap:
        return grid_map[6:10,3:7]
    else:
        return grid_map
