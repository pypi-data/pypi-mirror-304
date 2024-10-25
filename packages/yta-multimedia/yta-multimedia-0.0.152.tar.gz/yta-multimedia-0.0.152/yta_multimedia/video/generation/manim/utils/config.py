from yta_general_utils.file.writer import write_file
from yta_general_utils.file.reader import read_json_from_file
from yta_general_utils.programming.path import get_project_abspath

import json


CONFIG_MANIM_ABSPATH = get_project_abspath() + 'manim_parameters.json'

def write_manim_config_file(json_data):
    """
    Writes in the configuration file that we use to share
    parameters with manim software. This is the way to 
    share parameters to the process.
    
    TODO: I would like to be able to handle manim through 
    python code directly and not an external process I run,
    but for now this is working.
    """
    # We serialize json to str
    json_object_str = json.dumps(json_data, indent = 4)
    
    write_file(json_object_str, CONFIG_MANIM_ABSPATH)

def read_manim_config_file():
    """
    Reads the configuration file and returns it as a json
    object.
    """
    return read_json_from_file(CONFIG_MANIM_ABSPATH)