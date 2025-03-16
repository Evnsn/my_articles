#!/usr/bin/env python3
import shutil
import os
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

    # Update devcontainer.json
    json_path = os.path.join(target_dir, "devcontainer.json")
    with open(json_path, "r") as f:
        # Remove comments before parsing JSON
        content = f.read()
        content = re.sub(r"//.*?\n", "\n", content)  # Remove single-line comments
        content = re.sub(
            r"/\*.*?\*/", "", content, flags=re.DOTALL
        )  # Remove multi-line comments
        config = json.loads(content)

    # Update configuration
    config["name"] = f"{name}-dev"
    config["containerName"] = f"{name}-dev"
    config["workspaceFolder"] = (
        f"/workspaces/${{localWorkspaceFolderBasename}}/.devcontainer/{name}"
    )
    config["runArgs"] = [
        f"--name={name}-dev",
        f"--label=com.docker.compose.project={name}-dev",
    ]

    # Save updated configuration
    with open(json_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Created devcontainer '{name}' in .devcontainer/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python setup_new_project.py <project_name>")
        sys.exit(1)

    create_devcontainer(sys.argv[1])
