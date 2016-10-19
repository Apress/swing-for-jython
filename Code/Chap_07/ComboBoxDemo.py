#-------------------------------------------------------------------------------
#    Name: ComboBoxDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that demonstrates a JComboBox field.
#   Usage: wsadmin -f ComboBoxDemo.py
#            or
#          jython ComboBoxDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt       import EventQueue
from   java.awt       import FlowLayout
from   java.awt.event import ActionListener
from   javax.swing    import JComboBox
from   javax.swing    import JFrame
from   javax.swing    import JLabel

#-------------------------------------------------------------------------------
# Name: ComboBoxDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ComboBoxDemo( java.lang.Runnable, ActionListener ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'ComboBoxDemo',
            size = ( 200, 100 ),
            layout = FlowLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JLabel( 'Pick one:' ) )
        choices = 'The,quick,brown,fox,jumped'.split( ',' )
        choices.extend( 'over,the,lazy,spam'.split( ',' ) )
        ComboBox = frame.add( JComboBox( choices ) )
        ComboBox.addActionListener( self )
        self.msg = frame.add( JLabel() )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: actionPerformed()
    # Role: ActionListener Event handler for the JComboBox
    #---------------------------------------------------------------------------
    def actionPerformed( self, event ) :
        ComboBox = event.getSource()
        msg = 'Selection: ' + ComboBox.getSelectedItem()
        self.msg.setText( msg )


#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ComboBoxDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
