#-------------------------------------------------------------------------------
#    Name: MessageDialogDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating how to use MessageDialog
#          instances in an application
#    Note: Copy GreedEgg.gif to C:\temp\GreenEgg.gif or correct the path in
#          the code below.
#   Usage: wsadmin -f MessageDialogDemo.py
#            or
#          jython MessageDialogDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue

from   java.net    import URL

from   javax.swing import ImageIcon
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JOptionPane

#-------------------------------------------------------------------------------
# Name: MessageDialogDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class MessageDialogDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'MessageDialogDemo',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'Minimum',
                actionPerformed = self.one
            ),
            BorderLayout.NORTH
        )
        frame.add(
            JButton(
                'Full',
                actionPerformed = self.two
            ),
            BorderLayout.SOUTH
        )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: one()
    # Role: Instantiate the user class
    #---------------------------------------------------------------------------
    def one( self, event ) :
        JOptionPane.showMessageDialog(
            self.frame,
            r'The "Full" button expects to find C:\temp\GreenEgg.gif'
        )

    #---------------------------------------------------------------------------
    # Name: two()
    # Role: Instantiate the user class
    #---------------------------------------------------------------------------
    def two( self, event ) :
        JOptionPane.showMessageDialog(
            self.frame,
            'Green Eggs & Spam!',
            'A complete breakfast',
            JOptionPane.INFORMATION_MESSAGE,
            ImageIcon( URL( 'file:///C:/temp/GreenEgg.gif' ) )
        )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( MessageDialogDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
