import csv
import re
import os
import sys


class CSVFileHandler:
    def __init__(self):
        # Regex patterns for name and number validation
        self.name_pattern = r'^[a-zA-Z\s]+$'
        self.number_pattern = r'^\d+$'
        self.finding_number_path = self.folder_creation()
        self.fileName = "favorites.csv"
        self.filePath = self.finding_number_path + "\\" + self.fileName

    def folder_creation(self):
        try:
            # Create the Banking folder on the Desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            self.finding_number_path = os.path.join(desktop_path, "Finding_Number")
            print(self.finding_number_path)
            file_exists = os.path.exists(self.finding_number_path)
            print(file_exists)
            if not file_exists:
                os.makedirs(self.finding_number_path)
                print("Banking folder created successfully!")
                return self.finding_number_path
            else:
                print("Main Folder already exists.")
                return self.finding_number_path
        except FileExistsError as e:
            print("File already exist in the given path.")
        except PermissionError:
            print("You cannot create a file or folder to the given path. Please change directory.")
        except FileNotFoundError:
            print("File not found in the given path.")

    def validate_input(self, input_str, pattern):
        """Validates the input string based on the provided regex pattern."""
        while not re.match(pattern, input_str):
            if pattern == self.name_pattern:
                print(f"Invalid input. '{input_str}' is not a valid name. Please enter a valid name.")
            elif pattern == self.number_pattern:
                print(f"Invalid input. '{input_str}' is not a valid number. Please enter a valid number.")
            input_str = input(f"Please enter the correct input: ")
        return input_str

    def get_finder_name_from_csv(self):
        """Getting the Names present in the csv file."""
        with open(self.filePath, "r") as readFile:
            reader = csv.reader(readFile)
            finding_names = [row[0] for index, row in enumerate(reader) if index != 0]  # Exclude the header
        return finding_names

    def finding_favorite(self):
        try:
            option = int(input("""Please choose the option: 
                               Press 1 for Adding Data
                               Press 2 for Finding Favorite Number
                               Press 3 to Remove
                               Press 4 to Exit
                               """
                               ))
            if option == 1:
                self.create_csv_file()
            elif option == 2:
                self.read_csv_file()
            elif option == 3:
                self.remove_name_from_csv_file()
            elif option == 4:
                sys.exit()
            else:
                print("Please select correct option.")
                self.finding_favorite()
        except ValueError:
            print("Invalid key, please enter valid option.")
            self.finding_favorite()
        except KeyboardInterrupt:
            print("Keyboard Interrupted")

    def create_csv_file(self):
        """Creates the CSV file and adds data entries."""
        try:
            if os.path.isfile(self.filePath):
                with open(self.filePath, "a", newline="") as file:  # Use "w" mode to create a new file
                    myFile = csv.writer(file)
                    no_of_datas = input("How many data's do you want to add to the file? ")
                    if no_of_datas.isdigit():
                        for i in range(int(no_of_datas)):
                            Name = input("Enter your name: ").upper()
                            Name = self.validate_input(Name, self.name_pattern)
                            finding_names = self.get_finder_name_from_csv()
                            if Name in finding_names:
                                print("Name already exists. Skipping the entry.")
                                Name = input("Enter your name: ").upper()
                                Name = self.validate_input(Name, self.name_pattern)
                                # continue
                            Favorite_Number = input("Enter your favorite Number: ")
                            Favorite_Number = self.validate_input(Favorite_Number, self.number_pattern)
                            myFile.writerow([Name, Favorite_Number])
                    else:
                        print("Please enter numeric values.")
                        file.close()
                        if os.path.exists(self.filePath):
                            os.remove(self.filePath)
                        self.create_csv_file()
                self.finding_favorite()
            else:
                with open(self.filePath, "w", newline="") as file:  # Use "w" mode to create a new file
                    myFile = csv.writer(file)
                    myFile.writerow(['Name', 'Favorite_Number'])
                    no_of_datas = input("How many data's do you want to add to the file? ")
                    if no_of_datas.isdigit():
                        for i in range(int(no_of_datas)):
                            Name = input("Enter your name: ").upper()
                            Name = self.validate_input(Name, self.name_pattern)
                            Favorite_Number = input("Enter your favorite Number: ")
                            Favorite_Number = self.validate_input(Favorite_Number, self.number_pattern)
                            myFile.writerow([Name, Favorite_Number])
                    else:
                        print("Please enter numeric values.")
                        file.close()
                        if os.path.exists(self.filePath):
                            os.remove(self.filePath)
                        self.create_csv_file()
                    self.finding_favorite()
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")
        except KeyboardInterrupt:
            print(f"Error occurred while running the program: Keyboard Interrupted")

    def read_csv_file(self):
        """Reads the CSV file and searches for the favorite number based on the finder's name."""
        print("Finding the Favorite Number of the person.")
        findingNames = self.get_finder_name_from_csv()
        print(f"Names you can find : {findingNames}")
        try:
            with open(self.filePath, 'r') as file:
                myFile = csv.DictReader(file)
                finderName = input("Enter the Name of the finder: ").upper()
                finderName = self.validate_input(finderName, self.name_pattern)
                validatedName = self.validate_input(finderName, self.name_pattern)
                for val in myFile:
                    if validatedName == val["Name"]:
                        favouriteNumber = val["Favorite_Number"]
                        try:
                            chance = 3
                            for attempt in range(chance):
                                findingNumber = input("Enter your Number to find whether it's a Favorite Number or Not: ")
                                findingNumber = self.validate_input(findingNumber, self.number_pattern)
                                if findingNumber == favouriteNumber:
                                    print("Hurrah! You found the favorite number.")
                                    break
                                elif abs(int(favouriteNumber) - int(findingNumber)) == 1:
                                    print("Very close to the favorite number.")
                                else:
                                    print('Try once more.')
                            else:
                                print("You failed to find the favorite number.")
                            break  # Exit the loop after finding the matching name

                        except ValueError:
                            print("Sorry! Only numbers are allowed.")
                            break  # Exit the loop on error

                        except KeyboardInterrupt:
                            print("Keyboard Interrupted")
                            break  # Exit the loop on interruption
                else:
                    print("User not found in the CSV file.")
                    self.read_csv_file()
        except FileNotFoundError:
            print("File not Found in the given path, please create a new file.")
            self.finding_favorite()
        except KeyboardInterrupt:
            print(f"Error occurred while running the program: Keyboard Interrupted")
        except OSError as e:
            print(f"Error occurred while creating the CSV file: {e}")

    def remove_name_from_csv_file(self):
        """Reads the CSV file and searches for the favorite number based on the finder's name."""
        print("Finding the Favorite Number of the person.")
        findingNames = self.get_finder_name_from_csv()
        print(f"Names you can remove: {findingNames}")
        try:
            with open(self.filePath, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)  # Read all rows into a list
                print(rows)
            finderName = input("Enter the Name of the finder to remove: ").upper()
            finderName = self.validate_input(finderName, self.name_pattern)

            removed = False
            updated_rows = []
            for row in rows:
                if row[0].upper() == finderName:
                    print("Name found and removed.")
                    removed = True
                else:
                    updated_rows.append(row)

            if removed:
                with open(self.filePath, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)
                print("CSV file updated successfully.")
            else:
                print("Name not found in the CSV file.")

            self.finding_favorite()
        except FileNotFoundError:
            print(f"\nFile not Found in the given path, please create a new file.")
            self.finding_favorite()
        except KeyboardInterrupt:
            print(f"\nError occurred while running the program: Keyboard Interrupted")
        except OSError as e:
            print(f"\nError occurred while removing the CSV file: {e}")


# Create an instance of the CSVFileHandler class
csv_handler = CSVFileHandler()

# Call the create_csv_file() method to create the CSV file and add data entries
csv_handler.finding_favorite()
