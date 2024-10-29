# -*- coding: utf-8 -*-
# Copyright (c) 2020-2023 Salvador E. Tropea
# Copyright (c) 2020-2023 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
import os
from .error import KiPlotConfigurationError
from .gs import GS
from .out_base import VariantOptions
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger()


class Any_SCH_PrintOptions(VariantOptions):
    def __init__(self):
        with document:
            self.monochrome = False
            """ Generate a monochromatic output """
            self.frame = True
            """ *Include the frame and title block """
            self.all_pages = True
            """ Generate with all hierarchical sheets """
            self.color_theme = ''
            """ Color theme used, this must exist in the KiCad config (KiCad 6) """
            self.background_color = False
            """ Use the background color from the `color_theme` (KiCad 6) """
            self.title = ''
            """ Text used to replace the sheet title. %VALUE expansions are allowed.
                If it starts with `+` the text is concatenated """
            self.sheet_reference_layout = ''
            """ Worksheet file (.kicad_wks) to use. Leave empty to use the one specified in the project.
                This option works only when you print the toplevel sheet of a project and the project
                file is available """
        super().__init__()
        self.add_to_doc('variant', "Not fitted components are crossed")
        self._expand_id = 'schematic'

    def get_targets(self, out_dir):
        if self.output:
            return [self._parent.expand_filename(out_dir, self.output)]
        return [self._parent.expand_filename(out_dir, '%f.%x')]

    def run(self, name):
        super().run(name)
        command = self.ensure_tool('KiAuto')

        # This code has two purposes:
        # 1. Allow specifying a different worksheet
        # 2. Fix \ in the worksheet
        # For this we temporarily adjust the project
        prj = None
        if GS.pro_file and GS.pro_basename == GS.sch_basename:
            ori_wks = ''
            wks = GS.fix_page_layout(GS.pro_file, dry=True)
            # We have a project and is the project for the schematic
            if self.sheet_reference_layout:
                # The user wants a different worksheet
                new_wks = os.path.join(GS.pro_dir, self.sheet_reference_layout)
                if not os.path.isfile(new_wks):
                    raise KiPlotConfigurationError(f'Missing `{new_wks}` worksheet')
            else:
                ori_wks = new_wks = wks[0]
                if ori_wks and not os.path.isfile(new_wks):
                    # Try replacing backslashes
                    try_wks = new_wks.replace('\\', '/')
                    if not os.path.isfile(try_wks):
                        raise KiPlotConfigurationError(f'Missing `{new_wks}` worksheet')
                    new_wks = try_wks
            if ori_wks != new_wks:
                prj = GS.read_pro()
                GS.fix_page_layout(GS.pro_file, dry=False, force_sch=os.path.relpath(new_wks, GS.pro_dir),
                                   force_pcb=os.path.relpath(wks[1], GS.pro_dir))
        elif self.sheet_reference_layout:
            raise KiPlotConfigurationError('Using `sheet_reference_layout` but no project available')

        try:
            if self.title:
                self.set_title(self.title, sch=True)
            if self._comps or self.title:
                # Save it to a temporal dir
                sch_dir = GS.mkdtemp(self._expand_ext+'_sch_print')
                GS.copy_project_sch(sch_dir)
                fname = GS.sch.save_variant(sch_dir)
                sch_file = os.path.join(sch_dir, fname)
                self._files_to_remove.append(sch_dir)
            else:
                sch_file = GS.sch_file
            fmt = 'hpgl' if self._expand_ext == 'plt' else self._expand_ext
            cmd = [command, 'export', '--file_format', fmt, '-o', name]
            if self.monochrome:
                cmd.append('--monochrome')
            if not self.frame:
                cmd.append('--no_frame')
            if self.all_pages:
                cmd.append('--all_pages')
            if self.color_theme:
                cmd.extend(['--color_theme', self.color_theme])
            if self.background_color:
                cmd.append('--background_color')
            if hasattr(self, '_origin'):
                cmd.extend(['--hpgl_origin', str(self._origin)])
            if hasattr(self, 'pen_size'):
                cmd.extend(['--hpgl_pen_size', str(self.pen_size)])
            cmd.extend([sch_file, os.path.dirname(name)])
            self.exec_with_retry(self.add_extra_options(cmd), self._exit_error)
            if self.title:
                self.restore_title(sch=True)
        finally:
            if prj:
                GS.write_pro(prj)
