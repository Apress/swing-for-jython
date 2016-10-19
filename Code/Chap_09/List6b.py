#-------------------------------------------------------------------------------
#    Name: List6b.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Next iteration of our Jython Swing script showing how items can be
#          added and removed from a list.
#    Note: This script is incomplete.  Functionality remains to be added.
#          This iteration attempts to monitor changes to the JTextField using
#          a DocumentListener
#   Usage: wsadmin -f List6b.py
#            or
#          jython List6b.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/21  rag  0.2  Chg - replace InputMethodListener by DocumentListener
# 14/11/21  rag  0.1  Chg - Try using InputMethodListener
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

from   javax.swing.event import DocumentListener

#-------------------------------------------------------------------------------
# Name: DL()
# Role: Implement a DocumentListener class to monitor text changes to a textfield
#-------------------------------------------------------------------------------
class DL( DocumentListener ) :

    #---------------------------------------------------------------------------
    # Name: changedUpdate()
    # Role: DocumentListener event handler
    #---------------------------------------------------------------------------
    def changedUpdate( self, e ) :
        print 'changedUpdate() :', e

    #---------------------------------------------------------------------------
    # Name: insertUpdate()
    # Role: DocumentListener event handler
    #---------------------------------------------------------------------------
    def insertUpdate( self, e ) :
        print 'insertUpdate() :', e

    #---------------------------------------------------------------------------
    # Name: removeUpdate()
    # Role: DocumentListener event handler
    #---------------------------------------------------------------------------
    def removeUpdate( self, e ) :
        print 'removeUpdate() :', e


#-------------------------------------------------------------------------------
# Name: List6b()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List6b( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List6b',
            size = ( 200, 220 ),
            layout = GridLayout( 1, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        panel = JPanel( layout = GridLayout( 0, 1 ) )
        self.buttons = {}
        for name in 'First,Last,Before,After,Remove'.split( ',' ) :
            self.buttons[ name ] = panel.add( self.button( name ) )

        self.text = panel.add( JTextField( 10 ) )
        self.text.getDocument().addDocumentListener( DL() )
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
            valueChanged = self.selection,
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
    # Name: button()
    # Role: Create a button with the specified text, and with an actionListener
    #       event handler assigned
    #---------------------------------------------------------------------------
    def button( self, text ) :
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
        todo = event.getActionCommand()
        word = self.text.getText().strip()
        List = self.info
        pos  = List.getSelectedIndex()
        print '%s: "%s"  pos: %d' % ( todo, word, pos )
        if todo == 'Remove' :
            List.getModel().remove( pos )
            self.buttons[ todo ].setEnabled( 0 )
        
    #---------------------------------------------------------------------------
    # Name: selection()
    # Role: ListSelectionListener event handler
    #---------------------------------------------------------------------------
    def selection( self, e ) :
#       print 'selection():', e
        if e.getValueIsAdjusting() :
            si = e.getSource().getSelectedIndex()
            self.buttons[ 'Remove' ].setEnabled( si > -1 )


#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List6b() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
