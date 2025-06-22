#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
import re
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *


#*****************************************************
# VistaExplorer
#*****************************************************
class VistaExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        lfCmd("let executes = []")
        lfCmd("let [datas, cur_executive, using_alternative] = call('vista#finder#GetSymbols', executes)")
        # lfCmd("echomsg datas")
        data = lfEval("datas")
        buffer = vim.current.buffer
        lst = []
        for key, value in data.items():
            for tag in value:
                s = "{}:{}:\t{}".format(key, tag['lnum'], tag['text'])
                lst.append(s)
        return lst

    def getStlCategory(self):
        return "Vista"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def isFilePath(self):
        return False
    
#*****************************************************
# VistaExplManager
#*****************************************************
class VistaExplManager(Manager):
    def __init__(self):
        super(VistaExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return VistaExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Vista#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        match = re.match(r'^.+?:(\d+):\t.+$', line)
        if match:
        # 提取行号并转换为整数
            line_nr = int(match.group(1))
            lfCmd('buffer +%s %s' % (line_nr, vim.current.buffer.number))
            lfCmd('normal! ^')
            lfCmd('normal! zz')
            lfCmd('setlocal cursorline! | redraw | sleep 100m | setlocal cursorline!')
        else:
            return

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        if not line:
            return ''
        return line.rsplit("\t", 1)[1]

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, return the start position of the whole line
                  1, return the start position of code
                  2, return the start position remaining part
        """
        return lfBytesLen(line.rsplit("\t", 1)[0]) + lfBytesLen("\t")

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" x : open file under cursor in a horizontally split window')
        help.append('" v : open file under cursor in a vertically split window')
        help.append('" t : open file under cursor in a new tabpage')
        help.append('" i : switch to input mode')
        help.append('" p : preview the result')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _afterEnter(self):
        super(VistaExplManager, self)._afterEnter()
        if self._getInstance().getWinPos() == 'popup':
            lfCmd(r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_vistaKind'', ''^\w\+:'')')"""
                    % self._getInstance().getPopupWinId())
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
            lfCmd(r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_vistaLineNum'', '':\zs\d\+:'')')"""
                    % self._getInstance().getPopupWinId())
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
            # lfCmd(r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_vistaText'', ''\t\zs.*$'')')"""
            #         % self._getInstance().getPopupWinId())
            # id = int(lfEval("matchid"))
            # self._match_ids.append(id)
        else:
            id = int(lfEval(r'''matchadd('Lf_hl_vistaKind', '^\w\+:')'''))
            self._match_ids.append(id)
            id = int(lfEval(r'''matchadd('Lf_hl_vistaLineNum', ':\zs\d\+:')'''))
            self._match_ids.append(id)
            # id = int(lfEval(r'''matchadd('Lf_hl_marksText', '\t\zs.*$')'''))
            # self._match_ids.append(id)

    def _beforeExit(self):
        super(VistaExplManager, self)._beforeExit()

    def _previewInPopup(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        line_nr = line.rsplit("\t")[0].split(":")[1]
        self._createPopupPreview("", self._getInstance().getOriginalPos()[2].number, line_nr, jump_cmd='')

#*****************************************************
# VistaExplManager is a singleton
#*****************************************************
vistaExplManager = VistaExplManager()

__all__ = ['vistaExplManager']