#-------------------------------------------------------------------------------
#    Name: List9.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Next iteration of our Jython Swing script showing how items can be
#          added and removed from a list.
#    Note: This script is incomplete.  Functionality remains to be added.
#   Usage: wsadmin -f List9.py
#            or
#          jython List9.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import DefaultListModel
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel

#-------------------------------------------------------------------------------
# Name: List9()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List9( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List9',
            size = ( 200, 220 ),
            layout = GridLayout( 1, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        panel = JPanel( layout = GridLayout( 0, 1 ) )
        self.buttons = {}
        for name in 'First,Last,Before,After,Remove'.split( ',' ) :
            self.buttons[ name ] = panel.add( self.newButton( name ) )

        self.text = panel.add(
            JTextField(
                10,
                keyReleased = self.textCheck
            )
        )

        frame.add( panel )

        data = (
            'Now is the time for all good spam ' +
            'to come to the aid of their eggs'
        ).split( ' ' )
        model = DefaultListModel()
        for word in data :
            model.addElement( word )
        self.info = JList(
            model,
            valueChanged = self.textCheck,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        frame.add(
            JScrollPane(
                self.info,
                preferredSize = ( 200, 100 )
            )
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: newButton()
    # Role: Create a button with the specified text, and with an actionListener
    #       event handler assigned
    #---------------------------------------------------------------------------
    def newButton( self, text ) :
        return JButton(
            text,
            enabled = 0,
            actionPerformed = self.doit
        )

    #---------------------------------------------------------------------------
    # Name: doit()
    # Role: Perform the action identified by the button
    # Note: For insert actios:
    #       - Retrieve the "word" from the input field, and
    #       - insert it at the position in the list corresponding to the button
    #         that was pressed (i.e., First, Last, Before, After)
    #---------------------------------------------------------------------------
    def doit( self, event ) :
        todo  = event.getActionCommand()
        word  = self.text.getText().strip()
        List  = self.info
        pos   = List.getSelectedIndex()
        model = List.getModel()
#       print '%s: "%s"  pos: %d' % ( todo, word, pos )
        if todo == 'Remove' :
            model.remove( pos )
        else :
            if todo == 'First' :
                model.insertElementAt( word, 0 )
            elif todo == 'Last' :
                model.insertElementAt( word, model.getSize() )
            elif todo == 'Before' :
                model.insertElementAt( word, pos )
            else :
                model.insertElementAt( word, pos + 1 )
            self.text.setText( '' )
        self.textCheck()

    #---------------------------------------------------------------------------
    # Name: textCheck()
    # Role: enable the "insert" buttons only if the text field has data
    # Note: KeyListener event handler called after user releases the key
    #---------------------------------------------------------------------------
    def textCheck( self, e = None ) :
        word  = self.text.getText().strip()
        index = self.info.getSelectedIndex()
        for name in 'First,Last'.split( ',' ) :
            self.buttons[ name ].setEnabled( len( word ) > 0 )
        for name in 'Before,After'.split( ',' ) :
            self.buttons[ name ].setEnabled(
                len( word ) > 0 and
                index > -1
            )
        self.buttons[ 'Remove' ].setEnabled( index > -1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List9() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
