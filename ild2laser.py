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
    count = 0

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
            if len(files_arr) == 0 or not any(x in newFileName for x in files_arr):
                files_arr.append(newFileName)
            else:
                newFileName = f"{newFileName[0:5]}{count}.ild"
                count += 1
                files_arr.append(newFileName)
        else:
            print(f"{f} is not a valid .ild file and cannot be processed.")
        
        # Checks if the file already exists, copies if it doesn't
        try:
            if not os.path.exists(f'./Processed/ildfiles/{newFileName}'):
                shutil.copy(f'./To_Do/{f}', f'./Processed/ildfiles/{newFileName}')
        except:
            pass
        

def generate_playlist():
    playlist_contents = ''
    if os.path.exists(playlist_file):
        with open(playlist_file, "r") as f:
            playlist_contents = f.readlines()
            new_arr = []
            for x in playlist_contents:
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
        if not any(effect_filename in s for s in playlist_contents):
            f.write(f"{count},({effect_filename})\n")

def generate_effects():
    effects_contents = ''
    no_exists_array = []
    count = 1
    if os.path.exists(effect_file):
        with open(effect_file, "r") as f:
            effects_contents = f.readlines()
            new_arr = []
            for x in effects_contents:
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

    total_effects = ''
    for effect in effect_vars:
        if effect_vars.get(effect):
            total_effects += f"{effect}={effect_vars[effect]},"

    if os.path.exists(effect_file):
        with open(effect_file, "w+") as f:
            for i in effects_contents:
                f.write(i)

    with open(effect_file, "a+") as f:
        for file in files_arr:
            if not any(file in s for s in effects_contents):
                no_exists_array.append(file)
        for item in no_exists_array:
            f.write(f"{count},(ildfiles/{item},{total_effects})\n")
            count += 1

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
    'TI': '5',
    # 
    'SI': '22',
    # Rotation
    'RO': '',
    # 
    'CO': '',
    # 
    'HR': '',
    # 
    'HB': '23',
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

    os.chdir(os.path.dirname(__file__))
    cwd = os.getcwd()
    to_do_dir = f'{cwd}/To_Do'
    ildfiles_dir = f'{cwd}/Processed/ildfiles'
    PlayList_dir = f'{cwd}/Processed/PlayList'
    effect_file = f'{PlayList_dir}/{effect_filename}'
    playlist_file = f'{PlayList_dir}/{playlist_filename}'

    if not os.path.exists(to_do_dir):
        os.makedirs(to_do_dir)
        sys.exit(f"Please put your .ild files in the directory {cwd}/To_Do and then re-run this program.")
    if not os.path.exists(ildfiles_dir):
        os.makedirs(ildfiles_dir)
    if not os.path.exists(PlayList_dir):
        os.makedirs(PlayList_dir)

    # Array of items in the To_Do directory
    files = [f for f in os.listdir('To_Do')]
    files_arr = []

    copy_files()
    generate_playlist()
    generate_effects()
