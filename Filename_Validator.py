import os
import pathlib


# Check if the file exists at all given all other checks being passed
# Separate checking mechanisms for loading json file into database vs saving database to json file
# Loading json file into database needs to ensure the file exists
# Saving to json file needs to know if the file exists, so it can prompt the user with an option to overwrite
# or make a new file name
# is_unique is a boolean variable used by the function to know check to perform
def does_file_exist(filename, is_unique):
    if not is_unique:
        if pathlib.Path(filename).suffix == '.JSON' and not os.path.exists(filename):
            print(f"File {filename} was not found. Please make sure you didn't misspell the file name.")
            # .JSON suffix was found but full filename doesn't seem to exist
            return False
        else:
            # .JSON suffix not found
            return True
    if is_unique:
        if os.path.exists(filename):
            # File exists, will prompt user with overwrite or new filename options
            return True
        else:
            # File doesn't exist, filename will be returned for use in saving data
            return False


# Check if the filename is not empty, has a suffix (extension), is valid, and it's suffix is '.JSON'
def is_valid_filename(filename, is_unique):
    # Check if the file name is not empty
    if not filename:
        print("File name cannot be empty.")
        return False

    # Check if the file has a suffix (extension)
    if not pathlib.Path(filename).suffix:
        print(f"File {filename} contained no extension. Please make sure to include the file extension. (.JSON)")
        return False

    # Check if the filename ends with '.JSON'
    if pathlib.Path(filename).suffix and pathlib.Path(filename).suffix != '.JSON':
        print(f"Unfortunately, {pathlib.Path(filename).suffix} format is not supported, only .JSON format is.")
        return False

    # If is_unique is False a check is run to find out if the file exists,
    # so that it can actually be loaded by the code in main for the load json into database function
    # is_unique is a boolean check used to manage two separate kinds of does_file_exist() checks
    # One check is for loading json into database, the other is for saving database rows to json object
    # One must ensure a file exists to load
    # The other must warn the user if their file name will overwrite an existing file
    if not is_unique:
        if not does_file_exist(filename, False):
            return False

    # If all checks pass, then return True as the file name should be acceptable
    return True


# Prompt the user until a valid .json filename is entered.
# allows custom message to be passed as string for different cases
# (such as a custom loading json file msg and a custom saving to json file msg)
def get_valid_filename(message, is_unique):
    while True:
        filename = input(message).strip()
        if is_valid_filename(filename, is_unique):
            return filename


# For saving feature
# Prompt the user for a file name and ensure it doesn't overwrite an existing file unless confirmed
def get_unique_filename(message):
    while True:
        filename = get_valid_filename(message, True)
        if does_file_exist(filename, True):
            retry_check = False
            while True:
                overwrite = str(input(f"The file '{filename}' already exists. Do you want to overwrite it? (y/n): ").strip().lower())
                if overwrite == 'y':
                    return filename
                elif overwrite == 'n':
                    print("Please enter a new file name.")
                    retry_check = True
                    break
                else:
                    print("Invalid input, please enter y or n.")
                    continue
            if retry_check:
                continue
        elif not does_file_exist(filename, True):
            return filename
