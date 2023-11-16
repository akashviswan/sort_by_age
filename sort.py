import pandas as pd
import sys

# converting the age field to some standard
# would have been much easier if  "kubectl get nodes -o yaml" was used to get creationTimestamp of each node


def convert_age_string_to_seconds(age):
    components = age.split('d')
    # If 'd' is not present, set days to 0
    days = int(components[0]) if len(components) > 1 else 0

    time = components[-1]
    hours, minutes, seconds = 0, 0, 0

    if 'h' in time:
        hours = int(time.split('h')[0])
        time = time.split('h')[1]

    if 'm' in time:
        minutes = int(time.split('m')[0])
        time = time.split('m')[1]

    if 's' in time:
        seconds = int(time.split('s')[0])

    return pd.to_timedelta(f"{days} days {hours} hours {minutes} minutes {seconds} seconds")


def main(inputfile):
    # loading the text input file and converting to a dataframe
    input = pd.read_csv(inputfile, delim_whitespace=True, header=None)

    # append datetime formatted age
    input[12] = input[3].apply(convert_age_string_to_seconds)

    # df to string
    table_string = input.sort_values(12).drop(
        12, axis=1).to_string(index=False, header=None, col_space=9)

    # Save the string representation to a file
    with open('output.txt', 'w') as file:
        file.write(table_string)


if __name__ == "__main__":
    # execute only if run as a script
    # Check if a command-line argument (file path) is provided
    if len(sys.argv) != 2:
        print("Usage: python read_csv_script.py <file_path>")
    else:
        # Get the file path from the command-line argument
        input_file = sys.argv[1]
        main(input_file)
