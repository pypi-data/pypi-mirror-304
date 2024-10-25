import os
import pathlib
import sys
import subprocess
import toml
from auro_utils import Logger
from .utils import  calculate_geometry_metrics, generate_unique_uuid, read_toml

logger = Logger(log_level="debug")

def render_thumbnail(toml_file_path: str, thumbnail_path: str = None, resolution: tuple = (340, 235)):
    """
    Generates a thumbnail image for the asset specified in the TOML file.

    Args:
        toml_file_path (str): Path to the TOML configuration file.
        thumbnail_path (str, optional): Path to save the generated thumbnail. 
                                         Defaults to the same directory as the TOML file.
        resolution (tuple, optional): Size of the thumbnail image (width, height). 
                                       Defaults to (340, 235).

    Returns:
        bool: True if the thumbnail is rendered successfully.
    """
    toml_data = read_toml(toml_file_path)
    usd_path = os.path.join(os.path.dirname(toml_file_path), toml_data['model'].get('path'))
    if thumbnail_path is None:
        thumbnail_path = toml_file_path.replace('config.toml', 'thumbnail.png')
    root_path = pathlib.Path(__file__).resolve().parent
    entry_point = os.path.join(root_path, "gen_thumbnail.py")
    exec = sys.executable
    cmd = [exec,
           entry_point,
           "--usd_path", usd_path,
           "--thumbnail_path", thumbnail_path,
           "--resolution", str(resolution[0]), str(resolution[1])
           ]
    subprocess.run(cmd)
    return True

def gen_toml(toml_file_path, client):
    """
    Generate a TOML configuration file for a given asset.

    This function reads a TOML file, calculates geometry metrics for the asset,
    and enriches the TOML data with additional information retrieved from a 
    specified client. The generated TOML includes basic information, geometry,
    physics properties, scene tags, and spatial semantics for the asset.

    Args:
        toml_file_path (str): The file path to the TOML configuration file that
                              will be generated or updated.
        client: An instance of a client used to retrieve asset-related information
                such as name, mass, friction coefficient, and spatial semantics.

    Raises:
        FileNotFoundError: If the TOML file path does not exist or is invalid.
        Exception: If there are issues reading the TOML file or if the client 
                   fails to return expected information.

    Note:
        This function expects the TOML structure to contain specific keys 
        (`basic_info`, `geometry`, `physics`, `scene`, `material`, 
        `spatial_semantics`, `uuid`). It also calculates the bounding box 
        volume and center of mass, using fallback values if necessary.
    """
    toml_data = read_toml(toml_file_path)
    default_keys = ['basic_info', 'geometry', 'physics', 'scene', 'material', 'spatial_semantics', 'uuid']
    for key in default_keys:
        toml_data.setdefault(key, {})
    
    # Get the file path and get the geometry information
    root_path = os.path.dirname(toml_file_path)
    relative_path = toml_data['model'].get('path')
    usd_path = os.path.join(root_path, relative_path)
    bbox_info, total_volume, centroid = calculate_geometry_metrics(usd_path)

    # When the volume is calculated incorrectly, use boundingbox to approximate the volume and center of mass
    if total_volume>1:
        total_volume = round(bbox_info[1][0] * bbox_info[1][1] * bbox_info[1][2], 5)
        centroid = bbox_info[0]
    toml_data['geometry']['geometry_center'] = bbox_info[0]
    toml_data['geometry']['dimensions'] = bbox_info[1]
    toml_data['geometry']['volume'] = total_volume
    toml_data['physics']['center_of_mass'] = centroid

    # Add thumbnail path to toml file
    thumbnail_relative_path = toml_data['basic_info'].get('thumbnail', 'thumbnail.png')
    thumbnail_path = os.path.join(root_path, thumbnail_relative_path)
    toml_data['basic_info']['thumbnail'] = thumbnail_relative_path

    # Use asset thumbnail to let the LLM output asset name
    object_name = client.get_asset_name(thumbnail_path)
    toml_data['basic_info']['name'] = object_name

    # Generate a unique uuid from the object's name、 bbox_info、 total_volume
    uuid_value = generate_unique_uuid(object_name, bbox_info, total_volume)
    toml_data['uuid']['value'] = uuid_value

    # Using the large model to obtain the fuzzy search name of the object
    fuzzy_names = client.get_fuzzy_name(object_name)
    toml_data['basic_info']['fuzzy_name'] = fuzzy_names

    # Use the large model to get the approximate mass of an object from its name and volume
    mass = client.get_mass(object_name, total_volume)
    friction_coefficient = client.get_friction_coefficient(object_name)
    toml_data['physics']['mass'] = mass
    toml_data['physics']['friction_coefficient'] = friction_coefficient

    # scene_tag
    scene_tag = client.get_scene_tag(object_name)
    toml_data['scene']['tag'] = scene_tag

    # materials
    materials = client.get_material(object_name)
    toml_data['material']['tag'] = materials

    # spatial_semantics
    parents, chlidren = client.get_spatial_semantics(object_name)
    toml_data['spatial_semantics']['parent'] = parents
    toml_data['spatial_semantics']['chlidren'] = chlidren
    
    with open(toml_file_path, 'w') as f:
        toml.dump(toml_data, f)
    logger.log_success(f"config file has been written to {toml_file_path}")