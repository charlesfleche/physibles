from pathlib import Path
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from build123d import *

mold_wall_size = 5.0 * MM
mold_base_size = mold_wall_size / 2.0
min_concrete_size = 3.0 * MM
attach_hole_diameter = 2.2 * MM
attach_hole_radius = attach_hole_diameter
width = 30.0 * MM
thickness = min_concrete_size * 3

parts = []

# Disk

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        radius = width / 2.0
        Circle(width/2.0, align=Align.CENTER)
        with Locations((0, radius - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


# Square straight

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        radius = width / 2.0
        Rectangle(width, width, align=Align.CENTER)
        with Locations((0, radius - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


# Square up straight

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        with Locations(Rotation(0, 0, 45)):
            Rectangle(width, width, align=Align.CENTER)
        with Locations((0, radius - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


# Triangle

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        with Locations(Rotation(0, 0, 180)):
            Triangle(a=width, b=width, c=width, align=Align.CENTER)
        with Locations((0, radius - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


z_pack = pack(parts, padding=mold_wall_size, align_z=True)
show(z_pack)
# show_object(ex3_sk)

# bbox = part.bounding_box()
# silicon_mold = Box(
#     bbox.max.X - bbox.min.X + 2 * mold_wall_size,
#     bbox.max.Y - bbox.min.Y + 2 * mold_wall_size,
#     bbox.max.Z  + mold_wall_size,
#     align=(Align.CENTER, Align.CENTER, Align.MIN)
# )
# silicon_mold -= part

# bbox = silicon_mold.bounding_box()
# mold = Box(
#     bbox.max.X - bbox.min.X + 2 * mold_wall_size,
#     bbox.max.Y - bbox.min.Y + 2 * mold_wall_size,
#     bbox.max.Z + mold_base_size,
#     align=(Align.CENTER, Align.CENTER, Align.MIN)
# )
# mold -= silicon_mold

# z_pack = pack(
#     [
#         part,
#         silicon_mold,
#         mold
#     ],
#     padding=5,
#     align_z=True
# )
# show(z_pack)
# show_object(part)
# show_object(silicon_mold)
# show_object(mold)
# show(part)
# show(silicon_mold)
# show(mold)

# export_stl(part, Path(__file__).with_suffix(".stl"))
