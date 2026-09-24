import argparse
import hashlib
import json
import os
import subprocess

VIDEO_SUFFIX = "_video"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LABELED_SCRIPT = os.path.join(SCRIPT_DIR, "render_labeled.py")

RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
CACHE_FILE = "render_cache.json"

VIDEO_SETUP = (
    "import bpy; "
    "r = bpy.context.scene.render; "
    "r.image_settings.file_format = 'FFMPEG'; "
    "r.ffmpeg.format = 'MPEG4'; "
    "r.ffmpeg.codec = 'H264'; "
    "r.ffmpeg.constant_rate_factor = 'HIGH'"
)

def hash_files(paths):
    digest = hashlib.sha256()
    for path in paths:
        digest.update(os.path.relpath(path, SCRIPT_DIR).encode())
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                digest.update(chunk)
    return digest.hexdigest()

def load_cache(cache_path):
    try:
        with open(cache_path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def shared_hash():
    # render.py itself is left out so editing the CLI does not invalidate every render
    paths = [LABELED_SCRIPT]
    for root, _, files in os.walk(RESOURCES_DIR):
        paths += [os.path.join(root, f) for f in files if not f.endswith(".blend1")]
    return hashlib.sha256(f"{hash_files(sorted(paths))}{VIDEO_SETUP}".encode()).hexdigest()

def batch_render(blender_path, projects_dir, only=None, force=False):
    render_root = os.path.abspath("render")
    os.makedirs(render_root, exist_ok=True) # Make a "render" folder in the working directory

    cache_path = os.path.join(render_root, CACHE_FILE)
    cache = load_cache(cache_path)
    common_hash = shared_hash()
 
 
    for file in sorted(os.listdir(projects_dir)):
        if file.endswith(".blend") and file != "_PROJECT_TEMPLATE.blend":
            project_path = os.path.join(projects_dir, file)
            file_stem = os.path.splitext(file)[0]
            as_video = file_stem.endswith(VIDEO_SUFFIX)
            project_name = file_stem[:-len(VIDEO_SUFFIX)] if as_video else file_stem

            if only and project_name not in only and file_stem not in only:
                continue

            output_dir = os.path.join(render_root, project_name)

            os.makedirs(output_dir, exist_ok=True)

            project_hash = hashlib.sha256(f"{hash_files([project_path])}{common_hash}{as_video}".encode()).hexdigest()
            if not force and cache.get(project_name) == project_hash and os.listdir(output_dir):
                print(f"\nSkipping {file} (unchanged)")
                continue

            if as_video:
                render_path = os.path.abspath(os.path.join(output_dir, project_name))
                command = [
                    blender_path,
                    "-b", project_path,
                    "--python-expr", VIDEO_SETUP,
                    "-o", render_path,
                    "-a"
                ]
            else:
                render_path = os.path.abspath(os.path.join(output_dir, f"{project_name}_<label or frame>"))
                command = [
                    blender_path,
                    "-b", project_path,
                    "--python", LABELED_SCRIPT,
                    "--", os.path.abspath(output_dir), project_name
                ]

            print(f"\nRendering {file} as {'video' if as_video else 'images'}")
            print("Output path template:", render_path)
            if subprocess.run(command).returncode == 0:
                cache = load_cache(cache_path)
                cache[project_name] = project_hash
                with open(cache_path, "w") as f:
                    json.dump(cache, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Batch render Blender projects. Files suffixed with '{VIDEO_SUFFIX}' are rendered as MP4 video, others as WEBP frames.")
    parser.add_argument("blender_path", help="Path to the Blender executable")
    parser.add_argument("projects_dir", nargs="?", default=os.path.abspath("projects"),
                        help="Directory containing .blend files (default: ./projects)")
    parser.add_argument("--only", metavar="PROJECT", nargs="+", default=None,
                        help="Only render these project names, without .blend (default: all)")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Render even if the project has not changed since the last render")
    args = parser.parse_args()

    batch_render(args.blender_path, args.projects_dir, set(args.only) if args.only else None, args.force)
