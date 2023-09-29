import os
import subprocess

# Specify the directory where you want to start searching for Python files
root_directory = "src"

# Function to generate documentation for a Python file


def generate_documentation_for_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = f"docs/{module_name}"
    command = f"pdoc -o {output_dir} {file_path}"
    subprocess.run(command, shell=True)


# Recursively find and generate documentation for Python files
for root, dirs, files in os.walk(root_directory):
    for file in files:
        if file.endswith(".py"):
            python_file_path = os.path.join(root, file)
            generate_documentation_for_file(python_file_path)

print("Documentation generated successfully for all Python files.")
