"""OBSPokemonHUD - Items Editor

This is the items editor script for OBS, so you can do it all self-contained
"""

from asyncio.windows_events import NULL
import json
import obspython as obs
import os.path
import csv

# Enabled for some extra debug output to the script log
debug = False

# The location for the JSON file
json_file = ""

my_settings = NULL

# Items information
items = {
    "slot1": {"id": 0},
    "slot2": {"id": 0},
    "slot3": {"id": 0},
    "slot4": {"id": 0},
    "slot5": {"id": 0},
    "slot6": {"id": 0},
}

# Load item names from items.csv
item_names = {}
with open(os.path.join(os.path.dirname(__file__), 'data/items.csv'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            item_id = int(row['Item Number'])
            item_names[item_id] = row['Item Name']
        except Exception:
            continue

def script_description():
    """Sets up the description for the Items Editor."""
    return "OBSPokemonHUD - Items Editor.\nBy Ulico (Sorry Tom)."


def script_properties():
    """Sets up the properties section of the 'Scripts' window for items editing."""
    global properties
    global my_settings

    properties = obs.obs_properties_create()

            # Add a multi-line text box for team paste and a parse button at the top
    teampaste_box = obs.obs_properties_add_text(properties, "teampaste_box", "Paste Team", obs.OBS_TEXT_MULTILINE)
    obs.obs_properties_add_button(properties, "parse_paste_button", "Parse Paste", parse_paste_button)

    # Add in a file path property for the items.json file
    obs.obs_properties_add_path(properties, "json_file", "Items JSON File", obs.OBS_PATH_FILE, "*.json", None)



    name1 = obs.obs_properties_add_text(properties, "item_name_1", "Item 1 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_1", "Item 1 (ID)", obs.OBS_TEXT_INFO)
    name2 = obs.obs_properties_add_text(properties, "item_name_2", "Item 2 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_2", "Item 2 (ID)", obs.OBS_TEXT_INFO)
    name3 = obs.obs_properties_add_text(properties, "item_name_3", "Item 3 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_3", "Item 3 (ID)", obs.OBS_TEXT_INFO)
    name4 = obs.obs_properties_add_text(properties, "item_name_4", "Item 4 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_4", "Item 4 (ID)", obs.OBS_TEXT_INFO)
    name5 = obs.obs_properties_add_text(properties, "item_name_5", "Item 5 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_5", "Item 5 (ID)", obs.OBS_TEXT_INFO)
    name6 = obs.obs_properties_add_text(properties, "item_name_6", "Item 6 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "item_id_6", "Item 6 (ID)", obs.OBS_TEXT_INFO)


    # Add callbacks to update id fields when name changes
    obs.obs_property_set_modified_callback(name1, item_name_modified)
    obs.obs_property_set_modified_callback(name2, item_name_modified)
    obs.obs_property_set_modified_callback(name3, item_name_modified)
    obs.obs_property_set_modified_callback(name4, item_name_modified)
    obs.obs_property_set_modified_callback(name5, item_name_modified)
    obs.obs_property_set_modified_callback(name6, item_name_modified)

    obs.obs_properties_add_button(properties, "save_button", "Save", save_button)

    obs.obs_properties_apply_settings(properties, my_settings)

    if debug:
        print("Function: Properties (Items Editor)")

    return properties


def resolve_name_to_id(name):
    """Helper function to resolve item name to ID."""
    name = name.strip().lower()
    for item_id, item_name in item_names.items():
        if item_name.lower() == name:
            return item_id
    return 0


def item_name_modified(props, property, settings):
    """Update the corresponding item_id_X field when item_name_X changes."""
    
    # prop_name = obs.obs_property_name(property)
    # if prop_name.startswith("item_member_name_"):
    #     try:
    #         i = int(prop_name.split("_")[-1])
    #     except ValueError:
    #         return True
    # else:
    #     return True
    
    # if property == f"item_name_{i}":
        
    # return True

    if settings is None:
        # Fallback to global my_settings
            global my_settings
            settings = my_settings

    # Extract the index i from the property name, e.g., "team_member_name_3" -> 3
    prop_name = obs.obs_property_name(property)
    if prop_name.startswith("item_name_"):
        try:
            i = int(prop_name.split("_")[-1])
        except ValueError:
            return True
    else:
        return True
        
    update_slot(props, i, settings)
    
    return True


def update_slot(props, i, settings):
    name = obs.obs_data_get_string(settings, f"item_name_{i}")
    item_id = resolve_name_to_id(name)
    obs.obs_data_set_string(settings, f"item_id_{i}", str(item_id) if item_id else "Unknown")
    items[f'slot{i}']['id'] = item_id


def script_defaults(settings):
    """Sets the default values for item slots."""
    for i in range(1, 7):
        obs.obs_data_set_default_string(settings, f"item_name_{i}", "None")
        obs.obs_data_set_default_string(settings, f"item_id_{i}", "0")
    if debug:
        print("Function: Defaults (Items Editor)")


def script_update(settings):
    """Updates the settings values for items editing."""
    global json_file, items, my_settings
    my_settings = settings

    if not obs.obs_data_get_string(settings, "json_file"):
        if debug:
            print("Conditional: Returning because no JSON file is given")
        return

    if json_file != obs.obs_data_get_string(settings, "json_file"):
        if debug:
            print("Conditional: New JSON File (Items Editor)")
        json_file = obs.obs_data_get_string(settings, "json_file")
        with open(json_file, 'r') as file:
            new_items_data = json.load(file)
        for i in range(1, 7):
            item_id = new_items_data.get(f'slot{i}', {}).get('id', 0)
            name = item_names.get(item_id, "None")
            obs.obs_data_set_string(settings, f"item_id_{i}", str(item_id))
            obs.obs_data_set_string(settings, f"item_name_{i}", name)

    for i in range(1, 7):
        name = obs.obs_data_get_string(settings, f"item_name_{i}")
        item_id = resolve_name_to_id(name)
        obs.obs_data_set_string(settings, f"item_id_{i}", str(item_id) if item_id else "Unknown")
        items[f'slot{i}']['id'] = item_id

    if debug:
        print("Function: Script Update (Items Editor)")


def save_button(properties, p):
    """Saves the items information into the items.json file that has been given."""
    global json_file, items
    if not json_file:
        return
    with open(json_file, 'w') as file:
        json.dump(items, file, indent=4)
    if debug:
        print("Function: save_items")
        print(f"JSON file: {json_file}")
        print(f"Items data: {json.dumps(items)}")


def parse_paste_button(props, prop):
    """Parse the teampaste and fill the 6 item name slots from after the @ in each block."""
    global my_settings
    settings = my_settings
    paste = obs.obs_data_get_string(settings, "teampaste_box")
    # Split into blocks by double newlines
    blocks = [b.strip() for b in paste.split("\n\n") if b.strip()]
    for i, block in enumerate(blocks[:6]):
        # The first line is like 'Tornadus @ Covert Cloak'
        name_item_line = block.splitlines()[0] if block.splitlines() else ""
        item = None
        if ' @ ' in name_item_line:
            _, item = name_item_line.split(' @ ')
            item = item.strip()

        obs.obs_data_set_string(settings, f"item_name_{i+1}", item)
        # Optionally, update id as well
        update_slot(props, i+1, settings)
        # item_id = resolve_name_to_id(item)
        # obs.obs_data_set_string(settings, f"item_id_{i+1}", str(item_id) if item_id else "Unknown")
    return True
