#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.04.12 08:00:00                  #
# ================================================== #

from PySide6.QtGui import QAction

from ..utils import trans


class Theme:
    def __init__(self, window=None):
        """
        Theme controller

        :param window: main window object
        """
        self.window = window

    def toggle(self, name):
        """
        Toggles theme

        :param name: theme name
        """
        self.window.config.data['theme'] = name
        self.window.config.save()
        self.apply()
        self.window.set_theme(name + '.xml')
        self.update()

    def apply(self):
        """Applies theme fixes"""
        self.window.setStyleSheet(self.get_style('line_edit'))
        self.window.menu['menu.lang'].setStyleSheet(self.get_style('menu'))
        self.window.menu['menu.theme'].setStyleSheet(self.get_style('theme'))
        self.window.data['output'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['output.timestamp'].setStyleSheet(self.get_style('checkbox'))
        self.window.data['input.send_enter'].setStyleSheet(self.get_style('radio'))
        self.window.data['input.send_shift_enter'].setStyleSheet(self.get_style('radio'))
        self.window.data['input.send_clear'].setStyleSheet(self.get_style('checkbox'))

        # dialog: ctx rename
        self.window.dialog['ctx.rename'].input.setStyleSheet(self.get_style('line_edit'))

        # ai, user names
        self.window.data['preset.ai_name'].setStyleSheet(self.get_style('line_edit'))
        self.window.data['preset.user_name'].setStyleSheet(self.get_style('line_edit'))

        # dialog: settings
        self.window.config_option['use_context'].box.setStyleSheet(self.get_style('checkbox'))
        self.window.config_option['store_history'].box.setStyleSheet(self.get_style('checkbox'))
        self.window.config_option['store_history_time'].box.setStyleSheet(self.get_style('checkbox'))

        # dialog: preset editor
        self.window.config_option['preset.chat'].box.setStyleSheet(self.get_style('checkbox'))
        self.window.config_option['preset.completion'].box.setStyleSheet(self.get_style('checkbox'))
        self.window.config_option['preset.img'].box.setStyleSheet(self.get_style('checkbox'))

    def get_style(self, element):
        """
        Returns style for element

        :param element: element name
        :return: style
        """
        theme = self.window.config.data['theme']

        # initial dark theme colors
        label = "fff"  # dark_teal
        chat_color = "fff"  # dark_teal
        checkbox_checked = "1de9b6"  # dark_teal
        checkbox_unchecked = "3a3f45"  # dark_teal

        # inverse colors for light themes
        if theme.startswith('light_'):
            label = "000"
            chat_color = "000"
            checkbox_unchecked = "f5f5f5"

        # Windows-OS invisible checkboxes fixes
        if theme.endswith('amber'):
            checkbox_checked = "ffd740"
        elif theme.endswith('blue'):
            checkbox_checked = "448aff"
        elif theme.endswith('cyan'):
            checkbox_checked = "4dd0e1"
        elif theme.endswith('lightgreen'):
            checkbox_checked = "8bc34a"
        elif theme.endswith('pink'):
            checkbox_checked = "ff4081"
        elif theme.endswith('purple'):
            checkbox_checked = "ab47bc"
        elif theme.endswith('red'):
            checkbox_checked = "ff1744"
        elif theme.endswith('teal'):
            checkbox_checked = "1de9b6"
        elif theme.endswith('yellow'):
            checkbox_checked = "ffff00"

        # get theme element style
        if element == 'checkbox':
            return "QCheckBox::indicator:checked { background-color: #" + checkbox_checked + "; } QCheckBox::indicator:unchecked { background-color: #" + checkbox_unchecked + "; }"  # Windows fix
        elif element == 'radio':
            return "QRadioButton::indicator:checked { background-color: #" + checkbox_checked + "; } QRadioButton::indicator:unchecked { background-color: #" + checkbox_unchecked + "; }"  # Windows fix
        elif element == 'menu':
            return "QMenu::indicator:checked { background-color: #" + checkbox_checked + "; } QMenu::indicator:unchecked { background-color: #" + checkbox_unchecked + "; }"  # Windows fix
        elif element == "tree_view":
            return "QTreeView { padding: 0px; margin: 0px; }; QTreeView::item { padding: 0px; margin: 0px; }"
        elif element == "chat_output":
            return 'color: #{}; font-size: {}px;'.format(chat_color, self.window.config.data['font_size'])
        elif element == "line_edit":
            return "QLineEdit { color: #" + label + "; }"
        elif element == "text_bold":
            return "font-weight: bold;"

    def update(self):
        """Updates theme menu"""
        for theme in self.window.menu['theme']:
            self.window.menu['theme'][theme].setChecked(False)
        current = self.window.config.data['theme']
        if current in self.window.menu['theme']:
            self.window.menu['theme'][current].setChecked(True)

    def get_themes_list(self):
        """
        Returns list of themes

        :return: list of themes
        """
        return ['dark_amber',
                'dark_blue',
                'dark_cyan',
                'dark_lightgreen',
                'dark_pink',
                'dark_purple',
                'dark_red',
                'dark_teal',
                'dark_yellow',
                'light_amber',
                'light_blue',
                'light_cyan',
                'light_cyan_500',
                'light_lightgreen',
                'light_pink',
                'light_purple',
                'light_red',
                'light_teal',
                'light_yellow']

    def trans_theme(self, theme):
        """
        Translates theme name

        :param theme: theme name
        :return: translated theme name
        """
        return theme.replace('_', ' ').title().replace('Dark ', trans('theme.dark') + ': ').replace('Light ', trans(
            'theme.light') + ': ')

    def setup(self):
        """Setups theme"""
        # setup menu
        themes = self.get_themes_list()
        for theme in themes:
            name = self.trans_theme(theme)
            self.window.menu['theme'][theme] = QAction(name, self.window, checkable=True)
            self.window.menu['theme'][theme].triggered.connect(
                lambda checked=None, theme=theme: self.window.controller.theme.toggle(theme))
            self.window.menu['menu.theme'].addAction(self.window.menu['theme'][theme])

        # apply theme
        theme = self.window.config.data['theme']
        self.toggle(theme)
