#-------------------------------------------------------------------------------
#    Name: BoxLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script that positions application components using a
#          BoxLayout Manager, and a JTabbedPane to display the various component
#          alignments within each pane.
#    Note: Each layout is on a separate tab
#   Usage: wsadmin -f BoxLayoutDemo.py
#            or
#          jython BoxLayoutDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import Component
from   java.awt    import EventQueue
from   javax.swing import BoxLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JPanel
from   javax.swing import JTabbedPane

#-------------------------------------------------------------------------------
# Name: BoxLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class BoxLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'BoxLayoutDemo',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.addTabs( frame.getContentPane() )

        frame.setSize( 300, 175 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addTabs()
    # Role: Add the tab panels
    #---------------------------------------------------------------------------
    def addTabs( self, container ) :
        align = [
                    [ 'Left'  , Component.LEFT_ALIGNMENT   ],
                    [ 'Center', Component.CENTER_ALIGNMENT ],
                    [ 'Right' , Component.RIGHT_ALIGNMENT  ]
                ]

        names = '1,2,3 being the third number'.split( ',' )
        tabs  = JTabbedPane()
        for aName, aConst in align :
            tab = JPanel()
            tab.setLayout( BoxLayout( tab, BoxLayout.Y_AXIS ) )
            for name in names :
                tab.add( JButton( name, alignmentX = aConst ) )
            tabs.addTab( aName, tab )

        container.add( tabs )


#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( BoxLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
