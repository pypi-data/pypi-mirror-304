import bpy
import bmesh
import toml
import os
import shutil
import uuid
from mathutils import Vector
from auro_utils import Logger

logger = Logger(log_level="debug")

# read toml file
def read_toml(file_path):
    with open(file_path, 'r') as f:
        data = toml.load(f)
        return data

def calculate_combined_bounding_box(mesh_objects):
    """
    Calculate the overall 3D bounding box information for multiple objects and return the center and dimensions.

    Parameters:
        mesh_objects (list): A list of objects for which the bounding box information needs to be calculated.

    Returns:
        list: A list containing the center and dimensions of the overall bounding box.
    """

    if not mesh_objects:
        return None
    
    min_corner = Vector((float('inf'), float('inf'), float('inf')))
    max_corner = Vector((float('-inf'), float('-inf'), float('-inf')))

    # Iterate over all objects and update the overall bounding box
    for obj in mesh_objects:
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

        # Update the minimum and maximum corner points
        for corner in bbox_corners:
            min_corner = Vector((min(min_corner.x, corner.x), min(min_corner.y, corner.y), min(min_corner.z, corner.z)))
            max_corner = Vector((max(max_corner.x, corner.x), max(max_corner.y, corner.y), max(max_corner.z, corner.z)))

    # Calculate geometric center and dimensions
    center = (min_corner + max_corner) / 2
    dimensions = max_corner - min_corner

    return [list(round(coord, 3) for coord in center), 
            list(round(dim, 3) for dim in dimensions)] 


def calculate_centroid(mesh_objects):
    """
    Calculate the centroids of all MESH objects and return them.

    Parameters:
        mesh_objects (list): A list of objects for which the centroids need to be calculated.

    Returns:
        list: Coordinates of the centroids of all objects, rounded to three decimal places.
    """

    total_centroid = Vector((0.0, 0.0, 0.0))
    total_volume = 0.0
    
    for obj in mesh_objects:
        if obj.type != 'MESH':
            logger.log_warning(f"Object {obj.name} is not a mesh.")
            continue
        
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        # Calculating volume
        volume = abs(bm.calc_volume(signed=True))
        if volume > 0:
            # Get all vertex positions and calculate the center of mass of the object
            vertices = [bm.verts[i].co for i in range(len(bm.verts))]
            centroid = sum(vertices, Vector()) / len(vertices)
            total_centroid += centroid * volume
            total_volume += volume

        bm.free()

    if total_volume > 0:
        centroid_result = total_centroid / total_volume
        return [round(coord, 3) for coord in centroid_result], round(total_volume, 5)
    else:
        return None

def calculate_geometry_metrics(file_path: str):
    """
    Import USD file and calculate the overall 3D bounding box, total volume of all MESH objects, and centroid.

    Parameters:
        file_path (str): The path to the USD file.

    Returns:
        tuple: Bounding box information, total volume, and centroid.
    """

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.usd_import(filepath=file_path)

    # Get all mesh objects in the scene
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    # Calculate the overall bounding box information
    bbox_info = calculate_combined_bounding_box(mesh_objects)
    
    # Determine whether scaling is needed
    if bbox_info and any(dim > 10 for dim in bbox_info[1]):
        logger.log_info("Dimensions larger than 10, scaling down by 100.")
        for obj in mesh_objects:
            obj.scale = (0.01, 0.01, 0.01)
            obj.select_set(True)
        bpy.ops.object.transform_apply(scale=True)

    # Recalculate the overall bounding box information
    bbox_info = calculate_combined_bounding_box(mesh_objects)

    # Calculate the centroid and volume of all mesh files
    centroid, total_volume = calculate_centroid(mesh_objects)

    return bbox_info, total_volume, centroid

def generate_unique_uuid(object_name, bbox_info, total_volume, namespace=uuid.NAMESPACE_DNS):
    """
    Generate a unique UUID based on the model's object name, bounding box information, and total volume.

    Parameters:
        object_name (str): The name of the object for which to generate the UUID.
        bbox_info (list): The bounding box information, structured as a list of lists.
        total_volume (float): The total volume of the object.
        namespace (uuid.UUID, optional): The UUID namespace to use for generating the UUID. Defaults to uuid.NAMESPACE_DNS.

    Returns:
        str: A unique UUID generated from the provided parameters.
    """

    bbox_info_str = ', '.join([str(item) for sublist in bbox_info for item in sublist])
    unique_string = f"{object_name},[{bbox_info_str}],{total_volume}"
    return str(uuid.uuid5(namespace, unique_string))

