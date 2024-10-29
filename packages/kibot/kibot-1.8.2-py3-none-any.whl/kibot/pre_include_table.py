# -*- coding: utf-8 -*-
# Copyright (c) 2024 Nguyen Vincent
# Copyright (c) 2024 Salvador E. Tropea
# Copyright (c) 2024 Instituto Nacional de Tecnología Industrial
# License: AGPL-3.0
# Project: KiBot (formerly KiPlot)
# Contributed by Nguyen Vincent (@nguyen-v)
import os
import csv
from .error import KiPlotConfigurationError
from .gs import GS
from .kicad.pcb_draw_helpers import (draw_rect, draw_line, draw_text, get_text_width,
                                     GR_TEXT_HJUSTIFY_LEFT, GR_TEXT_HJUSTIFY_RIGHT,
                                     GR_TEXT_HJUSTIFY_CENTER)
from .kiplot import load_board, get_output_targets, look_for_output
from .misc import W_NOMATCHGRP
from .optionable import Optionable
from .registrable import RegOutput
from .macros import macros, document, pre_class  # noqa: F401
from . import log
logger = log.get_logger()
ALIGNMENT = {'left': GR_TEXT_HJUSTIFY_LEFT,
             'center': GR_TEXT_HJUSTIFY_CENTER,
             'right': GR_TEXT_HJUSTIFY_RIGHT}
VALID_OUTPUT_TYPES = {'bom', 'kibom', 'position'}


class IncTableOutputOptions(Optionable):
    """ Data for a layer """
    def __init__(self, name=None, parent=None):
        super().__init__()
        self._unknown_is_error = True
        with document:
            self.name = ''
            """ *Name of output """
            self.has_header = True
            """ Plot header on the table """
            self.bold_headers = True
            """ Whether or not the headers should be in bold """
            self.vertical_rule_width = 0.1
            """ Width of vertical rules between columns. Use 0 to eliminate it """
            self.horizontal_rule_width = 0.1
            """ Width of vertical rules between rows (doesn't include header)
                Use 0 to eliminate it """
            self.top_rule_width = 0.4
            """ Width of top rule (above header). Use 0 to eliminate it """
            self.bottom_rule_width = 0.4
            """ Width of bottom rule (bottom of table). Use 0 to eliminate it """
            self.header_rule_width = 0.3
            """ Width of rule below header. Use 0 to eliminate it """
            self.border_width = 0.4
            """ Width of border around the table. Use 0 to eliminate it """
            self.column_spacing = 2
            """ Blank space (in number of characters) between columns """
            self.row_spacing = 2
            """ Space (in number of characters) between rows """
            self.text_alignment = 'left'
            """ [left,center,right] Text alignment in the table """
            self.invert_columns_order = False
            """ Invert column order. Useful when inverting PCB texts in PCB Print """
        if name is not None:
            self.name = name
            self.config(parent)

    def __str__(self):
        v = f'{self.name} ({self.text_alignment}'
        if self.invert_columns_order:
            v += ' inverted'
        if self.has_header:
            v += ' header'
        return v+')'

    def config(self, parent):
        super().config(parent)
        self._text_alignment = ALIGNMENT[self.text_alignment]


class IncludeTableOptions(Optionable):
    """ Include table options """
    def __init__(self):
        with document:
            self.outputs = IncTableOutputOptions
            """ *[list(dict)|list(string)|string=?] List of CSV-generating outputs.
                When empty we include all possible outputs """
            self.enabled = True
            """ Enable the check. This is the replacement for the boolean value """
            self.group_name = 'kibot_table'
            """ Name for the group containing the table. The name of the group
                should be <group_name>_X where X is the output name.
                When the output generates more than one CSV use *kibot_table_out[2]*
                to select the second CSV """
        super().__init__()
        self._unknown_is_error = True

    def config(self, parent):
        super().config(parent)
        if isinstance(self.outputs, type):
            # Nothing specified, look for candidates
            self.outputs = [o.name for o in filter(lambda x: x.type in VALID_OUTPUT_TYPES, RegOutput.get_outputs())]
            logger.debug('- Collected outputs: '+str(self.outputs))
        self._outputs = [IncTableOutputOptions(o, self) if isinstance(o, str) else o for o in self.outputs]


class ITColumns:
    def __init__(self, header='', width=10):
        self.header = header  # Column header name
        self.width = width  # Relative width (default to 10)
        self.data = []  # List to hold data for the column


