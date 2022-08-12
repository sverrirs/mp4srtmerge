#!/usr/bin/env python
# coding=utf-8
__version__ = "1.0.0"
# When modifying remember to issue a new tag command in git before committing, then push the new tag
#   git tag -a v1.0.0 -m "v1.0.0"
#   git push origin master --tags
"""
Python script to merge selected srt files into the selected mp4 file using 
MP4Box, MUST BE INSTALLED AND AVAILABLE IN PATH

MP4Box -add <Subtitle>.srt:hdlr=sbtl:lang=eng <MovieWithOutSubtitle> -out <MovieWithSubtitle>.mp4

Author: Sverrir Sigmundarson  info@sverrirs.com  https://www.sverrirs.com
"""

import sys, os.path, re, time
from pathlib import Path # to check for file existence in the file system
import argparse # Command-line argument parser
import ntpath # Used to extract file name from path for all platforms http://stackoverflow.com/a/8384788
import glob # Used to do partial file path matching (when finding SRT files on disk)
import subprocess # To execute shell commands 

LANG_TO_CODE = {
    "english": "en-US",
    "_eng": "en-US",
    "icelandic": "is-is"
}

def findSrtFiles(working_dir, mp4file_name):
    """
    # 1. All SRT files in the same directory
    # 2. If subs folder then 
    #   2.1 Any SRT files in a subfolder having the same name as the mp4 file
    #   2.2 Any SRT files in the root of the "subs" folder
    #   2.3 Any SRT files in a sub folder of "subs" having the same name as the mp4 file
    
    # Filter out any SRT files that do not have a language present in the LANG_TO_CODE dict

    # Sort the SRT files by their filenames (i.e. to support 2_English, 3_French etc)
    """

    folders_to_check = [
        working_dir,
        "{0}/{1}".format(working_dir, mp4file_name),
        "{0}/subs".format(working_dir),
        "{0}/subs/{1}".format(working_dir, mp4file_name)
    ]
    
    for subs_folder in folders_to_check:
        if not os.path.exists(subs_folder):
            continue
        candidates = [each for each in os.listdir(subs_folder) if each.endswith('.srt')]
        if( len(candidates) > 0):
            srt_files = []
            for c in candidates:
                lang_code = findLanguageCode(c) # For each of the srt files discover their language code
                if( lang_code is None ):
                    continue
                srt_files.append({
                    "path": "{0}/{1}".format(subs_folder, c),
                    "language":  lang_code
                    })
            return srt_files

    # Nothing found
    print("No subtitle files found for file {0}".format(mp4file_name))
    return None

def findLanguageCode(fileName):
    for key in LANG_TO_CODE:
        if( key in str(fileName).lower()):
            return LANG_TO_CODE[key]
    return None

# MP4Box -add <Subtitle>.srt:hdlr=sbtl:lang=eng <MovieWithOutSubtitle> -out <MovieWithSubtitle>.mp4
def execute_mp4box(working_dir, mp4file, srt_files):
    prog_args = ["MP4Box"]

    # Add all the subtitle files
    for srt_file in srt_files:
        prog_args.append("-add")
        prog_args.append("{0}:hdlr=sbtl:lang={1}".format(srt_file["path"], srt_file["language"]))

    # The input movie filename
    prog_args.append("{0}/{1}".format(working_dir, mp4file.name))

    # The output movie filename
    merged_file_name = "{0}/{1}.subs".format(working_dir, mp4file.stem)
    prog_args.append("-out")
    prog_args.append(merged_file_name)

    # Force a UTF8 environment for the subprocess so that files with non-ascii characters are read correctly
    # for this to work we must not use the universal line endings parameter
    my_env = os.environ
    my_env['PYTHONIOENCODING'] = 'utf-8'

    # Run the app and collect the output
    ret = subprocess.Popen(prog_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=my_env)
    try:
        while True:
            try:
                line = ret.stdout.readline()
                if not line:
                    break
                line = line.strip()
                print(line)
            except UnicodeDecodeError:
                continue # Ignore all unicode errors, don't care!
        # Ensure that the return code was ok before continuing
        # Check if child process has terminated. Set and return returncode attribute. Otherwise, returns None.
        retcode = ret.poll()
        while retcode is None:
            retcode = ret.poll()
    except KeyboardInterrupt:
        ret.terminate()
        raise

    # If the process did not return an OK then we raise an error
    if ret.returncode != 0:
        raise RuntimeError("Unable to execute MP4box tool correctly, has it been installed and is it part of the system PATH variable?")

    return merged_file_name

def parseArguments():
    parser = argparse.ArgumentParser()
  
    parser.add_argument("-i", "--input", help="The input mp4 file that should be processed",
                                         type=str, 
                                         required=True)

    parser.add_argument("-d", "--dir", help="Applies the action to all MP4 files in the same directory as the file selected", 
                                       action="store_true")

    return parser.parse_args()

def run_single_mp4(mp4file, working_dir):
    
    # Find all the srt files and attempt to extract their language codes
    srt_files = findSrtFiles(working_dir, mp4file.stem)
    if( srt_files is None or len(srt_files) <= 0):
        return 0 # No subs found, exit without error
    
    # Merge the SRT files into a new version of the MP4 file with the suffix ".subs"
    new_file_path = execute_mp4box(working_dir, mp4file, srt_files)

    # If successful then remove the old MP4 file and replace the ".subs" suffix of the new one with ".mp4"
    original_file_path = "{0}/{1}".format(working_dir, mp4file.name)
    temp_file_path = "{0}/{1}.orig".format(working_dir, mp4file.stem)
    os.rename(original_file_path, temp_file_path)
    os.rename(new_file_path, original_file_path)
    os.remove(temp_file_path)

    # Finally delete all the subtitle files
    for srt_file in srt_files:
        os.remove(srt_file["path"])
        # Figure out if the subtitle directories are empty now and delete them as needed
        srt_path = Path(srt_file["path"])
        if( len(os.listdir(srt_path.parent)) == 0):
            # Empty can be deleted
            os.rmdir(srt_path.parent)
            # Check if the parent of the parent is now empty
            if( len(os.listdir(srt_path.parent.parent)) == 0):
                # Empty can be deleted
                os.rmdir(srt_path.parent.parent)


    

    # Returning no errors, successful run
    print("{0} subtitle files merged successfully into video {1}".format(len(srt_files), mp4file.stem))


##############################################################
##############################################################
def runMain():
    # Construct the argument parser for the commandline
    args = parseArguments()

    # The mp4 video file
    mp4file = Path(args.input)
    if( mp4file.suffix != ".mp4"):
        raise ValueError("Only MP4 video files are supported")

    # Get the current working directory from the file path 
    # (place that the files are that the script should operate on)
    working_dir = str(mp4file.parent)

    # If only one file
    if( not args.dir):
        run_single_mp4(mp4file, working_dir)
        return 0
    else:
        # Find all mp4 files in the directory and run the script on every single one
        [run_single_mp4(Path(each), working_dir) for each in os.listdir(working_dir) if each.endswith('.mp4')]
        return 0

###############################################################################
# If the script file is called by itself then execute the main function
if __name__ == '__main__':
  runMain()