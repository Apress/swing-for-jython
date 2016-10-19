#-------------------------------------------------------------------------------
#    Name: TabbedPaneDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple script demonstrating a JTabbedPane
#    Note: The buttons on the second tab have no ActionListener event handler
#          assigned
#   Usage: wsadmin -f TabbedPaneDemo.py
#            or
#          jython TabbedPaneDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import BorderLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel
from   javax.swing import JTabbedPane

#-------------------------------------------------------------------------------
# Name: TabbedPaneDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class TabbedPaneDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'TabbedPaneDemo',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.addTabs( frame.getContentPane() )

        frame.setSize( 300, 125 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addTabs()
    # Role: Add the tab panels
    #---------------------------------------------------------------------------
    def addTabs( self, container ) :
        tab1 = JPanel()
        tab1.add(
            JLabel(
                'The quick brown fox jumped over the lazy dog.'
            )
        )

        tab2 = JPanel()
        for name in 'A,B,C'.split( ',' ) :
            tab2.add( JButton( name ) )

        tab3 = JPanel()
        tab3.add(
            JLabel(
                'Now is the time for all good men to come to...'
            )
        )

        tabs = JTabbedPane()
        tabs.addTab( 'Uno' , tab1 )
        tabs.addTab( 'Dos' , tab2 )
        tabs.addTab( 'Tres', tab3 )

        container.add( tabs )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( TabbedPaneDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
