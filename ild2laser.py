#!/usr/bin/env python

import shutil
import os
import sys
import re

# Function to strip filename to < 8 characters
def change_to_eigth(file):
    return f"{file[0:8].strip()}.ild"

def remove_non_ascii(text):
    return ''.join([i for i in text if ord(i) < 128])

def copy_files():
    # Initializing
    arr = []
    count = 0

    # Array of items in the directory
    files = [f for f in os.listdir('To_Do')]

    for f in files:
        # If the file ends in .ild (case insensitive), it will proceed...
        if re.match('.*\.[iI][lL][dD]$', f) is not None:
            # If the length of the filename is > 8 characters, it'll strip it down
            if len(f) > 12:
                newFileName = change_to_eigth(f)
            else:
                newFileName = f
            
            # Strip Non-Ascii characters from the filename should they exist
            newFileName = remove_non_ascii(newFileName)

            # If there are duplicate names going to be written, change the name with an increasing count integer substitution
            if len(arr) == 0 or not any(x in newFileName for x in arr):
                arr.append(newFileName)
            else:
                newFileName = f"{newFileName[0:5]}{count}.ild"
                count += 1
                arr.append(newFileName)
        else:
            print(f"{f} is not a valid .ild file and cannot be processed.")
        
        # Checks if the file already exists, copies if it doesn't
        if not os.path.exists(f'./Processed/ildloves/{newFileName}'):
            shutil.copy(f'./To_Do/{f}', f'./Processed/ildloves/{newFileName}')

def generate_playlist():
    playlist_file = f'{PlayList_dir}/{playlist_filename}'
    if os.path.exists(playlist_file):
        with open(playlist_file, "r") as f:
            contents = f.readlines()
            print(contents)
            new_arr = []
            for x in contents:
                try:
                    ct = re.search("^\d*", x)
                    new_arr.append(int(ct.group()))
                except:
                    pass
            try:
                count = max(new_arr) + 1
            except:
                count = 1
    else:
        count = 1
    
    with open(playlist_file, "a+") as f:
        f.write(f"\n{count},({effect_filename})")

def generate_effects():
    effect_file = f'{PlayList_dir}/{effect_filename}'
    if os.path.exists(effect_file):
        with open(effect_file, "r") as f:
            contents = f.readlines()
            print(contents)
            new_arr = []
            for x in contents:
                try:
                    ct = re.search("^\d*", x)
                    new_arr.append(int(ct.group()))
                except:
                    pass
            try:
                count = max(new_arr) + 1
            except:
                count = 1
    else:
        count = 1
    
    toteffects = ''
    for effect in effect_vars:
        if effect_vars.get(effect):
            toteffects += f"{effect}={effect_vars[effect]}, "
    print(toteffects)

    # with open(effect_file, "w") as f:
    #     for i in contents:
    #         f.write(i)
    #     f.write(f"\n{count},({effect_filename})")

if __name__ == "__main__":

    ###############################
    ### Change these as desired ###
    ###############################

    # Playlist File Name:
    playlist_filename = "PlayList.pla"
    # Effect file name:
    effect_filename = "sami.eff"

    # Variables that alter how the item is displayed (leave empty if none required)
    effect_vars = {
    # Time
    'TI': 'YES',
    # 
    'SI': '22',
    # Rotation
    'RO': '',
    # 
    'CO': '',
    # 
    'HR': '',
    # 
    'HB': '',
    # 
    'VR': '',
    # 
    'VB': '',
    # 
    'DR': '',
    # 
    'BE': '',
    }

    #####################
    ### Running Logic ###
    #####################

    cwd = os.getcwd()
    to_do_dir = f'{cwd}/To_Do'
    ildloves_dir = f'{cwd}/Processed/ildloves'
    PlayList_dir = f'{cwd}/Processed/PlayList'

    if not os.path.exists(to_do_dir):
        os.makedirs(to_do_dir)
        sys.exit(f"Please put your .ild files in the directory {cwd}/To_Do and then re-run this program.")
    if not os.path.exists(ildloves_dir):
        os.makedirs(ildloves_dir)
    if not os.path.exists(PlayList_dir):
        os.makedirs(PlayList_dir)

    # copy_files()
    # generate_playlist()
    generate_effects()
