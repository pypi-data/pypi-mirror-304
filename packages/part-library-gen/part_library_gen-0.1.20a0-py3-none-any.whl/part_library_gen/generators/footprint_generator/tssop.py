from decimal import Decimal
from .footprint import Footprint
from ..components.pad import Pad
from ..components.lines import Lines
from ..components.circle import Circle


class Parameters:
    def __init__(self, pin_count: int, pin_pitch, pad_width, pad_height, pad_row_spacing):
        self.pin_count = pin_count
        self.pin_pitch = pin_pitch
        self.pad_width = pad_width
        self.pad_height = pad_height
        self.pad_row_spacing = pad_row_spacing


def generate(parameters, name):
    row_spacing = parameters.E.typ + 2 * parameters.b.get_available_max() - parameters.L.get_available_max()
    overlay_d = parameters.D.get_available_max()
    overlay_e = parameters.E.get_available_max() - parameters.L.get_available_max() - Decimal('0.5')
    parameters = Parameters(20,
                            pin_pitch=parameters.e.get_available_max(),
                            pad_width=parameters.L.get_available_max(),
                            pad_height=parameters.b.get_available_max() + Decimal('0.06'),
                            pad_row_spacing=parameters.L.get_available_max() + 2*parameters.b.get_available_max()-parameters.L.get_available_max())

    pin_count_per_side = int(parameters.pin_count / 2)
    first_pad_y = pin_count_per_side * parameters.pin_pitch / 2
    left_pads = add_vertical_pads(first=1,
                                  last=10,
                                  pitch=parameters.pin_pitch,
                                  width=parameters.pad_width,
                                  height=parameters.pad_height,
                                  x=row_spacing / -2,
                                  y_offset=first_pad_y)
    right_pads = add_vertical_pads(first=20,
                                   last=11,
                                   pitch=parameters.pin_pitch,
                                   width=parameters.pad_width,
                                   height=parameters.pad_height,
                                   x=row_spacing / 2,
                                   y_offset=first_pad_y)

    footprint = Footprint(name)
    footprint.add_pad(left_pads)
    footprint.add_pad(right_pads)

    # add overlay layer
    overlay_rectangle = Lines(overlay_e / -2, overlay_d / 2)
    overlay_rectangle.add_point(overlay_e / -2, overlay_d / -2)
    overlay_rectangle.add_point(overlay_e / 2, overlay_d / -2)
    overlay_rectangle.add_point(overlay_e / 2, overlay_d / 2)
    footprint.add_overlay(overlay_rectangle)
    radius = Decimal('0.5')
    spacing = Decimal('0.5')
    overlay_one_position_mark = Circle(overlay_e / -2 + radius + spacing, overlay_d / 2 - radius - spacing, radius)
    footprint.add_overlay(overlay_one_position_mark)

    footprint.width = row_spacing + 3
    footprint.height = overlay_d + 2
    return footprint


def add_vertical_pads(first, last, pitch: Decimal, width: Decimal, height: Decimal, x, y_offset: Decimal):
    pads = []
    count = abs(last - first)
    for i in range(count + 1):
        pads.append(Pad(number=first + i if first < last else first - i,
                        x=x,
                        y=y_offset - Decimal(i) * pitch,
                        width=width,
                        height=height
                        ))
    return pads
