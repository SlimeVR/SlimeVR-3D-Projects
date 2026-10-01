# Renders the images used by infographic.html: python infographic.py <path to blender>
# Each project becomes render/infographic/<project>.png (transparent, 560 px/m) at the frame set below.
import os
import subprocess
import sys

PROJECTS = {
    "mounting_forward_video": 16,
    "mounting_back_video": 16,
    "mounting_tpose_up_video": 16,
    "mounting_tpose_down_video": 16,
    "mounting_forward_tiptoe_video": 16,
    "mounting_back_tiptoe_video": 16,
    "mounting_tpose_up_tiptoe_video": 16,
    "mounting_tpose_down_tiptoe_video": 16,
    "mounting_forward_kneeling_video": 16,
    "mounting_back_kneeling_video": 16,
    "mounting_tpose_up_kneeling_video": 16,
    "mounting_tpose_down_kneeling_video": 16,
}

root = os.path.dirname(os.path.abspath(__file__))
for project, frame in PROJECTS.items():
    out = os.path.join(root, "render", "infographic", project + ".png")
    setup = ("import bpy; s = bpy.context.scene; r = s.render; i = r.image_settings; "
             "i.media_type = 'IMAGE'; i.file_format = 'PNG'; i.color_mode = 'RGBA'; r.film_transparent = True; "
             "r.resolution_percentage = round(56000 * s.camera.data.ortho_scale / max(r.resolution_x, r.resolution_y)); "
             f"s.frame_set({frame}); r.filepath = {out!r}; bpy.ops.render.render(write_still=True)")
    print("Rendering", project, "frame", frame)
    subprocess.run([sys.argv[1], "-b", os.path.join(root, "projects", project + ".blend"), "--python-expr", setup],
                   check=True, stdout=subprocess.DEVNULL)
