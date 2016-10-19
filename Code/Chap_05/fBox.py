#-------------------------------------------------------------------------------
#    Name: fBox.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample application using Box & Glue classes
#    Note: The Submit button event handler display info about the TextField
#   Usage: wsadmin -f fBox.py
#            or
#          jython fBox.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Toolkit

from   javax.swing import Box
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: fBox()
# Role: Used to demonstrate how to create a Jython Swing application
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class fBox( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'flexible Box',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        print '\nscreenSize:', Toolkit.getDefaultToolkit().getScreenSize()

        box = Box.createHorizontalBox()
        box.add( Box.createGlue() )
        box.add( Box.createRigidArea( Dimension( 5, 5 ) ) )
        box.add( JLabel( 'Name:' ) )
        box.add( Box.createRigidArea( Dimension( 5, 5 ) ) )
        self.tf = box.add(
            JTextField(
                10 # ,
#               maximumSize = Dimension(   2000, 20 )
#               maximumSize = Dimension(  20000, 20 )
#               maximumSize = Dimension( 200000, 20 )
            )
        )
        box.add( Box.createRigidArea( Dimension( 5, 5 ) ) )
        box.add(
            JButton(
                'Submit',
                actionPerformed = self.buttonPress
            )
        )
        box.add( Box.createRigidArea( Dimension( 5, 5 ) ) )
        box.add( Box.createGlue() )

        frame.add( box )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: buttonPress()
    # Role: Event handler for button press
    #---------------------------------------------------------------------------
    def buttonPress( self, event ) :
        tf = self.tf
        print 'Width curr: %4d  min: %4d  max: %4d  pref: %4d' % (
            tf.getSize().getWidth(),
            tf.getMinimumSize().getWidth(),
            tf.getMaximumSize().getWidth(),
            tf.getPreferredSize().getWidth()
        )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( fBox() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
