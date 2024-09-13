import sqlite3
import sys
from User import User
import json
from Conn_Manager import ConnManager
from Filename_Validator import get_valid_filename
from Filename_Validator import get_unique_filename


# Function for presenting user with menu options and input choices to make with validation for the input
def menu_operation():
    while True:
        # Display a menu of options to the user
        menu_display()
        choice = input("Operation: ")
        if choice.lower() == "q":
            print("Quitting program.")
            sys.exit(0)
        try:
            choice_int = int(choice)
            menu_options(choice_int)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4, or Q to quit.")


# Function for menu display
def menu_display():
    print("1. Load JSON data into Database")
    print("2. Export Database to JSON object")
    print("3. Custom SQL Command")
    print("4. Print All Data in Database")
    print("Q. Quit")


# Function for responding to user input during menu operation
def menu_options(choice):
    # Loop that only accepts integers within the range 1 - 4
    # and has functions to call for each
    while True:
        if 1 <= choice <= 4:
            match choice:
                case 1:
                    menu_option_one()
                    # When the function completes, the loop is broken
                    # and the user is returned to the menu display (menu_operation())
                    break
                case 2:
                    menu_option_two()
                    break
                case 3:
                    menu_option_three()
                    break
                case 4:
                    menu_option_four()
                    break
        # Any invalid input should raise a ValueError up to the calling function (menu_operation())
        else:
            raise ValueError


# Function for menu option one, loading json files into database
def menu_option_one():
    while True:
        print("You selected to load JSON data into database.")
        # There is a check to ensure a valid file name is given by calling the filename_validator module,
        # using the get_valid_filename() function within
        # A custom message is passed to the get_valid_filename() function along with the boolean check 'False'
        # Since the user is supposed to load an existing file, the False boolean will guide the function
        # to only check if the file exists so that it can be read,
        # otherwise it will warn the user the file isn't found and to try again
        json_file = get_valid_filename("Please enter .JSON file name.: ", False)
        # After a valid file name is obtained, it is loaded into init_database() function
        # this function ensures the table 'users' exists, and goes through a process of
        # converting json objects to database rows
        init_database(json_file)
        # Using cached database connection to obtain row count for the print message below
        row_count = ConnManager.fetch_data("SELECT COUNT(*) FROM users")
        # If successful, a message is displayed to the user of the file being found and,
        # the current number of rows in the database
        print(f"File {json_file} found and database initialized with, currently, {row_count[0][0]} rows.")
        # End of loading json file into database - exit loop and return to main menu
        break


def init_database(json_file):
    while True:
        # Calls users_table() function to execute a query command
        # that creates the table 'users' if it doesn't already exist
        users_table()
        # Create list of user_obj from json objects in file so to populate rows in our database table
        # with the necessary values using the accessor methods of user_obj via read_file() function
        user_list = read_file(json_file)
        # Outer for loop that iterates through user objects
        # each iteration obtains row values for SQL INSERT from user object accessor methods
        # each iteration also performs an internal check of the user_id in the user object
        # against any user_id that might already exist in the table 'users'
        # via an inner for loop that iterates through the rows of the database
        for user_obj in user_list:
            user_id = user_obj.get_id()
            first_name = user_obj.get_first_name()
            last_name = user_obj.get_last_name()
            age = user_obj.get_age()
            city = user_obj.get_city()
            phone_number = user_obj.get_phone_num()
            # Using cached connection to fetch all rows from database
            data = ConnManager.fetch_data('SELECT * FROM users')
            # Initialized boolean check for inner for loop by setting it to 'False'
            match_found = False
            for row in data:
                # If a match is found, then set match_found check to 'True'
                # and break out of inner for loop
                if user_obj.get_id() == row[0]:
                    match_found = True
                    break
            # During this iteration of outer for loop, if match_found is still 'False' then
            # go ahead and commit the INSERT of that row of values
            if not match_found:
                ConnManager.execute_query(
                    "INSERT INTO users (user_id, first_name, last_name, age, city, phone_number) VALUES(?, ?, ?, ?, ?, ?)",
                    (user_id, first_name, last_name, age, city, phone_number))
            # Else match_found is True, the INSERT is skipped and
            # the outer for loop iterates to the next user object
        # Upon successful init of database via loading of json file,
        # break out of while loop and return to main menu
        break


# Function to read json file into user objects (python objects)
def read_file(json_file):
    # create a user_list of user_obj from the json objects in file
    with open(json_file, "r") as file:
        user_list = []
        data = json.load(file)
        for row in data:
            # loop through python dictionary and create User objects
            new_user = User(row["id"], row["first_name"], row["last_name"], row["age"], row["city"],
                            row["phone_number"])
            user_list.append(new_user)
    return user_list


