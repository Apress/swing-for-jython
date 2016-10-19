#-------------------------------------------------------------------------------
#    Name: CheckBoxes.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use the JCheckBox class
#   Usage: wsadmin -f CheckBoxes.py
#            or
#          jython CheckBoxes.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   javax.swing import JCheckBox
from   javax.swing import JFrame
from   javax.swing import JLabel

#-------------------------------------------------------------------------------
# Name: CheckBoxes()
# Role: Used to demonstrate how to create some check boxes
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class CheckBoxes( java.lang.Runnable ) :

    #-----------------------------------------------------------------------------
    # Name: addCB()
    # Role: Used to add a checkbox with the specified text to the content pane
    #-----------------------------------------------------------------------------
    def addCB( self, pane, text ) :
        pane.add(
            JCheckBox(
                text,
                itemStateChanged = self.toggle
            )
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create the application frame & populate it
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Check Boxes',
            layout = FlowLayout(),
            size   = ( 250, 100 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        cp = frame.getContentPane()
        self.addCB( cp, 'Yes' )
        self.addCB( cp, 'No'  )
        self.addCB( cp, 'Maybe' )
        self.label = frame.add( JLabel( 'Nothing selected' ) )
        frame.setVisible( 1 )

    #-----------------------------------------------------------------------------
    # Name: toggle()
    # Role: Used to handle itemStateChanged events when the selection is made
    #-----------------------------------------------------------------------------
    def toggle( self, event ) :
        cb    = event.getItem()
        text  = cb.getText()
        state = [ 'No', 'Yes' ][ cb.isSelected() ]
        self.label.setText( '%s selected? %s' % ( text, state ) )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( CheckBoxes() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
