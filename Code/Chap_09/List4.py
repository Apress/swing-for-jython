#-------------------------------------------------------------------------------
#    Name: List4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: First iteration of our Jython Swing script showing how items can be
#          added and removed from a list.
#    Note: This script is incomplete.  Functionality remains to be added.
#   Usage: wsadmin -f List4.py
#            or
#          jython List4.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import BorderLayout
from   java.awt    import GridLayout
from   java.awt    import EventQueue
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel

#-------------------------------------------------------------------------------
# Name: List4()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List4( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List4',
            size = ( 200, 222 ),
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        data = (
            'Now is the time for all good spam ' +
            'to come to the aid of their eggs'
        ).split( ' ' )
        self.info = JList(
            data,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
#       self.info = JList( data )
        frame.add(
            JScrollPane(
                self.info,
                preferredSize = ( 200, 100 )
            ),
            BorderLayout.NORTH
        )
        panel = JPanel( layout = GridLayout( 0, 2 ) )
        self.text = panel.add( JTextField( 10 ) )
        panel.add( self.button( 'First'  ) )
        panel.add( self.button( 'Last'   ) )
        panel.add( self.button( 'Before' ) )
        panel.add( self.button( 'After'  ) )
        panel.add( self.button( 'Remove' ) )
        frame.add( panel, BorderLayout.SOUTH )
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

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List4() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
