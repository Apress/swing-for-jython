#-------------------------------------------------------------------------------
#    Name: OptionDialogDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script demonstrating the use of the
#          JOptionPane.showOptionDialog() method call
#    Note: You are encouraged to uncomment lines to see what results
#   Usage: wsadmin -f OptionDialogDemo.py
#            or
#          jython OptionDialogDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue

from   javax.swing import JButton
from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JOptionPane

#-------------------------------------------------------------------------------
# Name: OptionDialogDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class OptionDialogDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'OptionDialogDemo',
            size = ( 150, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'showOptionDialog',
                actionPerformed = self.showOD
            )
        )
        self.label = JLabel( '', JLabel.CENTER )
        frame.add( self.label, BorderLayout.SOUTH )
        frame.setVisible( 1 )
 
    #---------------------------------------------------------------------------
    # Name: showOD()
    # Role: Demonstrate JOptionPane.showOptionDialog() method call
    #---------------------------------------------------------------------------
    def showOD( self, event ) :
        options = 'Bacon,Eggs,Spam'.split( ',' )
#       options = 'Now is the time for all good spam'.split( ' ' )
        result = JOptionPane.showOptionDialog(
            self.frame,                         # parentComponent
            'What goes good with spam?',        # message text
            'This is a test!',                  # title
            JOptionPane.DEFAULT_OPTION,         # optionType
#           JOptionPane.OK_CANCEL_OPTION,       # optionType
#           JOptionPane.YES_NO_OPTION,          # optionType
#           JOptionPane.YES_NO_CANCEL_OPTION,   # optionType
            JOptionPane.QUESTION_MESSAGE,       # messageType
            None,                               # icon
            options,                            # options
#           None,                               # options
            options[ -1 ]                       # initialValue
#           None                                # initialValue
        )
        self.label.setText( 'result = %d' % result )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( OptionDialogDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
