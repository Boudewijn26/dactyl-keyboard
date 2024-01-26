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

mm2units = 90 / 25.4
# thickness = 2.0 * mm2units
break_length = 0.5 * mm2units

# t_length = (0.5 * mm2units) / thickness
# t_thickness_first = 0.5 - (t_length / 2)
# t_thickness_second = 0.5 + (t_length / 2)
minimum_break_length = 5.5 * mm2units
break_spacing = 18.0 * mm2units

extra_cut = (153.857 - 152.859) * mm2units


def cut_segment(segment):
    t_length = break_length / segment.length()
    t_first = 0.5 - (t_length / 2)
    t_second = 0.5 + (t_length / 2)
    start, _ = segment.split(t_first)
    _, end = segment.split(t_second)

    return start, end


lengths = sorted([line.length() for path in paths for line in path])


broken_paths = []
for p_index, path in enumerate(paths):
    segments = []
    current_spacing = break_spacing
    treated = False

    for index, line in enumerate(path):
        if (current_spacing + line.length() / 2) >= break_spacing and (
            line.length() > minimum_break_length
        ):
            treated = True
            segments.extend(cut_segment(line))
            current_spacing = line.length() / 2
        else:
            segments.append(line)
            current_spacing = current_spacing + line.length()

    if treated:
        broken_paths.append(Path(*segments))
    else:
        print(f"uncut: {p_index}, {lengths[0:10]}")
        # lengths = sorted([line.length() for line in path])
        # if lengths[0] > 49:  # cut out for the keys
        #     broken_paths.append(path)
        # else:

# print(broken_paths)
wsvg(
    paths=broken_paths,
    attributes=attributes,
    svg_attributes=svg_attributes,
    filename="../things/broken.svg",
)
