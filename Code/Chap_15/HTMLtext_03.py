#-------------------------------------------------------------------------------
#    Name: HTMLtext_03.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating one way in which HTML might
#          be used by an application
#    Note: This example demonstrates a valid way to use the Swing Event Dispatch
#          Thread to display a Jython Swing class
#   Usage: wsadmin -f HTMLtext_03.py
#            or
#          jython HTMLtext_03.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   javax.swing import JFrame
from   javax.swing import JToggleButton

#-------------------------------------------------------------------------------
# Name: HTMLtext_03()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class HTMLtext_03( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'HTMLtext_03',
            size = ( 100, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        text  = '<html><font color="red">Off</font>'
        label = frame.add(
            JToggleButton(
                text,
                itemStateChanged = self.toggle
            )
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: toggle()
    # Role: ItemListener event handler
    #---------------------------------------------------------------------------
    def toggle( self, event ) :
        button = event.getItem()
        button.setText(
            '<html><font color="%s">%s</font>' % [
               ( 'red'  , 'Off' ),
               ( 'green', 'On'  )
            ][ button.isSelected() ]
        )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( HTMLtext_03() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
