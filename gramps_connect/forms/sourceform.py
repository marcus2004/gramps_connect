#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (c) 2015 Gramps Development Team
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# Gramps imports:
from gramps.gen.lib.src import Source

# Gramps Connect imports:
from .forms import Form

class SourceForm(Form):
    """
    A form for listing, viewing, and editing a Person object.
    """
    _class = Source
    view = "source"
    tview = "Source"

    # Fields for editor:
    edit_fields = [
        "type",
        "text.string",
        "gramps_id",
        "tag_list",
        "private",
    ]

    # URL for page view rows:
    link = "/source/%(handle)s"

    # Search fields to use if not specified:
    default_search_fields = [
        "text.string",
        "gramps_id",
    ]

    # Search fields, list is OR
    search_terms = {
        "text": "text.string",
        "id": "gramps_id",
    }

    order_by = [("gramps_id", "ASC")]

    # Fields for page view; width sum = 95%:
    select_fields = [
        ("gramps_id", 10),
        ("title", 30),
        ("author", 20),
        ("pubinfo", 10),
        ("abbrev", 10),
        ("change", 10),
        ("private", 5),
    ]

    # Other fields needed to select:
    env_fields = [
        "handle",
    ]

    def set_post_process_functions(self):
        """
        Set the post_process_functions dictionary.
        """
        self.post_process_functions = {
            "text.string": self.preview,
        }

    def preview(self, text, env):
        return text[:100]

    def describe(self):
        """
        Textual description of this instance.
        """
        return str(self.instance.gramps_id)