def check_usd_path(root_directory):
    """
    Check if a valid USD or USDA file exists in the specified root directory.
    This function ensures that a 'model' directory exists within the root directory 
    and that it contains at least one valid USD or USDA file.

    If the 'model' directory does not exist, it creates one and moves any valid 
    USD or USDA files, or specific folders (SubUSDs, textures, materials) 
    from the root directory to the newly created 'model' directory.

    Parameters:
        root_directory (str): The root directory of a single asset.

    Returns:
        bool: True if the check is successful and valid files are present, 
              raises a FileNotFoundError if no valid files are found.
    """

    entries = os.listdir(root_directory)
    file_formats = ('.usd', '.usda')
    folder_formats = ("SubUSDs", "textures", "materials")

    if "model" not in entries:
        model_directory = os.path.join(root_directory, "model")
        os.makedirs(model_directory)
        logger.log_info(f"The model folder {model_directory} did not exist, but is now created.")
        if not any(entry.endswith(file_formats) for entry in entries):
            logger.log_error(f"{root_directory} is an invalid assets folder")
            raise FileNotFoundError(f"No valid usd or usda file found in directory {root_directory}.")
        for entry in entries:
            src_path = os.path.join(root_directory, entry)
            if entry != "model":
                if entry.endswith(file_formats) or entry in folder_formats:
                    dest_path = os.path.join(model_directory, entry)
                    shutil.move(src_path, dest_path)
                    logger.log_info(f"{entry} has been moved to the {model_directory}.")
        logger.log_info(f"{root_directory} is a valid assets folder")
        return True

    else:
        model_directory = os.path.join(root_directory, "model")
        if not any(entry.endswith(file_formats) for entry in os.listdir(model_directory)):
            logger.log_error(f"{root_directory} is an invalid assets folder")
            raise FileNotFoundError(f"No valid usd or usda file found in directory {root_directory}.")
        else:
            return True

def find_usd_and_create_config(root_directory, regenerate:bool = False):
    """
    Create a config file for a object asset.

    Parameters:
        root_directory (str): The root directory where the 'model' directory and USD files are located.
        regenerate (bool): A flag indicating whether to regenerate the config file. 
                           Defaults to False.

    Returns:
        bool: True if the config.toml file is created or exists, 
              raises a FileNotFoundError if no valid USD or USDA files are found.
    """

    file_formats = ('.usd', '.usda')
    model_directory = os.path.join(root_directory, "model")
    if not os.path.exists(model_directory):
        logger.log_error(f"No valid usd or usda file found in directory {root_directory}.")
        raise FileNotFoundError(f"No valid usd or usda file found in directory {root_directory}.")
    
    for usd_file in os.listdir(model_directory):
        if usd_file.endswith(file_formats):
            config_path = os.path.join(root_directory, 'config.toml')
            if not os.path.exists(config_path) or regenerate:
                usd_file_path = os.path.join("model", usd_file)
                config_data = {
                    "model": {
                        "path": usd_file_path  # 只写入usd文件名
                    }
                }
                # 写入config.toml文件
                with open(config_path, 'w') as config_file:
                    toml.dump(config_data, config_file)
                logger.log_info(f'Created config.toml in {root_directory}')
            else:
                logger.log_info(f'config.toml already exists in {root_directory}')
            return True

    raise FileNotFoundError(f"No valid usd or usda file found in directory {root_directory}.")

def get_config_file(root_directory, regenerate: bool = False):
    """
    Returns the path to the configuration file that needs to be generated at the root directory.

    This function checks if a config.toml file has been generated based on the provided UUID.
    If the file has not been generated, it returns the path for the config file. 
    If the file already exists and `regenerate` is set to False, it returns an empty string.
    If `regenerate` is set to True, the function will recreate the config.toml file regardless of its current existence.

    Parameters:
        root_directory (str): The root directory where the config.toml file is located.
        regenerate (bool): A flag indicating whether to regenerate the config.toml file. 
                           Defaults to False.

    Returns:
        str: The path to the config.toml file if it exists or has been created, 
             otherwise returns None if the UUID is present in the config file.
    """

    config_file_path = os.path.join(root_directory, "config.toml")
    if not os.path.exists(config_file_path):
        logger.log_info(f"{config_file_path} does not exist, try to generate the file")
        find_usd_and_create_config(root_directory, regenerate=regenerate)

    if regenerate:
        find_usd_and_create_config(root_directory, regenerate=regenerate)
        logger.log_info(f"Regenerate config files for {root_directory}")
        return config_file_path
    else:
        config_data = read_toml(config_file_path)
        if 'uuid' not in config_data:
            logger.log_info(f"Find the config file {config_file_path} to be generated for the asset")
            return config_file_path
        return None