from svgpathtools import svg2paths2, wsvg, Path

paths, attributes, svg_attributes = svg2paths2("../things/nested.svg")

units = {
    # "px" (or "no units") is 96 dpi: 1 inch/96 px * 25.4 mm/1 inch = 25.4/96 mm/px
    "": 25.4 / 96,
    "px": 25.4 / 96,
    # "pt" is 72 dpi: 1 inch/72 pt * 25.4 mm/1 inch = 25.4/72 mm/pt
    "pt": 25.4 / 72,
    # Units are Picas "pc", 6 dpi: 1 inch/6 pc * 25.4 mm/1 inch = 25.4/6 mm/pc
    "pc": 25.4 / 6,
    "cm": 10.0,
    "mm": 1.0,
    # Units are inches: 25.4 mm/1 inch
    "in": 25.4,
}

units_to_mm = 90 / 25.4
thickness = 2.0 * units_to_mm

t_length = (0.5 * units_to_mm) / thickness
t_thickness_first = 0.5 - (t_length / 2)
t_thickness_second = 0.5 + (t_length / 2)

print(t_thickness_first)
print(t_thickness_second)


def cut_segment(path, index, t_first, t_second):
    start, _ = path[index].split(t_first)
    _, end = path[index].split(t_second)

    pre_segments = path[0:index]
    post_segments = path[(index + 1) :]
    print(f"{len(path)} into {len(pre_segments)}/{len(post_segments)}")

    return Path(*pre_segments, start, end, *post_segments)


lengths = sorted([line.length() for path in paths for line in path])


broken_paths = []
for p_index, path in enumerate(paths):
    cut_thickness = False
    for index, line in enumerate(path):
        # if line.length() > 161:
        #     print(line.start.real)
        #     print(line.start.imag)
        #     print(line)
        # print(line.length())
        if (thickness - 0.08) < line.length() < (thickness + 0.08):
            cut_thickness = True
            broken_paths.append(
                cut_segment(path, index, t_thickness_first, t_thickness_second)
            )

            break

    if not cut_thickness:
        lengths = sorted([line.length() for line in path])
        if lengths[0] > 49: # cut out for the keys
            broken_paths.append(path)
        else:
          print(f"uncut: {p_index}, {lengths[0:10]}")

# print(broken_paths)
wsvg(
    paths=broken_paths,
    attributes=attributes,
    svg_attributes=svg_attributes,
    filename="../things/broken.svg",
)