def update_table_group(g, pos_x, pos_y, width, tlayer, ops, out, csv_file):
    if not os.path.isfile(csv_file):
        raise KiPlotConfigurationError(f'Missing `{csv_file}`, create it first using the `{out.name}` output')
    # Purge all content
    for item in g.GetItems():
        GS.board.Delete(item)
    cols = []

    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=out._obj.get_csv_separator())

        if out.has_header:
            headers = next(reader)
            for header in headers:
                cols.append(ITColumns(header=header))
        else:
            first_row = next(reader)
            for _ in range(len(first_row)):
                cols.append(ITColumns())

            # Add the first row data to the cols
            for i, value in enumerate(first_row):
                cols[i].data.append(value)

        # Add the rest of the CSV rows to the column data
        for row in reader:
            for i, value in enumerate(row):
                if i < len(cols):
                    cols[i].data.append(value)

    if out.invert_columns_order:
        cols.reverse()

    measure_table(cols, out)

    total_char_w = sum(c.width_char for c in cols)
    total_rel_w = sum((c.width for c in cols))  # should be equal to 1

    font_w = int(width/total_char_w) if total_char_w else 0

    xpos_x = int(pos_x + out.column_spacing*font_w/2)
    max_row_data = 0
    for c in cols:
        c.w = int(c.width/total_rel_w*width)
        c.x = xpos_x
        if out._text_alignment == GR_TEXT_HJUSTIFY_LEFT:
            c.xoffset = 0
        if out._text_alignment == GR_TEXT_HJUSTIFY_RIGHT:
            c.xoffset = int(c.w - out.column_spacing*font_w)
        elif out._text_alignment == GR_TEXT_HJUSTIFY_CENTER:
            c.xoffset = int(c.w/2 - out.column_spacing*font_w/2)
        xpos_x += c.w
        max_row_data = max(max_row_data, len(c.data))
    y = pos_y

    row_h = out.row_spacing*font_w

    if out.has_header:
        y += int(row_h)  # Space for top rule + column titles + header rule
        draw_line(g, pos_x, y, pos_x + width, y, tlayer, line_w=GS.from_mm(out.header_rule_width))
        # Draw headers
        for c in cols:
            draw_text(g, c.x + c.xoffset, int(pos_y + 0.5*row_h - font_w), c.header, font_w, font_w,
                      tlayer, bold=out.bold_headers, alignment=out._text_alignment)

    # Draw horizontal rules
    for i in range(max_row_data-1):
        rule_y = int(y + (i+1)*row_h)
        draw_line(g, pos_x, rule_y, pos_x+width, rule_y, tlayer, line_w=GS.from_mm(out.horizontal_rule_width))

    table_h = 0
    for c in cols:
        row_y = int(y + row_h/2)
        for d in c.data:
            draw_text(g, c.x + c.xoffset, int(row_y - font_w), d, font_w, font_w, tlayer, alignment=out._text_alignment)
            row_y += row_h
        table_h = int(max(table_h, row_y-pos_y) - row_h/2)

    # Draw top and bottom rules
    draw_line(g, pos_x, pos_y, pos_x + width, pos_y, tlayer, line_w=GS.from_mm(out.top_rule_width))
    draw_line(g, pos_x, pos_y + table_h, pos_x + width, pos_y + table_h, tlayer, line_w=GS.from_mm(out.bottom_rule_width))

    for n, c in enumerate(cols):
        if n > 0:
            vrule_x = int(c.x - out.column_spacing*font_w/2)
            draw_line(g, vrule_x, pos_y, vrule_x, pos_y + table_h, tlayer, line_w=GS.from_mm(out.vertical_rule_width))

    # Draw rectangle around table
    draw_rect(g, pos_x, pos_y, width, table_h, tlayer, line_w=GS.from_mm(out.border_width))


def measure_table(cols, out):
    col_spacing_width = get_text_width('o')*out.column_spacing

    for c in cols:
        max_data_len = max(get_text_width(d) for d in c.data) if c.data else 0
        max_data_width_char = max(len(d) for d in c.data) if c.data else 0
        c.max_len = max(get_text_width(c.header), max_data_len) + col_spacing_width
        c.width_char = max(len(c.header), max_data_width_char) + out.column_spacing

    tot_len = sum(c.max_len for c in cols)

    # Compute relative widths
    for c in cols:
        c.width = c.max_len/tot_len


