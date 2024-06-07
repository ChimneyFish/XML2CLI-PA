import xml.etree.ElementTree as ET
import os

def parse_xml_to_cli(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize a list to store CLI commands
    cli_commands = []

    # Helper function to properly format path segments
    def format_path_segment(tag, attrib):
        if 'name' in attrib:
            return f"{tag} {attrib['name']}"
        return tag

    # Recursively parse XML elements to form CLI commands
    def process_element(element, path):
        current_path_segment = format_path_segment(element.tag, element.attrib)
        new_path = f"{path} {current_path_segment}".strip() if path else current_path_segment

        if list(element):  # If the element has children
            for child in element:
                process_element(child, new_path)
        else:  # If the element is a leaf
            command = f"{new_path} {element.text}".strip()
            cli_commands.append(command)

    # Start processing from the root element
    process_element(root, '')

    # Remove unwanted prefix and unnecessary "entry" segments
    filtered_commands = []
    unwanted_prefix = "config devices entry localhost.localdomain "
    for cmd in cli_commands:
        if unwanted_prefix in cmd:
            cmd = cmd.replace(unwanted_prefix, "")

        # Remove unnecessary "entry" segments
        cmd = cmd.replace(" entry", "")

        filtered_commands.append(cmd)

    # Prepend 'set ' to each command
    final_commands = [f"set {cmd}" for cmd in filtered_commands]

    return final_commands

def main():
    # Prompt for input and output file locations
    input_file = input("Enter the path to the input XML file: ").strip()
    
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    output_file = input("Enter the path for the output CLI commands file: ").strip()

    # Parse the XML and get CLI commands
    try:
        cli_commands = parse_xml_to_cli(input_file)
    except ET.ParseError as e:
        print(f"Error: Failed to parse the XML file. {e}")
        return

    # Write CLI commands to the output file
    try:
        with open(output_file, 'w') as file:
            for command in cli_commands:
                file.write(command + '\n')
        print(f"CLI commands have been written to {output_file}")
    except Exception as e:
        print(f"Error: Unable to write to the file '{output_file}'. {e}")

if __name__ == "__main__":
    main()
