
import math
import click
import numpy as np
from PIL import Image
from galbot_sim.core import GalbotSim

def calculate_camera_pose(aabb: np.ndarray) -> tuple:
    """
    Calculate the camera's position and orientation based on the axis-aligned bounding box (AABB) of an object.

    Args:
        aabb (np.ndarray): An array representing the axis-aligned bounding box of the object. 
                           The array should contain six elements: [xmin, ymin, zmin, xmax, ymax, zmax].

    Returns:
        tuple: A tuple containing two elements:
            - eye (np.ndarray): The calculated position of the camera.
            - look (np.ndarray): The target point the camera is looking at (the center of the bounding box).
    """
    center_x = (aabb[0] + aabb[3]) / 2
    center_y = (aabb[1] + aabb[4]) / 2
    center_z = (aabb[2] + aabb[5]) / 2
    center = np.array([center_x, center_y, center_z])

    width = aabb[3] - aabb[0]
    height = aabb[4] - aabb[1]
    depth = aabb[5] - aabb[2]

    diagonal = math.sqrt(width ** 2 + height** 2 + depth** 2)
    if center[2]<0.2: center[2] += depth/2
    look = center.copy()

    if diagonal<0.3: center-=[0.3,0.3,-0.5]
    camera_distance = diagonal *2
    
    camera_position = np.array([
        center[0] - camera_distance / math.sqrt(2),
        center[1] - camera_distance / math.sqrt(2),
        center[2] + camera_distance * 1.5])

    eye = camera_position

    return eye, look

def add_light():
    """
    Add a dome light to the USD stage if it does not already exist.
    The light is used to illuminate the scene.
    """
    from pxr import UsdLux
    import omni.usd
    stage = omni.usd.get_context().get_stage()

    # DomeLight prim path
    dome_light_path = "/World/DomeLight"

    if not stage.GetPrimAtPath(dome_light_path):
        dome_light_prim = UsdLux.DomeLight.Define(stage, dome_light_path)
        # Set the intensity of the domeLight
        dome_light_prim.GetIntensityAttr().Set(500)

@click.command()
@click.option("--usd_path", required=True, help="Path to the USD file.")
@click.option("--thumbnail_path", required=True, help="Path to save the thumbnail image.")
@click.option("--resolution", type=(int, int), default=(340, 235), help="Resolution of the thumbnail.")
def render_thumbnail(usd_path: str, thumbnail_path: str = None, resolution: tuple = (340, 235)):
    """
    Render a thumbnail image of the specified USD object and save it to the given path.

    Args:
        usd_path (str): The path to the USD file of the object to be rendered.
        thumbnail_path (str): The path where the rendered thumbnail image will be saved.
        resolution (tuple): The resolution of the thumbnail image, specified as (width, height).
    """
    # Define a temporary config file for initializing galbotsim
    config = {"prim_path": "/World/object",
              "file_path": usd_path,
              "logger_config": {"log_level": "debug"},
              "world_config": {"prim_path": "/World",
                               "add_default_ground_plane": False},
              "simulator_config": {"headless": False},
              "position" : [0.0, 0.0, 0.0],
              "orientation" : [0.0, 0.0, 0.0, 1.0],
              "scale" : [1.0, 1.0, 1.0],
              }

    galbot_sim = GalbotSim(config)
    galbot_sim.world.scene.add_ground_plane(color=np.array([0.8, 0.8, 0.8]))
    add_light()

    import omni.isaac.core.utils.prims as prim_utils
    position = [0.0, 0.0, 0.0]
    orientation =[1.0, 0.0, 0.0, 0.0]
    prim_path = config.get("prim_path", "/World/object")
    galbot_sim.logger.log_info(f"usd path is {usd_path}")
    prim = prim_utils.create_prim(
            prim_path=prim_path,
            usd_path=usd_path,
            position=position,
            orientation=orientation,
            scale=[1.0, 1.0, 1.0],
        )
    
    galbot_sim.play()
    galbot_sim.world.reset()

    from omni.isaac.core.utils.bounds import create_bbox_cache, compute_aabb
    from omni.isaac.sensor import Camera
    import omni.isaac.core.utils.viewports as viewports_utils

    prim_path = config.get("prim_path")
    bbox_cache = create_bbox_cache()
    aabb = compute_aabb(bbox_cache, prim_path, include_children=False)

    if max(abs(x) for x in aabb)>5:
        galbot_sim.world.stage.RemovePrim("/World/object")
        config["scale"] = [0.01, 0.01, 0.01]
        prim = prim_utils.create_prim(
            prim_path=prim_path,
            usd_path=usd_path,
            position=position,
            orientation=orientation,
            scale=[0.01, 0.01, 0.01],
        )

    galbot_sim.world.reset()
    aabb = compute_aabb(bbox_cache, prim_path, include_children=False)

    eye, look = calculate_camera_pose(aabb)

    camera_position = [0.0, 0.0, 0.0]
    camera_orientation =[1.0, 0.0, 0.0, 0.0]

    camera = Camera(prim_path="/World/camera",
                    position=camera_position,
                    frequency=20,
                    resolution=resolution,
                    orientation=camera_orientation)
    
    viewports_utils.set_camera_view(eye=eye,target=look,camera_prim_path="/World/camera")

    galbot_sim.world.reset()
    camera.initialize()

    for i in range(20):
        galbot_sim.world.step(render=True)

    thumbnail_img = Image.fromarray(camera.get_rgba()[:, :, :3])
    thumbnail_img.save(thumbnail_path)
    galbot_sim.logger.log_success(f"The thumbnail of model {usd_path} has been successfully saved to {thumbnail_path}.")

if __name__ == "__main__":
    render_thumbnail()
