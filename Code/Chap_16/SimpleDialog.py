#-------------------------------------------------------------------------------
#    Name: SimpleDialog.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script that demonstrates a modal vs non-modal
#          dialog boxes without an owner
#   Usage: wsadmin -f SimpleDialog.py
#            or
#          jython SimpleDialog.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import GridLayout

from   javax.swing import JButton
from   javax.swing import JDialog
from   javax.swing import JLabel
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: SimpleDialog()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SimpleDialog( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'SimpleDialog',
            size = ( 250, 100 ),
            layout = GridLayout( 0, 2 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'Modal',
                actionPerformed = self.makeDialog
            )
        )
        frame.add(
            JButton(
                'non-Modal',
                actionPerformed = self.makeDialog
            )
        )
        self.boxNum = 0
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: makeDialog()
    # Role: ActionListener event handler used to create the specified kind of
    #       JDialog box
    #---------------------------------------------------------------------------
    def makeDialog( self, event ) :
        cmd = event.getActionCommand()
        isModal = ( cmd == 'Modal' )
        dialog = JDialog(
            self.frame,                # Try None as owner...
#           None,                      # owner
            title = '%d: %s' % ( self.boxNum, cmd ),
            modal = isModal,
            size = ( 200, 100 ),
            locationRelativeTo = self.frame
        )
        self.boxNum += 1
        dialog.add( JLabel( cmd ) )
        dialog.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SimpleDialog() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
