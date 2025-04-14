config_settings = {
    "projectnames": {
        "type": "command",
        "help": "Adjust SAST project names",
        "description": "Adjust SAST project names in projects.json file based on name mappings",
        "small": None,
        "required": False,
        "isdefault": False,
        "default": None,
        "aliases": [] },
    "groupnames": {
        "type": "command",
        "help": "Adjust SAST group names",
        "description": "Adjust SAST group names in teams.json file based on name mappings",
        "small": None,
        "required": False,
        "isdefault": False,
        "default": None,
        "aliases": [] },
    "export-folder": {
        "type": "param",
        "help": "Location of SAST exported files",
        "description": "Location of the SAST exported fileS",
        "required": False,
        "default": None,
        "datatype": "file" }
}
