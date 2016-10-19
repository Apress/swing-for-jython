#-------------------------------------------------------------------------------
#    Name: FileChooserDemo1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script demonstrating the use of the
#          JFileChooser class
#    Note: This uses all of the JFileChooser defaults
#   Usage: wsadmin -f FileChooserDemo1.py
#            or
#          jython FileChooserDemo1.py
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
from   javax.swing import JFileChooser
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: FileChooserDemo1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class FileChooserDemo1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'FileChooserDemo1',
            size = ( 150, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'File Open',
                actionPerformed = self.showFC
            )
        )
        self.label = JLabel( '', JLabel.CENTER )
        frame.add( self.label, BorderLayout.SOUTH )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: showFC()
    # Role: Demonstrate use of JFileChooser
    #---------------------------------------------------------------------------
    def showFC( self, event ) :
        fc = JFileChooser()
        result = fc.showOpenDialog( None )
        if result == JFileChooser.APPROVE_OPTION :
            message = 'result = "%s"' % fc.getSelectedFile()
        else :
            message = 'Request canceled by user'
        self.label.setText( message )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( FileChooserDemo1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
