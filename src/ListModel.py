#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from gobject import TYPE_STRING, TYPE_PYOBJECT
import gtk

class ListModel:
    def __init__(self,tree,dlist,select_func=None,event_func=None):
        self.tree = tree
        l = len(dlist)
        mylist = [TYPE_STRING]*l + [TYPE_PYOBJECT]
        self.model = gtk.ListStore(*mylist)

        self.selection = self.tree.get_selection()
        self.tree.set_model(self.model)

        self.data_index = l
        
        cnum = 0
        for name in dlist:
            renderer = gtk.CellRendererText()
            column = gtk.TreeViewColumn(name[0],renderer,text=cnum)
            column.set_min_width(name[2])
            if name[0] == '':
                column.set_clickable(gtk.TRUE)
                column.set_visible(gtk.FALSE)
            else:
                column.set_resizable(gtk.TRUE)
            cnum = cnum + 1
            tree.append_column(column)
            
        num = 0
        for name in dlist:
            column = tree.get_column(num)
            if name[1] != -1:
                column.set_sort_column_id(name[1])
                if num == 0:
                    column.clicked()
                num = num + 1

        if select_func:
            self.selection.connect('changed',select_func)
        if event_func:
            self.double_click = event_func
            self.tree.connect('event',self.button_press)

    def get_selected(self):
        return self.selection.get_selected()

    def clear(self):
        self.model.clear()

    def get_object(self,iter):
        return self.model.get_value(iter,self.data_index)
        
    def add(self,data,info=None):
        iter = self.model.append()
        col = 0
        for object in data:
            self.model.set_value(iter,col,object)
            col = col + 1
        self.model.set_value(iter,col,info)
        
    def button_press(self,obj,event):
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            self.double_click(obj)
            return 1
