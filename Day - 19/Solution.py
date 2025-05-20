# Day 19
# Challenge: Write a parser to convert Kubernetes YAML configs into JSON.
# Focus: YAML parsing
# Example Hint: Use pyyaml

import yaml
import json
import sys
from pathlib import Path

def yaml_to_json(yaml_file_path, json_file_path=None):
    """
    Convert a Kubernetes YAML config file to JSON format.
    
    Args:
        yaml_file_path (str): Path to the input YAML file
        json_file_path (str, optional): Path to save the JSON output. 
                                        If None, prints to stdout.
    """
    try:
        # Read the YAML file
        with open(yaml_file_path, 'r') as yaml_file:
            # Load all documents from the YAML file (Kubernetes files may contain multiple documents)
            yaml_docs = list(yaml.safe_load_all(yaml_file))
            
            # If single document, convert directly
            if len(yaml_docs) == 1:
                json_data = json.dumps(yaml_docs[0], indent=2)
            else:
                # For multiple documents, create a JSON array
                json_data = json.dumps(yaml_docs, indent=2)
            
            # Output the result
            if json_file_path:
                with open(json_file_path, 'w') as json_file:
                    json_file.write(json_data)
                print(f"Successfully converted {yaml_file_path} to {json_file_path}")
            else:
                print(json_data)
                
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yaml_to_json.py <input.yaml> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"Error: File {input_file} not found", file=sys.stderr)
        sys.exit(1)
    
    yaml_to_json(input_file, output_file)
