#-------------------------------------------------------------------------------
#    Name: PropertyListener.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use a 
#          PropertyChangeListener.
#   Usage: wsadmin -f PropertyListener.py
#            or
#          jython PropertyListener.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/28  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import GridLayout

from   java.text   import NumberFormat

from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JFormattedTextField
from   javax.swing import JLabel
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTextArea
from   javax.swing import SwingConstants

#-------------------------------------------------------------------------------
# Name: PropertyListener
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class PropertyListener( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: changed()
    # Role: PropertyChangeListener event handler
    #---------------------------------------------------------------------------
    def changed( self, pce ) :
        format  = '    Name: %(name)s\n'
        format += 'OldValue: %(old)s\n'
        format += 'NewValue: %(new)s\n\n'
        name    = pce.getPropertyName()
        old     = `pce.getOldValue()`
        new     = `pce.getNewValue()`
        self.textArea.append( format % locals() )

    #---------------------------------------------------------------------------
    # Name: clear()
    # Role: Button event handler, used to clear the text area
    #---------------------------------------------------------------------------
    def clear( self, e ) :
        self.textArea.setText( '' )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :

        #---------------------------------------------------------------------------
        # Name: label()
        # Role: Instantiate a Right aligned label with the specified text
        #---------------------------------------------------------------------------
        def label( text ) :
            return JLabel(
                    text + ' ',
                    horizontalAlignment = SwingConstants.RIGHT
                )

        frame = JFrame(
            'PropertyListener',
            layout = BorderLayout(),
            locationRelativeTo = None,
            size = ( 400, 300 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        pane = JPanel( layout = GridLayout( 0, 2 ) )

        pane.add( label( 'Number:' ) )
        pane.add(
            JFormattedTextField(
                NumberFormat.getNumberInstance(),
                value = 12345.67890,
                columns = 10,
                propertyChange = self.changed
            )
        )

        pane.add( label( 'Currency:' ) )
        pane.add(
            JFormattedTextField(
                NumberFormat.getCurrencyInstance(),
                value = 12345.67890,
                columns = 10,
                propertyChange = self.changed
            )
        )

        frame.add( 
            JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                pane,
                JButton(
                    'Clear',
                    actionPerformed = self.clear
                ),
            ),
            BorderLayout.NORTH
        )

        self.textArea = JTextArea(
            rows = 10,
            columns = 40,
            editable = 0,
            focusable = 0,
            font = Font( 'Courier' , Font.BOLD, 12 )
        ) 
        frame.add(
            JScrollPane( self.textArea ),
            BorderLayout.CENTER
        )

        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( PropertyListener() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
