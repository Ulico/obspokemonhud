"""OBSPokemonHUD - Team Editor

This is the team editor script for OBS, so you can do it all self-contained
"""

from asyncio.windows_events import NULL
from glob import glob
import json
import obspython as obs
import os.path
import csv

# Enabled for some extra debug output to the script log
# True or False (they need to be capitals for Python)
debug = False

# The location for the JSON file
json_file = ""

my_settings = NULL

# Team information
team = {
    "map" : "Showdown",
    "slot1": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
    "slot2": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
    "slot3": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
    "slot4": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
    "slot5": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
    "slot6": {
        "dexnumber": 0,
        "variant" : "Standard",
        "shiny": False,
    },
}
    

def script_description():
    """Sets up the description

    This is a built-in OBS function.

    It outputs the value for the description part of the "Scripts" window for
    this script.
    """
    return "OBSPokemonHUD - Team Editor.\nAlso by Tom (edited by Ulico)."


def script_properties():
    """Sets up the properties section of the "Scripts" window.

    This is a built-in OBS function.

    It sets up the properties part of the "Scripts" screen for this script.

    Returns:
        properties
    """

    global display_type
    global v1
    global button
    global properties
    global my_settings

    # Declare the properties object for us to mess with
    properties = obs.obs_properties_create()

    # Add a multi-line text box for team paste and a parse button at the top
    teampaste_box = obs.obs_properties_add_text(properties, "teampaste_box", "Paste Team", obs.OBS_TEXT_MULTILINE)
    obs.obs_properties_add_button(properties, "parse_paste_button", "Parse Paste", parse_paste_button)

    # Add in a file path property for the team.json file
    obs.obs_properties_add_path(properties, "json_file", "Team JSON File", obs.OBS_PATH_FILE, "*.json", None)

     # Set up the sprite style dropdown
    sprite_style = obs.obs_properties_add_list(
        properties,
        "sprite_style",
        "Sprite Style",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    # Automatically build sprite maps
    sprite_types = [s for s in os.listdir(script_path()) if '.json' in s]
    for x in sprite_types:
        if 'map' in x and 'example' not in x:
            map = x.replace('map_','').replace('.json','')
            obs.obs_property_list_add_string(sprite_style, map, map)

    # ------------------------------------------------------

    name1 = obs.obs_properties_add_text(properties, "team_member_name_1", "Member 1 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_1", "Member 1 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_1", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_1", "Member 1 Shiny?")

    name2 = obs.obs_properties_add_text(properties, "team_member_name_2", "Member 2 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_2", "Member 2 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_2", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_2", "Member 2 Shiny?")

    name3 = obs.obs_properties_add_text(properties, "team_member_name_3", "Member 3 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_3", "Member 3 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_3", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_3", "Member 3 Shiny?")

    name4 = obs.obs_properties_add_text(properties, "team_member_name_4", "Member 4 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_4", "Member 4 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_4", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_4", "Member 4 Shiny?")

    name5 = obs.obs_properties_add_text(properties, "team_member_name_5", "Member 5 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_5", "Member 5 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_5", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_5", "Member 5 Shiny?")

    name6 = obs.obs_properties_add_text(properties, "team_member_name_6", "Member 6 (Name)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(properties, "team_member_dex_6", "Member 6 (Dex No.)", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_list(properties, "variant_6", "Variant", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_bool(properties, "team_member_shiny_6", "Member 6 Shiny?")

    # Remove live update callback for name fields

    button = obs.obs_properties_add_button(
        properties,  # The properties variable
        "save_button",  # Setting identifier string
        "Save",
        save_button
    )
              
    # Anytime a pokemon number changes, update the variant lists
    obs.obs_property_set_modified_callback(name1, name_modified)
    obs.obs_property_set_modified_callback(name2, name_modified)
    obs.obs_property_set_modified_callback(name3, name_modified)
    obs.obs_property_set_modified_callback(name4, name_modified)
    obs.obs_property_set_modified_callback(name5, name_modified)
    obs.obs_property_set_modified_callback(name6, name_modified)

    # When sprite_style changes, clear all team member fields
    def sprite_style_modified(props, property, settings):
        for i in range(1, 7):
            obs.obs_data_set_string(settings, f"team_member_name_{i}", "")
            obs.obs_data_set_string(settings, f"team_member_dex_{i}", "0")
            obs.obs_data_set_string(settings, f"variant_{i}", "")
        return True

    obs.obs_property_set_modified_callback(sprite_style, sprite_style_modified)

    obs.obs_properties_apply_settings(properties, my_settings)

    if debug:
        print("Function: Properties")

    # Finally, return the properties so they show up
    return properties


def name_modified(props, property, settings):
    """Update the corresponding item_id_X field when item_name_X changes."""
    
    if settings is None:
        # Fallback to global my_settings
            global my_settings
            settings = my_settings

    # Extract the index i from the property name, e.g., "team_member_name_3" -> 3
    prop_name = obs.obs_property_name(property)
    if prop_name.startswith("team_member_name_"):
        try:
            i = int(prop_name.split("_")[-1])
        except ValueError:
            return True
    else:
        return True
        
    update_slot(props, i, settings)
    
    return True

def update_slot(props, i, settings):
    name = obs.obs_data_get_string(settings, f"team_member_name_{i}")
    dex = int(resolve_name_to_dex(name).split('_')[0])
    obs.obs_data_set_string(settings, f"team_member_dex_{i}", str(dex) if dex else "Unknown")

    current_map = obs.obs_data_get_string(settings, "sprite_style")
    try:
        with open(script_path() + "map_" + current_map + ".json", 'r') as file:
            sprite_map = json.load(file)
        variant_prop = obs.obs_properties_get(props, f"variant_{i}")
        obs.obs_property_list_clear(variant_prop)
        if dex > 0 and str(dex) in sprite_map['sprites']:
            for sprite_variant in sprite_map['sprites'][str(dex)]:
                obs.obs_property_list_add_string(variant_prop, sprite_variant, sprite_variant)
    except Exception as e:
        if debug:
            print(f"Variant update error: {e}")

def script_defaults(settings):
    """Sets the default values

    This is a built-in OBS function.

    It sets all of the default values when the user presses the "Defaults"
    button on the "Scripts" screen.
    """

    # Team member dex no.
    obs.obs_data_set_default_int(settings, "team_member_dex_1", 0)
    obs.obs_data_set_default_int(settings, "team_member_dex_2", 0)
    obs.obs_data_set_default_int(settings, "team_member_dex_3", 0)
    obs.obs_data_set_default_int(settings, "team_member_dex_4", 0)
    obs.obs_data_set_default_int(settings, "team_member_dex_5", 0)
    obs.obs_data_set_default_int(settings, "team_member_dex_6", 0)

    # Team member shiny state
    obs.obs_data_set_default_bool(settings, "team_member_shiny_1", False)
    obs.obs_data_set_default_bool(settings, "team_member_shiny_2", False)
    obs.obs_data_set_default_bool(settings, "team_member_shiny_3", False)
    obs.obs_data_set_default_bool(settings, "team_member_shiny_4", False)
    obs.obs_data_set_default_bool(settings, "team_member_shiny_5", False)
    obs.obs_data_set_default_bool(settings, "team_member_shiny_6", False)

    # If debug is enabled, print out this bit of text
    if debug:
        print("Function: Defaults")

def script_update(settings):
    """Updates the settings values

    This is a built-in OBS function.

    This runs whenever a setting is changed or updated for the script. It also
    sets up and removes the timer.
    """
    global json_file
    global team
    global my_settings

    my_settings = settings
    
    #variantUpdate(v1)
    

    # If the team json file isn't given, return out so nothing happens
    if not obs.obs_data_get_string(settings, "json_file"):
        if debug:
            print("Conditional: Returning because no JSON file is given")
        return

    if json_file != obs.obs_data_get_string(settings, "json_file"):
        # If debug is enabled, print out this bit of text
        if debug:
            print("Conditional: New JSON File")

        json_file = obs.obs_data_get_string(settings, "json_file")

        with open(obs.obs_data_get_string(settings, "json_file"), 'r') as file:
            new_team_data = json.load(file)


        obs.obs_data_set_int(settings, "team_member_dex_1", new_team_data['slot1']['dexnumber'])
        obs.obs_data_set_int(settings, "team_member_dex_2", new_team_data['slot2']['dexnumber'])
        obs.obs_data_set_int(settings, "team_member_dex_3", new_team_data['slot3']['dexnumber'])
        obs.obs_data_set_int(settings, "team_member_dex_4", new_team_data['slot4']['dexnumber'])
        obs.obs_data_set_int(settings, "team_member_dex_5", new_team_data['slot5']['dexnumber'])
        obs.obs_data_set_int(settings, "team_member_dex_6", new_team_data['slot6']['dexnumber'])

        obs.obs_data_set_bool(settings, "team_member_shiny_1", new_team_data['slot1']['shiny'])
        obs.obs_data_set_bool(settings, "team_member_shiny_2", new_team_data['slot2']['shiny'])
        obs.obs_data_set_bool(settings, "team_member_shiny_3", new_team_data['slot3']['shiny'])
        obs.obs_data_set_bool(settings, "team_member_shiny_4", new_team_data['slot4']['shiny'])
        obs.obs_data_set_bool(settings, "team_member_shiny_5", new_team_data['slot5']['shiny'])
        obs.obs_data_set_bool(settings, "team_member_shiny_6", new_team_data['slot6']['shiny'])

    for i in range(1, 7):
        name = obs.obs_data_get_string(settings, f"team_member_name_{i}")
        dex = int(resolve_name_to_dex(name).split('_')[0])

        team[f'slot{i}']['dexnumber'] = dex
        team[f'slot{i}']['variant'] = obs.obs_data_get_string(settings, f"variant_{i}")
        team[f'slot{i}']['shiny'] = obs.obs_data_get_bool(settings, f"team_member_shiny_{i}")
    team['map'] = obs.obs_data_get_string(settings, "sprite_style")

    # If debug is enabled, print out this bit of text
    if debug:
        print("Function: Script Update")


def save_button(properties, p):
    """Saves the team information in to the team.json file that has been given

    Returns:
        None: Returns / exits the function if no JSON file is set
    """

    global json_file
    global team

    

    if not json_file:
        return

    with open(json_file, 'w') as file:
        json.dump(team, file, indent=4)

    if debug:
        print("Function: save_team")
        print(f"JSON file: {json_file}")
        print(f"Team data: {json.dumps(team)}")

# Load pokemon names and dex numbers from data/pokemon.csv
pokemon_name_to_dex = {}
with open(os.path.join(os.path.dirname(__file__), 'data/pokemon.csv'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            dex = row['Number'].strip().lower()
            name = row['Name'].strip().lower()
            pokemon_name_to_dex[name] = dex
        except Exception:
            continue

def resolve_name_to_dex(name):
    return pokemon_name_to_dex.get(name.strip().lower(), '0')


def script_path():
    return os.path.dirname(os.path.abspath(__file__)) + os.sep

def parse_paste_button(props, prop):
    """Parse the teampaste and fill the 6 name slots, updating shiny as well."""
    global my_settings
    settings = my_settings
    paste = obs.obs_data_get_string(settings, "teampaste_box")
    # Split into blocks by double newlines
    blocks = [b.strip() for b in paste.split("\n\n") if b.strip()]

    for i, block in enumerate(blocks[:6]):
        lines = block.splitlines()
        # The first line is like 'Tornadus @ Covert Cloak'
        name_item_line = lines[0] if lines else ""
        if ' @ ' in name_item_line:
            name, _ = name_item_line.split(' @ ')
            name = name.strip()
        else:
            name = name_item_line.strip()
        # Check for nickname/gender
        if '(' in name and ')' in name:
            parts = name.split('(')
            parts = [part.strip().strip(')') for part in parts]
            if parts[-1] in ['M', 'F']:
                name = parts[-2]
            else:
                name = parts[-1]
        # Shiny detection
        shiny = False
        for line in lines:
            if line.strip().lower().startswith('shiny'):
                shiny = True
                break
        # Optionally, update dex as well
        dex = resolve_name_to_dex(name)
        if '_' in dex:
            obs.obs_data_set_string(settings, f"team_member_name_{i+1}", name.split('-')[0])
        else:
            obs.obs_data_set_string(settings, f"team_member_name_{i+1}", name)
        obs.obs_data_set_bool(settings, f"team_member_shiny_{i+1}", shiny)
        team[f'slot{i+1}']['shiny'] = shiny
        update_slot(props, i+1, settings)
        # Set variant if possible
        variant_prop = obs.obs_properties_get(props, f"variant_{i+1}")
        variant_set = False
        if '-' in name:
            variant_candidate = name.split('-', 1)[1].strip().lower()
            # Check if this variant is in the dropdown options
            if variant_prop is not None:
                for idx in range(obs.obs_property_list_item_count(variant_prop)):
                    if obs.obs_property_list_item_string(variant_prop, idx).lower() == variant_candidate:
                        obs.obs_data_set_string(settings, f"variant_{i+1}", variant_candidate)
                        variant_set = True
                        break
        if not variant_set and variant_prop is not None and obs.obs_property_list_item_count(variant_prop) > 0:
            # Try to set to "Standard" if available, otherwise use the first option
            standard_idx = -1
            for idx in range(obs.obs_property_list_item_count(variant_prop)):
                if obs.obs_property_list_item_string(variant_prop, idx).lower() == "standard":
                    standard_idx = idx
                    break
            if standard_idx != -1:
                obs.obs_data_set_string(settings, f"variant_{i+1}", "standard")
            else:
                first_variant = obs.obs_property_list_item_string(variant_prop, 0)
                obs.obs_data_set_string(settings, f"variant_{i+1}", first_variant)

        team[f'slot{i+1}']['variant'] = obs.obs_data_get_string(settings, f"variant_{i+1}")
        team[f'slot{i+1}']['dexnumber'] = int(dex.split('_')[0])

    return True