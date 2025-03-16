#!/usr/bin/env python3
import shutil
import os
import sys
import json
import re


def create_devcontainer(name: str):
    """Create a new devcontainer from template."""
    # Setup paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(root_dir, "template")
    target_dir = os.path.join(root_dir, ".devcontainer", name)

    # Create directory and copy template
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    shutil.copytree(template_dir, target_dir)

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

    print(f"Created devcontainer '{name}' in .devcontainer/")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_new_project.py <project_name>")
        sys.exit(1)

    create_devcontainer(sys.argv[1])
