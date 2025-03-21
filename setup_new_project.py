#!/usr/bin/env python3
import shutil
import os
import sys
import json
import re


def create_devcontainer(name: str, template_name: str = "template"):
    """Create a new devcontainer from template.

    Args:
        name: Name of the new devcontainer
        template_name: Name of the template folder within .devcontainer to use (default: "template")
    """
    # Setup paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Use template from .devcontainer directory
    template_dir = os.path.join(root_dir, ".devcontainer", template_name)
    target_dir = os.path.join(root_dir, ".devcontainer", name)

    # Check if template exists
    if not os.path.exists(template_dir):
        print(f"Error: Template '{template_name}' not found in .devcontainer/")
        available_templates = [
            d
            for d in os.listdir(os.path.join(root_dir, ".devcontainer"))
            if os.path.isdir(os.path.join(root_dir, ".devcontainer", d))
        ]
        if available_templates:
            print(f"Available templates: {', '.join(available_templates)}")
        sys.exit(1)

    # Define patterns to ignore during copy
    ignore_patterns = [".venv"]

    # Create directory and copy template, ignoring specified patterns
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    # Custom copy function to ignore specific directories
    def custom_copy_function(src, dst):
        # Skip .venv directories
        if os.path.basename(src) in ignore_patterns:
            return

        if os.path.isdir(src):
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                custom_copy_function(s, d)
        else:
            shutil.copy2(src, dst)

    # Copy files with our custom function
    custom_copy_function(template_dir, target_dir)

    # Update devcontainer.json with the name
    json_path = os.path.join(target_dir, "devcontainer.json")
    with open(json_path, "r") as f:
        # Remove comments and clean up JSON
        content = f.read()
        # Remove single-line comments
        content = re.sub(r"//.*?(?=\n|$)", "", content)
        # Remove multi-line comments
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        # Replace tabs with spaces
        content = content.replace("\t", "    ")
        # Remove trailing commas
        content = re.sub(r",(\s*[}\]])", r"\1", content)
        config = json.loads(content)

    # Update name-related fields
    config["name"] = name
    config["containerName"] = name
    config["workspaceFolder"] = (
        f"/workspaces/${{localWorkspaceFolderBasename}}/.devcontainer/{name}"
    )
    config["runArgs"] = [f"--name={name}", f"--label=com.docker.compose.project={name}"]

    # Save updated configuration
    with open(json_path, "w") as f:
        json.dump(config, f, indent=4)

    print(
        f"Created devcontainer '{name}' from template '{template_name}' in .devcontainer/"
    )
    print(f"Note: Skipped copying the following patterns: {', '.join(ignore_patterns)}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python setup_new_project.py <project_name> [template_name]")
        print("       template_name defaults to 'base' if not specified")
        sys.exit(1)

    project_name = sys.argv[1]
    template_name = sys.argv[2] if len(sys.argv) == 3 else "base"

    create_devcontainer(project_name, template_name)
