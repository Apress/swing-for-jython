#-------------------------------------------------------------------------------
#    Name: WSAShelp_01.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display the results of calling Help.help()
#    Note: This requires a WebSphere Application Server environment and is the
#          first iteration of this application script.
#   Usage: wsadmin -f WSAShelp_01.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 12/12/10  rag  0.01  New - Initial application
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import Font

from   javax.swing import JFrame
from   javax.swing import JTabbedPane
from   javax.swing import JTextArea
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: WSAShelp_01()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class WSAShelp_01( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'WSAShelp_01',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
#       text = Help.help()
#       tabs = text.count( '\t' )
#       text = Help.help().expandtabs()
#       rows = text.count( '\n' ) + 1
#       cols = max( [ len( x ) for x in text.splitlines() ] )
#       cols = max( [ len( x.expandtabs() ) for x in text.splitlines() ] )
#       print '\nrows: %d  cols: %d  tabs: %d' % ( rows, cols, tabs )
        frame.add(
            JScrollPane(
                JTextArea(
#                   text,
                    Help.help().expandtabs(),
                    20,
                    80,
                    font = Font( 'Courier' , Font.PLAIN, 12 )
                )
            )
        )
        frame.pack()
        size = frame.getSize()
#       print 'frame.getSize():', size
        loc = frame.getLocation()
#       print 'frame.getLocation():', loc
        loc.x -= ( size.width  >> 1 )
        loc.y -= ( size.height >> 1 )
        frame.setLocation( loc )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WSAShelp_01() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WSAShelp_01.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
