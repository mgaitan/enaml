#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import TraitError

from .enaml_test_case import required_method
from .window import TestWindow


class TestDialog(TestWindow):
    """ Logic for testing Dialogs.

    """

    def setUp(self):
        """ Set up Dialog tests.

        """

        enaml_source = """
defn MainWindow():
    Dialog -> dialog:
        title = 'foo'
"""

        self.view = self.parse_and_create(enaml_source)
        self.component = self.component_by_name(self.view, 'dialog')
        self.widget = self.component.toolkit_widget
        # Don't actually show the dialog.
        self.widget.show = lambda: None
        # (trait_name, value) log of all trait change events on the Dialog.
        self.event_log = []
        self.component.on_trait_change(self._append_event_handler, 'anytrait')

    def test_initial_active(self):
        """ Test the initial value of the active flag on the Dialog.

        """
        self.assertEquals(self.component.active, False)

    def test_result_value(self):
        """ Test the modification of the result value.

        """
        self.assertEquals(self.component.result, 'rejected')
        self.component.accept()
        self.assertEquals(self.component.result, 'accepted')
        self.component.reject()
        self.assertEquals(self.component.result, 'rejected')

    def test_show_close(self):
        """ Test the behavior when showing and closing the dialog.

        """
        self.component.open()
        # Compare sets because the order is unimportant.
        self.assertEquals(set(self.event_log), set([
            ('active', True),
            ('_active', True),
            ('opened', True),
        ]))
        self.event_log = []
        self.component.accept()
        self.assertEquals(set(self.event_log), set([
            ('active', False),
            ('_active', False),
            ('result', 'accepted'),
            ('_result', 'accepted'),
            ('closed', 'accepted'),
        ]))
        self.event_log = []
        self.component.open()
        self.assertEquals(set(self.event_log), set([
            ('active', True),
            ('_active', True),
            ('opened', True),
        ]))
        self.event_log = []
        self.component.reject()
        self.assertEquals(set(self.event_log), set([
            ('active', False),
            ('_active', False),
            ('result', 'rejected'),
            ('_result', 'rejected'),
            ('closed', 'rejected')
        ]))

    @required_method
    def get_result(self, widget):
        """ Get the result value from the widget.

        """
        pass

    def _append_event_handler(self, object, name, old, new):
        """ Append the trait change notification to the event log.

        """
        self.event_log.append((name, new))