from spleeter.separator import Separator

# Initialize Spleeter with 2stems (vocals + accompaniment)
separator = Separator('spleeter:2stems')

# Input and output paths
input_file = "path/to/input.m4a"
output_folder = "path/to/output/folder"

# Perform separation
separator.separate_to_file(input_file, output_folder)

print("Separation complete! Check the output folder for results.")
