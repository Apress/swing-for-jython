#-------------------------------------------------------------------------------
#    Name: List5.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Next iteration of our Jython Swing script showing how items can be
#          added and removed from a list.
#    Note: This script is incomplete.  Functionality remains to be added.
#   Usage: wsadmin -f List5.py
#            or
#          jython List5.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel

from   javax.swing.event import ListSelectionListener

#-------------------------------------------------------------------------------
# Name: List5()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List5( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List5',
            size = ( 200, 220 ),
            layout = GridLayout( 1, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        panel = JPanel( layout = GridLayout( 0, 1 ) )
        panel.add( self.button( 'Remove' ) )
        panel.add( self.button( 'First'  ) )
        panel.add( self.button( 'Last'   ) )
        panel.add( self.button( 'Before' ) )
        panel.add( self.button( 'After'  ) )
        self.text = panel.add( JTextField( 10 ) )
        frame.add( panel )

        data = (
            'Now is the time for all good spam ' +
            'to come to the aid of their eggs'
        ).split( ' ' )
        self.info = JList(
            data,
            valueChanged = self.selection,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
#       self.info = JList( data )
        frame.add(
            JScrollPane(
                self.info,
                preferredSize = ( 200, 100 )
            )
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: button()
    # Role: Create and button with the specified text, with an actionListener
    #---------------------------------------------------------------------------
    def button( self, text ) :
        return JButton( text, actionPerformed = self.insert )

    #---------------------------------------------------------------------------
    # Name: insert()
    # Role: Retrieve the "word" from the input field, and insert it at the
    #       position in the list corresponding to the button that was pressed
    #---------------------------------------------------------------------------
    def insert( self, event ) :
        todo = event.getActionCommand()
        word = self.text.getText()
        print '%s: "%s"' % ( todo, word )

    #---------------------------------------------------------------------------
    # Name: selection()
    # Role: ListSelectionListener event handler
    #---------------------------------------------------------------------------
    def selection( self, e ) :
        index = e.getSource().getSelectedIndex()
        if not e.getValueIsAdjusting() :
            print 'selected %d' % index

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List5() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
