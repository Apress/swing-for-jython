#-------------------------------------------------------------------------------
#    Name: CustomDialog.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing one way to use a custom dialog
#          to obtain input from the user.
#   Usage: wsadmin -f CustomDialog.py
#            or
#          jython CustomDialog.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import GridLayout

from   javax.swing import JButton
from   javax.swing import JDialog
from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JPanel
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: CustomDialog()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class CustomDialog( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'CustomDialog',
            size = ( 200, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        self.label = frame.add( JLabel( '' ) )
        frame.add(
            JButton(
                'Prompt user',
                actionPerformed = self.popup
            ),
            BorderLayout.SOUTH
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: popup()
    # Role: ActionListener event handler - invoked when button is pressed
    #---------------------------------------------------------------------------
    def popup( self, event ) :
        self.dialog = dialog = JDialog(
            self.frame,
            'Name prompt',
            1,
            layout = GridLayout( 0, 2 ),
            locationRelativeTo = self.frame
        )
        dialog.add( JLabel( "What's your name?" ) )
        self.text = dialog.add(
            JTextField(
                10,
                actionPerformed = self.enter
            )
        )
        self.result = None
        dialog.pack()
        dialog.setVisible( 1 )
        self.label.setText( 'Name = "%s"' % self.result )
 
    #---------------------------------------------------------------------------
    # Name: enter()
    # Role: ActionListener event handler - invoked when user presses <Enter>
    #---------------------------------------------------------------------------
    def enter( self, event ) :
        self.result = self.text.getText()
        self.dialog.setVisible( 0 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( CustomDialog() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
