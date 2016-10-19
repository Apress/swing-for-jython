#-------------------------------------------------------------------------------
#    Name: InputDialogDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script demonstrating the use of the
#          JOptionPane.showInputDialog() method call
#    Note: You are encouraged to uncomment lines to see what results
#   Usage: wsadmin -f InputDialogDemo.py
#            or
#          jython InputDialogDemo.py
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
            'InputDialogDemo',
            size = ( 150, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'showInputDialog',
                actionPerformed = self.showID
            )
        )
        self.label = JLabel( '', JLabel.CENTER )
        frame.add( self.label, BorderLayout.SOUTH )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: showID()
    # Role: Demonstrate JOptionPane.showInputDialog() method call
    #---------------------------------------------------------------------------
    def showID( self, event ) :
        result = JOptionPane.showInputDialog(
            self.frame,                         # parentComponent
            'What is your favorite color?'      # message text
        )
        self.label.setText( 'result = "%s"' % result )

#   #---------------------------------------------------------------------------
#   # Name: showID()
#   # Role: JOptionPane.showOptionDialog() method with initialValue
#   #---------------------------------------------------------------------------
#   def showID( self, event ) :
#       result = JOptionPane.showInputDialog(
#           self.frame,                         # parentComponent
#           'What is your favorite color?',     # message text
#           'Spam'                              # initialValue
#       )
#       self.label.setText( 'result = "%s"' % result )

#   #---------------------------------------------------------------------------
#   # Name: showID()
#   # Role: JOptionPane.showOptionDialog() method with messageType
#   #---------------------------------------------------------------------------
#   # Note: messageType constants
#   #   JOptionPane.PLAIN_MESSAGE
#   #   JOptionPane.ERROR_MESSAGE
#   #   JOptionPane.INFORMATION_MESSAGE
#   #   JOptionPane.WARNING_MESSAGE
#   #   JOptionPane.QUESTION_MESSAGE
#   #---------------------------------------------------------------------------
#   def showID( self, event ) :
#       result = JOptionPane.showInputDialog(
#           self.frame,                         # parentComponent
#           'What is your favorite color?',     # message text
#           'Asked by the bridge guardian',     # title
#           JOptionPane.QUESTION_MESSAGE        # messageType
#       )
#       self.label.setText( 'result = "%s"' % result )

#   #---------------------------------------------------------------------------
#   # Name: showID()
#   # Role: Demonstrate the 7 argument showInputDialog() method call
#   #---------------------------------------------------------------------------
#   def showID( self, event ) :
#       COLORS = 'Red,Orange,Yellow,Green,Blue,Indigo,Violet'
#       colors = COLORS.split( ',' )
#       result = JOptionPane.showInputDialog(
#           self.frame,                     # parentComponent
#           'What is your favorite color?', # message text
#           'Asked by the bridge guardian', # title
#           JOptionPane.QUESTION_MESSAGE,   # messageType
#           None,                           # icon
#           colors,                         # selectionValues
#           colors[ -1 ]                    # initialSelectionValue
#       )
#       self.label.setText( 'result = "%s"' % result )

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