def update_table(ops, parent):
    logger.debug('Starting include table preflight')
    load_board()
    csv_files = []
    csv_name = []
    out_to_csv_mapping = {}  # Create a mapping of out variable to its corresponding CSV files

    logger.debug('- Analyzing requested outputs')
    for out in ops._outputs:
        if not out.name:
            raise KiPlotConfigurationError('output entry without a name')
        csv = look_for_output(out.name, '`include table`', parent, VALID_OUTPUT_TYPES) if out.name else None
        if not csv:
            logger.debug(f'  - {out.name} no CSV')
            continue
        out._obj = csv
        targets, _, _ = get_output_targets(out.name, parent)

        # Filter targets to include only CSV files
        csv_targets = [file for file in targets if file.endswith('.csv')]

        for file in csv_targets:
            csv_files.append(file)

        # Append the CSV file names (without path and extension) to csv_name
        for file in csv_targets:
            file_name = os.path.basename(file)  # Get the file name
            name_without_ext = os.path.splitext(file_name)[0]  # Remove the extension
            csv_name.append(name_without_ext)

        # Map the CSV file names to the corresponding out variable
        out_to_csv_mapping[out.name] = (out, csv_targets)
        logger.debug(f'  - {out.name} -> {csv_targets}')

    group_found = False  # Flag to track if any group was found with ops.group_name
    updated = False
    group_prefix = ops.group_name + "_"
    group_prefix_l = len(group_prefix)
    logger.debug('- Scanning board groups')
    for g in GS.board.Groups():
        group_name = g.GetName()
        if not group_name.startswith(group_prefix):
            continue
        group_found = True  # A group with ops.group_name was found
        logger.debug('  - '+group_name)

        # Extract the part after <group_name>_
        group_suffix = group_name[group_prefix_l:]
        index = 0
        if group_suffix[-1] == ']':
            index = int(group_suffix[-2])-1
            group_suffix = group_suffix[:-3]
            logger.debug(f'    - {group_suffix} index: {index}')
        out, csv = out_to_csv_mapping.get(group_suffix)
        if not csv:
            logger.warning(W_NOMATCHGRP+f'No output to handle `{group_name}` found')
            continue
        if index < 0 or index >= len(csv):
            msg = f'index {index+1} is out of range, '+('only one CSV available' if len(csv) == 1 else
                                                        f'must be in the [1,{len(csv)}] range')
            raise KiPlotConfigurationError(msg)
        # We know about it
        x1, y1, x2, y2 = GS.compute_group_boundary(g)
        item = g.GetItems()[0]
        layer = item.GetLayer()
        logger.debug(f'    - Found group @{GS.to_mm(x1)},{GS.to_mm(y1)} mm'
                     f' ({GS.to_mm(x2-x1)}x{GS.to_mm(y2-y1)} mm) layer {layer}'
                     f' with name {g.GetName()}')
        update_table_group(g, x1, y1, x2 - x1, layer, ops, out, csv[index])
        updated = True

    if not group_found:
        logger.warning(W_NOMATCHGRP+f'No `{ops.group_name}*` groups found, skipping `include_table` preflight')

    return updated


@pre_class
class Include_Table(BasePreFlight):  # noqa: F821
    """ Include Table
        Draws a table in the PCB from data in a CSV generated by an output. Needs KiCad 7 or newer.
        To specify the position and size of the drawing you should draw a rectangle in your PCB
        with the width and layer you want. |br|
        Then draw another thing inside the rectangle, select both and create a group
        (right mouse button, then Grouping -> Group). Now edit the group and change its name
        to *kibot_table_X* where X should match the name of the output. Consult the
        `group_name` option for details. |br|
        After running this preflight the rectangle will contain the table with the same name.
        Only the width of the table is important, the height will be adjusted.
        Important: This preflight assumes that a separated KiBot run generated the outputs
        needed for the tables """

    def __init__(self):
        super().__init__()
        self._pcb_related = True
        with document:
            self.include_table = IncludeTableOptions
            """ [boolean|dict=false] Use a boolean for simple cases or fine-tune its behavior """

    def __str__(self):
        v = self.include_table
        if isinstance(v, bool):
            return super().__str__()
        return f'{self.type}: {v.enabled} ({[out.name for out in v._outputs]})'

    def config(self, parent):
        super().config(parent)
        if isinstance(self.include_table, bool):
            self._value = IncludeTableOptions()
            self._value.config(self)
        else:
            self._value = self.include_table

    def apply(self):
        if not GS.ki7:
            raise KiPlotConfigurationError('The `include_table` preflight needs KiCad 7 or newer')
        if update_table(self._value, self):
            GS.save_pcb()
