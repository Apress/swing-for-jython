#-------------------------------------------------------------------------------
#    Name: AvailableFonts.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to display the list of available fonts
#          in a scrollable TextArea.
#    Note: Portions of the data may be selected (highlighted), but no event
#          handlers have been defined so this is about all the user can do.
#   Usage: wsadmin -f AvailableFonts.py
#            or
#          jython AvailableFonts.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import GraphicsEnvironment

from   javax.swing import JFrame
from   javax.swing import JTextArea
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: AvailableFonts()
# Role: Create, and display our simple application
#-------------------------------------------------------------------------------
class AvailableFonts( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Build and display our graphical application
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'Available Fonts',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # First, we a local graphics environment (LGE) instance.  Then, we call
        # its getAvailableFontFamilyNames() method to obtain the list of all
        # available font names.
        #-----------------------------------------------------------------------
        lge = GraphicsEnvironment.getLocalGraphicsEnvironment()
        fontNames = lge.getAvailableFontFamilyNames()

        #-----------------------------------------------------------------------
        # The JTextArea will be used to hold the names of the available fonts.
        # Unfortunately, we don't know, for certain, how many font names are
        # present.  So, we need to have the JTextArea be within a JScrollPane,
        # "just in case" too many names exist for us to display at one time. ;-)
        #-----------------------------------------------------------------------
        frame.add(
            JScrollPane(
                JTextArea(
                    '\n'.join( fontNames ),
                    editable = 0,
                    rows = 8,
                    columns = 32
                )
            )
        )

        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( AvailableFonts() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
