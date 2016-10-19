#-------------------------------------------------------------------------------
#    Name: RadioButtons.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use a ButtonGroup with
#          ToggleButtons
#   Usage: wsadmin -f RadioButtons.py
#            or
#          jython RadioButtons.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   javax.swing import ButtonGroup
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JToggleButton

#-------------------------------------------------------------------------------
# Name: ButtonGroupDemo()
# Role: Used to demonstrate how to create some check boxes
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ButtonGroupDemo( java.lang.Runnable ) :

    #-----------------------------------------------------------------------------
    # Name: addRB()
    # Role: Used to add a radio button with the specified text to the specifie
    #       pane and button group
    #-----------------------------------------------------------------------------
    def addRB( self, pane, bg, text ) :
        bg.add(
            pane.add(
                JToggleButton(
                    text,
                    selected = ( text == '1' ),
                    itemStateChanged = self.toggle
                )
            )
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create the application frame & populate it
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'ToggleButton Group',
            layout = FlowLayout(),
            size   = ( 265, 100 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        cp = frame.getContentPane()
        bg = ButtonGroup()
        for i in range( 1, 6 ) :
            self.addRB( cp, bg, `i` )
        self.label = frame.add( JLabel( 'Selection: 1' ) )
        frame.setVisible( 1 )

    #-----------------------------------------------------------------------------
    # Name: toggle()
    # Role: Used to handle itemStateChanged events when the selection is made
    #-----------------------------------------------------------------------------
    def toggle( self, event ) :
        text = event.getItem().getText()
        self.label.setText( 'Selection: ' + text )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ButtonGroupDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
