import functools
import math
from pathlib import Path

from ocp_vscode import set_port, show_object

set_port(3939)

from build123d import *

mold_wall_size = 5.0 * MM
mold_base_size = mold_wall_size / 2.0
min_concrete_size = 3.0 * MM
attach_hole_diameter = 2.2 * MM
attach_hole_radius = attach_hole_diameter
width = 20.0 * MM
thickness = min_concrete_size

parts = []

# Triangle

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        with Locations(Rotation(0, 0, 0)):
            l = 2 * width * math.sqrt(3) / 3
            Triangle(a=l, b=l, c=l, align=Align.CENTER)
        with Locations(
            (0, width / 2 / math.sqrt(3) - min_concrete_size - attach_hole_radius)
        ):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        with Locations(Rotation(0, 0, 180)):
            l = 2 * width * math.sqrt(3) / 3
            Triangle(a=l, b=l, c=l, align=Align.CENTER)
        with Locations((0, width / 2 - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


# Disk

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        radius = width / 2.0
        Circle(width / 2.0, align=Align.CENTER)
        with Locations((0, radius - min_concrete_size - attach_hole_radius)):
            Circle(attach_hole_radius, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)


for Shape in [
    Rectangle,
    functools.partial(RectangleRounded, radius=attach_hole_radius),
]:
    # Square straight

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            radius = width / 2.0
            Shape(width, width, align=Align.CENTER)
            with Locations((0, radius - min_concrete_size - attach_hole_radius)):
                Circle(attach_hole_radius, mode=Mode.SUBTRACT)
        extrude(amount=thickness)
        parts.append(ex3.part)

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            radius = width / 2.0
            Shape(width, width * 2, align=Align.CENTER)
            with Locations((0, width - min_concrete_size - attach_hole_radius)):
                Circle(attach_hole_radius, mode=Mode.SUBTRACT)
        extrude(amount=thickness)
        parts.append(ex3.part)

    # Square up straight

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            l = width / math.sqrt(2)
            with Locations(Rotation(0, 0, 45)):
                Shape(l, l, align=Align.CENTER)
            with Locations(
                (0, (width / 2 - min_concrete_size) / math.sqrt(2) - attach_hole_radius)
            ):
                Circle(attach_hole_radius, mode=Mode.SUBTRACT)
        extrude(amount=thickness)
        parts.append(ex3.part)


with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        RectangleRounded(width=width, height=width, radius=attach_hole_radius)
        Circle(width / 4, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Rectangle(width=width, height=width)
        Rectangle(width=width / 3, height=width / 3, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Circle(radius=width / 2)
        Circle(width / 6, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Circle(radius=width / 2)
        Rectangle(width=width / 3, height=width / 3, mode=Mode.SUBTRACT)
    extrude(amount=thickness)
    parts.append(ex3.part)

for _ in range(2):
    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            Rectangle(width=width / 2, height=width / 2)
        extrude(amount=thickness)
        parts.append(ex3.part)

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            RectangleRounded(
                width=width / 2, height=width / 2, radius=attach_hole_radius
            )
        extrude(amount=thickness)
        parts.append(ex3.part)

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            Circle(radius=width / 4)
        extrude(amount=thickness)
        parts.append(ex3.part)

z_pack = pack(parts, padding=mold_wall_size, align_z=True)
# show(z_pack)
# show_object(ex3_sk)

with BuildPart() as positive:
    # Adding a list of objects directly to the part
    add(z_pack)
bbox = positive.part.bounding_box()

with BuildPart() as silicon_mold:
    center = bbox.center()
    with Locations((center.X, center.Y, 0)):
        Box(
            bbox.size.X + 2 * mold_wall_size,
            bbox.size.Y + 2 * mold_wall_size,
            bbox.size.Z + mold_wall_size,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
silicon_mold.part -= positive.part

bbox = silicon_mold.part.bounding_box()
with BuildPart() as mold:
    center = bbox.center()
    with Locations((center.X, center.Y, -mold_wall_size)):
        Box(
            bbox.size.X + 2 * mold_wall_size,
            bbox.size.Y + 2 * mold_wall_size,
            bbox.size.Z + mold_wall_size,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
mold.part -= silicon_mold.part

# bbox = silicon_mold.bounding_box()
# mold = Box(
#     bbox.max.X - bbox.min.X + 2 * mold_wall_size,
#     bbox.max.Y - bbox.min.Y + 2 * mold_wall_size,
#     bbox.max.Z + mold_base_size,
#     align=(Align.CENTER, Align.CENTER, Align.MIN),
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
# show_object(positive)
# show_object(silicon_mold)
show_object(mold)
# show(part)
# show(silicon_mold)
# show(mold)

export_stl(mold.part, Path(__file__).with_name("mold.stl"))
