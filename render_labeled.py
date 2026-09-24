# Run inside Blender: blender -b <file> --python render_labeled.py -- <output_dir> <name>
# Renders every frame as a still, named after the timeline marker on that frame
# (<name>_<marker>.webp). Frames without a marker are numbered (<name>_0001.webp).
import os
import re
import sys

import bpy

output_dir, name = sys.argv[sys.argv.index("--") + 1:][:2]

scene = bpy.context.scene
scene.render.image_settings.file_format = "WEBP"

markers = {}
for marker in scene.timeline_markers:
    markers.setdefault(marker.frame, []).append(marker.name)

for frame in range(scene.frame_start, scene.frame_end + 1, scene.frame_step):
    scene.frame_set(frame)
    label = re.sub(r"[^\w\-]+", "_", "_".join(markers.get(frame, []))).strip("_")
    scene.render.filepath = os.path.join(output_dir, f"{name}_{label or f'{frame:04d}'}")
    bpy.ops.render.render(write_still=True)
