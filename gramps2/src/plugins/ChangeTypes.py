#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000-2004  Donald N. Allingham
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

# $Id$

"Database Processing/Rename personal event types"

import os

import gtk
import gtk.glade

import const
import Utils
from gettext import gettext as _
from QuestionDialog import OkDialog
import AutoComp

#-------------------------------------------------------------------------
#
#
#
#-------------------------------------------------------------------------
def runTool(database,person,callback,parent=None):
    try:
        trans = database.start_transaction()
        ChangeTypes(database,person,parent,trans)
        database.add_transaction(trans,_('Change types'))
    except:
        database.add_transaction(trans,_('Change types'))
        database.undo()

        import DisplayTrace
        DisplayTrace.DisplayTrace()

#-------------------------------------------------------------------------
#
#
#
#-------------------------------------------------------------------------
class ChangeTypes:
    def __init__(self,db,person,parent,trans):
        self.person = person
        self.db = db
        self.trans = trans

        base = os.path.dirname(__file__)
        glade_file = "%s/%s" % (base,"changetype.glade")
        self.glade = gtk.glade.XML(glade_file,"top","gramps")

        self.auto1 = AutoComp.AutoCombo(self.glade.get_widget("original"),
                                        const.personalEvents)
        self.auto2 = AutoComp.AutoCombo(self.glade.get_widget("new"),
                                        const.personalEvents)

        Utils.set_titles(self.glade.get_widget('top'),
                         self.glade.get_widget('title'),
                         _('Change event types'))

        self.glade.signal_autoconnect({
            "on_close_clicked"     : Utils.destroy_passed_object,
            "on_apply_clicked"     : self.on_apply_clicked
            })
    
    def on_apply_clicked(self,obj):
        modified = 0
        original = unicode(self.glade.get_widget("original_text").get_text())
        new = unicode(self.glade.get_widget("new_text").get_text())

        for person_id in self.db.get_person_keys():
            person = self.db.try_to_find_person_from_id(person_id)
            for event_id in person.get_event_list():
                if not event_id:
                    continue
                event = self.db.find_event_from_id(event_id)
                if event.get_name() == original:
                    event.set_name(new)
                    modified = modified + 1
                    self.db.commit_event(event,self.trans)

        if modified == 1:
            msg = _("1 event record was modified")
        else:
            msg = _("%d event records were modified") % modified
            
        OkDialog(_('Change types'),msg)
        Utils.destroy_passed_object(obj)

#------------------------------------------------------------------------
#
# 
#
#------------------------------------------------------------------------
from Plugins import register_tool

register_tool(
    runTool,
    _("Rename personal event types"),
    category=_("Database Processing"),
    description=_("Allows all the events of a certain name to be renamed to a new name")
    )
