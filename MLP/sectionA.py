"""
CS340 Course Project

This program will offer a 6 option menu that reads data from
a txt file.

Open source code, released under the GNU Public License
Pavlos Constantinou, 20210366@student.act.edu 09/05/2023
"""
import matplotlib.pyplot as plt
plt.rcdefaults()


# menu display function
def menuoptions():
    print("==================================================")
    print("USER MENU: NBA SPORTS STATISTICS DATA PROCESSING")
    print("==================================================")
    print("1. Read and display the NBA stats data for the top 10 players")
    print("2. Filter data by a threshold based on points per game")
    print("3. Calculate a new performance metric, display stats data")
    print("4. Display a column graph based on the new metric")
    print("5. Sort and display the statistics data (with the new metric)")
    print("6. Exit the program")


# options functions
def option1():
    file = open("NBA_2023_stats.txt", "r")
    print("Here is the data: \n")
    for x in file:
        print(x)
    file.close()


def option2():
    file = open("NBA_2023_stats.txt")
    data = file.readlines()
    threshold = 0.0
    try:
        threshold = float(input("Please choose a threshold from 28.3 and greater: "))
    except ValueError:
        print("Error: please enter a valid number")
        exit()
    print()
    print("Here are the players that achieved that threshold: \n")
    for line in data[1:]:  # skipping the header row
        name, mins, pts, fg, threep, reb, ast, blk, stl = line.strip().split("\t")
        if float(pts) >= threshold:
            print(name + ": " + pts + " points")
    file.close()


def option3():
    file = open("NBA_2023_stats.txt")
    data = file.readlines()[1:]

    new_data = []
    for line in data:  # skipping the header row and calculating the new metric
        name, mins, pts, fg, threep, reb, ast, blk, stl = line.strip().split("\t")
        metric = round(float(pts) * float(reb) * float(ast) * float(stl) / float(mins), 1)
        new_data.append((name, mins, pts, fg, threep, reb, ast, blk, stl, metric))

    # creating a new file and adding the 10th column
    file2 = open("NBA_processed_stats.txt", "w")
    file2.write("PLAYER\tMIN\tPTS\tFG%\t3P%\tREB\tAST\tBLK\tSTL\tPERFORMANCE\n")  # rewriting the header line

    for line in new_data:
        file2.write("\t".join(str(x) for x in line) + "\n")

    print()
    print("Here is the new processed data: \n")
    # printing the new file
    for line in new_data:
        print("\t".join(str(x) for x in line))

    file.close()
    file2.close()


def option4():
    file = open("NBA_processed_stats.txt")
    # skip the first line of the text file
    header = file.readline()
    data = []
    for line in file:
        columns = line.strip().split("\t")
        # extract column of interest
        name, mins, pts, fg, threep, reb, ast, blk, stl, metric = columns
        # convert metric to float
        metric = float(metric)
        # create a tuple of name and metric to the list
        data.append((name, metric))
    names = [x[0] for x in data]
    metrics = [x[1] for x in data]

    # create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.barh(names, metrics)

    # set axis labels and title
    ax.set_xlabel('Performance')
    ax.set_ylabel('Player')
    ax.set_title('Performance of Top 10 NBA players')

    # display the chart
    plt.show()

    file.close()


def option5():
    # Read the data from file
    file = open('NBA_processed_stats.txt', 'r')
    lines = file.readlines()

    # Extract the header
    header = lines[0].strip().split('\t')

    sort_field = input("Enter the field number (1-10) to sort by: ")

    # Convert the input to an integer and subtract 1 to get the corresponding index
    sort_index = int(sort_field) - 1

    # Check if the input is valid
    if sort_index < 0 or sort_index >= len(header):
        print("Invalid field number")
        exit()

    sort_order = input("Enter the sort order (asc/desc): ")

    # Extract the header and data
    data = [line.strip().split('\t') for line in lines[1:]]

    # Sort the data
    data.sort(key=lambda row: row[sort_index], reverse=(sort_order == 'desc'))

    # Display the sorted data
    print('\t'.join(header))
    for row in data:
        print('\t'.join(row))

    # Save the sorted data to a new file
    file2 = open('NBA_sorted_stats.txt', 'w')
    file2.write('\t'.join(header) + '\n')
    for row in data:
        file2.write('\t'.join(row) + '\n')

    # Read the sorted data back into memory
    file2read = open('NBA_sorted_stats.txt', 'r')
    sorted_lines = file2read.readlines()

    # Display the sorted data from the file
    print('\nSorted Data from File:')
    for line in sorted_lines:
        print(line.strip())

    file.close()
    file2.close()
    file2read.close()


menuoptions()
option = int(input("Please select an option: "))

while option != 6:
    if option == 1:
        option1()
    elif option == 2:
        option2()
    elif option == 3:
        option3()
    elif option == 4:
        option4()
    elif option == 5:
        option5()
    else:
        print("Invalid option, try again.")

    print()
    menuoptions()
    option = int(input("Please select an option: "))

print("Thank you for using this program!")
