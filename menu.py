# -*- coding: utf-8 -*-
import json
import pyperclip
import re
import urwid

from API import CodecookApi
from menu import *


api = CodecookApi()

class Menu(urwid.WidgetWrap):

    def __init__(self, title, title_obj_list):
        widget = self.load(title, title_obj_list)
        urwid.WidgetWrap.__init__(self, widget)

    def load(self, title, dict):
        """
        Build ListBox with title and buttons from dictionary.
            return Widget
        """
        body = [urwid.Text(title), urwid.Divider()]
        for key, value in dict.iteritems():
            button = urwid.Button(key)
            urwid.connect_signal(button, 'click', self.item_chosen, value)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        list_box = urwid.ListBox(body)
        adapter = urwid.BoxAdapter(list_box, 100)
        return adapter


class ConceptMenu(Menu):

    def __init__(self, objects):
        title = "Tasks"
        if len(objects)>0:
            title_obj_list = {obj.get('name'):obj for obj in objects}
            Menu.__init__(self, title, title_obj_list)
        else:
            #Show no results
            body = [urwid.Text(title + " - no results"), urwid.Divider()]

            button = urwid.Button("Go back.")
            urwid.connect_signal(button, 'click', self.go_back)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

            list_box = urwid.ListBox(body)
            adapter = urwid.BoxAdapter(list_box, 100)
            urwid.WidgetWrap.__init__(self, adapter)

    def go_back(self, button):
        self.navigator.close_menu()

    def item_chosen(self, button, choice):
        concept_id = choice.get('id')
        concept_detail = api.get_concept_detail(concept_id)
        method_list = concept_detail.get('methods')

        # list of method_uri's to list of method_id's
        matcher = re.compile('/(\d+)/')
        method_ids = []
        for uri in method_list:
            result = matcher.search(uri)
            if result:
                method_ids.append(result.group(1))
        # get methods detail from list of ids
        method_details = api.get_methods_detail(method_ids)
        self.object_list = method_details.get('objects')
        self.list = []
        for obj in self.object_list:
            item = obj.get('main_language')
            title = obj.get('title')
            if title:
                item += "- " + title
            self.list.append(item)

        menuObj = MethodMenu(self.object_list)
        self.navigator.open_menu(menuObj)


class MethodMenu(Menu):

    def __init__(self, objects):
        title_obj_list = {}
        for obj in objects:
            item = obj.get('main_language')
            btn_text = item
            title = obj.get('title')
            if title:
                btn_text += " - " + title
            title_obj_list[btn_text] = obj

        Menu.__init__(self, "Methods", title_obj_list)

    def item_chosen(self, button, choice):
        methodUri = choice.get('resource_uri')
        method = api.get_path_data(methodUri)
        snippets = method.get('snippets', None)
        menuObj = SnippetMenu(snippets)
        self.navigator.open_menu(menuObj)


class SnippetMenu(Menu):

    def __init__(self, objects):
        title_obj_list = {obj.get('content')[:20]:obj for obj in objects}
        Menu.__init__(self, "Snippets", title_obj_list)

    def item_chosen(self, button, choice):
        # global copy_success
        content = choice.get('content')
        pyperclip.copy(content)
        # copy_success = True
        raise urwid.ExitMainLoop()


class SearchQuestion(urwid.WidgetWrap):
    def __init__(self, title):
        self.edit_widget = urwid.Edit(title)
        urwid.WidgetWrap.__init__(self, self.edit_widget)

    def keypress(self, size, key):
        if key != 'enter':
            return super(SearchQuestion, self).keypress(size, key)
        query = self.edit_widget.edit_text

        results = api.search_concept(query)
        objects = results.get('objects', None)

        menuObj = ConceptMenu(objects)
        self.navigator.open_menu(menuObj)


class MenuNavigator(urwid.Filler):
    """
    Nested menu widget. Opens and closes widgets in a nested manner.
    """
    menu_level = 0
    menu_stack = []

    def __init__(self, widget, *args, **kwargs):
        super(MenuNavigator, self).__init__(widget, valign='top', *args, **kwargs)
        self.open_menu(widget)

    def open_menu(self, widget):
        widget.navigator = self # set property so widget can call navigator.new menu
        self.menu_stack.append(widget) # Remember widget
        self.original_widget = widget # Show new widget
        self.menu_level += 1 # Menu level is one deeper

    def close_menu(self):
        """Close current menu and load previous"""
        self.menu_stack.pop()
        self.menu_level -= 1
        self.original_widget = self.menu_stack[-1]

    def keypress(self, size, key):
        if key == 'esc' and self.menu_level > 1:
            self.close_menu()
        else:
            return super(MenuNavigator, self).keypress(size, key)