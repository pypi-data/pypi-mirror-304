"""
When running this script, use the following command:
blender --background --python mesh2usd.py -- -i input.obj -o output.usd
"""

import bpy
import os
import sys

def parse_cli_args():
    """Parse the input command line arguments."""
    import argparse

    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1 :]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
        f"Run blender in background mode with this script:\n\tblender --background --python {__file__} -- [options]"
    )
    parser = argparse.ArgumentParser(description=usage_text)
    # Add arguments
    parser.add_argument("-i", "--in_file", metavar="FILE", type=str, required=True, help="Path to input mesh file.")
    parser.add_argument("-o", "--out_file", metavar="FILE", type=str, required=True, help="Path to output usd file.")
    args = parser.parse_args(argv)
    # Check if any arguments provided
    if not argv or not args.in_file or not args.out_file:
        parser.print_help()
        return None
    # return arguments
    return args

def convert_mesh_to_usd(in_file: str, out_file: str):
    """Convert a mesh file to `.usd` using blender.

    Args:
        in_file: Input mesh file to process.
        out_file: Path to store output usd file.
    """
    # check valid input file
    if not os.path.exists(in_file):
        raise FileNotFoundError(in_file)
    # create directory if it doesn't exist for destination file
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
    # reset scene to empty
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # load object into scene
    if in_file.endswith(".obj"):
        bpy.ops.wm.obj_import(filepath=in_file)
    elif in_file.endswith(".stl") or in_file.endswith(".STL"):
        bpy.ops.wm.stl_import(filepath=in_file)
    elif in_file.endswith(".dae"):
        bpy.ops.wm.collada_import(filepath=in_file)
    else:
        raise ValueError(f"Input file not in obj/stl/dae format: {in_file}")

    # save it as usd file
    if not out_file.endswith(".usd"):
        out_file += ".usd"
    bpy.ops.wm.usd_export(filepath=out_file, check_existing=False)


if __name__ == "__main__":
    # read arguments
    cli_args = parse_cli_args()
    # check CLI args
    if cli_args is None:
        sys.exit()
    # process via blender
    convert_mesh_to_usd(cli_args.in_file, cli_args.out_file)