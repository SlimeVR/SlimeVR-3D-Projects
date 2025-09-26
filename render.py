import os
import subprocess
import sys

def batch_render(blender_path, projects_dir):
    render_root = os.path.abspath("render")
    os.makedirs(render_root, exist_ok=True) # Make a "render" folder in the working directory

    # Loop through all .blend files
    for file in os.listdir(projects_dir):
        if file.endswith(".blend") and file != "_PROJECT_TEMPLATE.blend":
            project_path = os.path.join(projects_dir, file)
            project_name = os.path.splitext(file)[0]
            output_dir = os.path.join(render_root, project_name)

            os.makedirs(output_dir, exist_ok=True)

            render_path = os.path.abspath(os.path.join(output_dir, f"{project_name}_####")) # Absolute output path with project name + frame placeholder

            command = [
                blender_path,
                "-b", project_path,
                "-o", render_path,
                "-F", "PNG",
                "-a"
            ]

            print(f"\nRendering {file}")
            print("Output path template:", render_path)
            subprocess.run(command)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_render.py <blender_path> [projects_dir (optional)]")
        sys.exit(1)

    blender_path = sys.argv[1]

    if len(sys.argv) >= 3:
        projects_dir = sys.argv[2]
    else:
        projects_dir = os.path.abspath("projects")

    batch_render(blender_path, projects_dir)
