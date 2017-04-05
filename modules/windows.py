#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for moving and controlling **windows**
=====================================================

This command-module offers commands for naming windows, bringing
named windows to the foreground, and positioning and resizing
windows.

Commands
--------

The following voice commands are available:

Command: **"name window <dictation>"**
    Assigns the given name to the current foreground window.

Command: **"focus <window name>"** or **"bring <window name> to the foreground"**
    Brings the named window to the foreground.

Command: **"focus title <window title>"**
    Brings a window with the given word(s) in the title to the foreground.

Command: **"place <window> <position> [on <monitor>]"**
    Relocates the target window to the given position.

Command: **"stretch <window> <position>"**
    Stretches the target window to the given position.

Usage examples
--------------

 - Say **"place window left"** to relocate the foreground window
   to the left side of the monitor it's on.
 - Say **"place Firefox top right on monitor 2"** to relocate
   the window which was previously named "Firefox" to the top right
   corner of the second display monitor.

"""


import time
import os
from modules.util.json_parser import parse_file
import win32api, win32con, win32gui
from dragonfly import (Grammar, Alternative, RuleRef, DictListRef,
                       Dictation, Compound, Rule, CompoundRule,
                       Choice, Window, Rectangle, monitors,
                       Config, Section, Item, FocusWindow, ActionError)


window_names = {}
monitor_names = {}


default_monitors_file = """{
    "monitor_names": {
        "main": 0
    }
}
"""


def load_config(config_path):
    monitors_file = os.path.join(config_path, "monitors.json")
    for key, value in parse_file(monitors_file, default_monitors_file)["monitor_names"].iteritems():
        monitor_names[key] = monitors[value]

    for i, m in enumerate(monitors):
        monitor_names[str(i + 1)] = m


def create_grammar():
    class WinSelectorRule(CompoundRule):

        spec = "window | win | window <window_name>"
        extras = [Choice("window_name", window_names)]
        exported = False

        def value(self, node):
            if node.has_child_with_name("window_name"):
                return node.get_child_by_name("window_name").value()
            return Window.get_foreground()

    win_selector = RuleRef(WinSelectorRule(), name="win_selector")

    class MonSelectorRule(CompoundRule):

        spec = "(this | current) monitor | [monitor] <monitor_name>"
        extras = [Choice("monitor_name", monitor_names)]
        exported = False

        def value(self, node):
            if node.has_child_with_name("monitor_name"):
                return node.get_child_by_name("monitor_name").value()
            return None

    mon_selector = RuleRef(MonSelectorRule(), name="mon_selector")

    class NameWinRule(CompoundRule):

        spec = "name (window | win) <name>"
        extras = [Dictation("name")]

        def _process_recognition(self, node, extras):
            name = str(extras["name"])
            window = Window.get_foreground()
            window.name = name
            window_names[name] = window
            self._log.debug("%s: named foreground window '%s'." % (self, window))

    class FocusWinRule(CompoundRule):

        spec = "focus <win_selector> | bring <win_selector> to [the] (top | foreground)"
        extras = [win_selector]

        def _process_recognition(self, node, extras):
            window = extras["win_selector"]
            if not window:
                self._log.warning("No window with that name found.")
                return
            self._log.debug("%s: bringing window '%s' to the foreground."
                            % (self, window))
            for attempt in range(4):
                try:
                    window.set_foreground()
                except Exception, e:
                    self._log.warning("%s: set_foreground() failed: %s."
                                      % (self, e))
                    time.sleep(0.2)
                else:
                    break

    class FocusTitleRule(CompoundRule):

        spec = "focus title <text>"
        extras = [Dictation("text")]

        def _process_recognition(self, node, extras):
            title = str(extras["text"])
            action = FocusWindow(title=title)
            try:
                action.execute()
            except ActionError:
                self._log.warning("No window with that name found.")

    horz_left = Compound("left", name="horz", value=0.0)
    horz_center = Compound("center", name="horz", value=0.5)
    horz_right = Compound("right", name="horz", value=1.0)
    vert_top = Compound("top", name="vert", value=0.0)
    vert_center = Compound("center", name="vert", value=0.5)
    vert_bottom = Compound("bottom", name="vert", value=1.0)

    horz_all = Alternative([horz_left, horz_center, horz_right], name="horz_all")
    vert_all = Alternative([vert_top, vert_center, vert_bottom], name="vert_all")

    position_element = Compound(
        spec="   <horz_all>"
             " | <vert_all>"
             " | <vert_all> <horz_all>",
        extras=[horz_all, vert_all],
    )
    position_rule = Rule(
        name="position_rule",
        element=position_element,
        exported=False,
    )
    position = RuleRef(position_rule, name="position")

    class CloseRule(CompoundRule):
        spec = "close <win_selector>"
        extras = [
            win_selector
        ]

        def _process_recognition(self, node, extras):
            window = extras["win_selector"]
            win32api.PostMessage(win32gui.FindWindow(0, window.title), win32con.WM_CLOSE, 0, 0)

    class MinimizeRule(CompoundRule):
        spec = "minimize <win_selector>"
        extras = [
            win_selector
        ]

        def _process_recognition(self, node, extras):
            window = extras["win_selector"]
            win32gui.ShowWindow(win32gui.FindWindow(0, window.title), win32con.SW_MINIMIZE)

    class FullscreenRule(CompoundRule):
        spec = "place <win_selector> on <mon_selector>"
        extras = [
            win_selector,
            mon_selector
        ]

        def _process_recognition(self, node, extras):
            window = extras["win_selector"]
            window.set_position(extras["mon_selector"].rectangle)

    class TranslateRule(CompoundRule):

        spec = "place <win_selector> <position> [on <mon_selector>]"
        extras = [
            win_selector,
            mon_selector,
            position
        ]

        def _process_recognition(self, node, extras):
            # Determine which window to place on which monitor.
            window = extras["win_selector"]
            if "mon_selector" in extras:
                monitor = extras["mon_selector"].rectangle
            else:
                monitor = window.get_containing_monitor().rectangle

            # Calculate available area within monitor.
            pos = window.get_position()

            monitor_move_x = monitor.x1 - window.get_containing_monitor().rectangle.x1
            monitor_move_y = monitor.y1 - window.get_containing_monitor().rectangle.y1
            m_x1 = monitor.x1 + pos.dx / 2
            m_dx = monitor.dx - pos.dx
            m_y1 = monitor.y1 + pos.dy / 2
            m_dy = monitor.dy - pos.dy

            # Get spoken position and calculate how far to move.
            horizontal = node.get_child_by_name("horz")
            vertical = node.get_child_by_name("vert")
            if horizontal:
                dx = m_x1 + horizontal.value() * m_dx - pos.center.x
            else:
                dx = 0
            if vertical:
                dy = m_y1 + vertical.value() * m_dy - pos.center.y
            else:
                dy = 0

            # Translate and move window.
            pos.translate(dx + monitor_move_x, dy + monitor_move_y)
            window.set_position(pos)

    class ResizeRule(CompoundRule):

        spec = "place <win_selector> [from] <position> [to] <position> [on <mon_selector>]"
        extras = [
            win_selector,
            mon_selector,
            position
        ]

        def _process_recognition(self, node, extras):
            # Determine which window to place on which monitor.
            window = extras["win_selector"]
            pos = window.get_position()
            if "mon_selector" in extras:
                monitor = extras["mon_selector"].rectangle
            else:
                monitor = window.get_containing_monitor().rectangle

            # Determine horizontal positioning.
            nodes = node.get_children_by_name("horz")
            horizontals = [(monitor.x1 + n.value() * monitor.dx) for n in nodes]
            if len(horizontals) == 1:
                horizontals.extend([pos.x1, pos.x2])
            elif len(horizontals) != 2:
                self._log.error("%s: Internal error." % self)
                return
            x1, x2 = min(horizontals), max(horizontals)

            # Determine vertical positioning.
            nodes = node.get_children_by_name("vert")
            verticals = [(monitor.y1 + n.value() * monitor.dy) for n in nodes]
            if len(verticals) == 1:
                verticals.extend([pos.y1, pos.y2])
            elif len(verticals) != 2:
                self._log.error("%s: Internal error." % self)
                return
            y1, y2 = min(verticals), max(verticals)

            # Move window.
            pos = Rectangle(x1, y1, x2 - x1, y2 - y1)
            window.set_position(pos)

    class StretchRule(CompoundRule):

        spec = "stretch <win_selector> [to] <position>"
        extras = [
            win_selector,
            position
        ]

        def _process_recognition(self, node, extras):
            # Determine which window to place.
            window = extras["win_selector"]
            pos = window.get_position()
            monitor = window.get_containing_monitor().rectangle

            # Determine horizontal positioning.
            horizontals = [pos.x1, pos.x2]
            child = node.get_child_by_name("horz")
            if child: horizontals.append(monitor.x1 + child.value() * monitor.dx)
            x1, x2 = min(horizontals), max(horizontals)

            # Determine vertical positioning.
            verticals = [pos.y1, pos.y2]
            child = node.get_child_by_name("vert")
            if child: verticals.append(monitor.y1 + child.value() * monitor.dy)
            y1, y2 = min(verticals), max(verticals)

            # Move window.
            pos = Rectangle(x1, y1, x2 - x1, y2 - y1)
            window.set_position(pos)

    grammar = Grammar("window")
    grammar.add_rule(NameWinRule())
    grammar.add_rule(FocusWinRule())
    grammar.add_rule(FocusTitleRule())
    grammar.add_rule(CloseRule())
    grammar.add_rule(MinimizeRule())
    grammar.add_rule(FullscreenRule())
    grammar.add_rule(TranslateRule())
    grammar.add_rule(ResizeRule())
    grammar.add_rule(StretchRule())
    return grammar, True