# Function to execute sql command to create users table if it doesn't exist
def users_table():
    # Create Users table if it doesn't exist
    ConnManager.execute_query(""" 
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER not null primary key,
                        first_name VARCHAR(45),
                        last_name VARCHAR(45),
                        age INTEGER,
                        city VARCHAR(35),
                        phone_number VARCHAR(15)
                    )
                """)


# Function for menu option two, exporting all data to .JSON file
def menu_option_two():
    print("Exporting all data to JSON object.")
    # initialize a list to hold all user objects that will be used to then create a json file
    user_list = []
    # Pulling all database rows from table 'users' via cached db connection
    data = ConnManager.fetch_data('SELECT * FROM users')
    # Initializing each attribute for a user object with values from the current database row
    # with a for loop iterating through each row in the database, the user object is appended to user_list
    for row in data:
        user_id = row[0]
        first_name = row[1]
        last_name = row[2]
        age = row[3]
        city = row[4]
        phone_number = row[5]
        # Using the initialized attributes to create and fill a new user object (python object)
        new_user = User(user_id, first_name, last_name, age, city, phone_number)
        # Appending the newly created user object to the previously initialized user_list
        user_list.append(new_user)
    # Calling filename_validator module to get a proper .JSON file name for saving data
    # via get_unique_filename() - this differs from get_valid_filename()
    # The is_unique check in get_unique_filename() will be set to 'True'
    # Since the user is saving an existing file, the 'True' check will guide the function
    # to only check if the file exists so that it may prompt the user
    # with an option to overwrite or try entering a new file name
    json_save_file = get_unique_filename("Please enter the name for the export file.: ")
    # Passing user_list and the save file name to function for writing data to .JSON file
    write_out_json(user_list, json_save_file)
    print("File is created and ready for use.")


# Function for writing user objects (python object) into a json file
def write_out_json(user_list, file_name):
    write_out = []
    # Make a dictionary list from the User objects
    for user in user_list:
        write_out.append(user.__dict__())
    # Write to json with the dictionary list of values
    with open(file_name, "w") as file:
        json.dump(write_out, file)


# Function for menu option three
def menu_option_three():
    print("Please enter your custom SQL, there is only one table named Users, and here is the list of columns:")
    print("user_id, first_name, last_name, age, city, phone_number")
    # Main loop for user to continue trying SQL queries
    while True:
        # Input for user SQL query is removed of any beginning or
        # trailing whitespace
        query = str(input("Enter your query: ")).strip()
        # Start of check to ensure user is only trying SELECT query commands
        # by using startswith() function to grab the first word from the user input
        if not query.upper().startswith('SELECT'):
            query_split = query.split()
            query_term = query_split[0]
            print(f"Sorry {query_term} is not allowed, only Select.")
            # Return to query input
            continue
        elif query.upper().startswith('SELECT'):
            try:
                # Attempt to send user's SELECT query with cached db connection
                data = ConnManager.fetch_data(query)
                # Calling print_data() function and passing the user's results in for display
                print_data(data)
                # Initializing a boolean check for inner while loop to 'False'
                cont_check = False
                while True:
                    # Ask user if they wish to continue entering SQL input or return to main menu
                    cont = str(input("Do you wish to continue (Y) or go back to main menu (B)?: "))
                    if cont.strip().upper() == 'Y':
                        cont_check = True
                        break
                    elif cont.strip().upper() == 'B':
                        break
                    else:
                        print("Please enter either Y or B.")
                        continue
                if cont_check:
                    continue
                elif not cont_check:
                    break
            # Catching any errors with SQL input by user (incorrect usage of SELECT)
            except sqlite3.OperationalError:
                print("Something went wrong.")
                continue


# Function for menu option four, display all database rows
def menu_option_four():
    # Using cached connection to grab all rows from database
    data = ConnManager.fetch_data('SELECT * FROM users')
    # Calling print_data() function to display results
    print_data(data)


# Function that formats the printed display of database rows from SQL results
def print_data(data):
    print("\n** User list **")
    for row in data:
        print("------------")
        print(f"User ID: {row[0]}")
        print(f"{row[1]} {row[2]}")
        print(f"{row[3]}")
        print(f"{row[4]}")
        print(f"{row[5]}")
    print("------------")
    print("** End of User List **\n")


# Main method mainly handled by menu_operation()
def main():
    menu_operation()


if __name__ == "__main__":
    main()
