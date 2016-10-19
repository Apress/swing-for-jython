#-------------------------------------------------------------------------------
#    Name: SplitPane5.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script using a frame containing nested JSplitPanes
#    Note: The top buttons have an ActionListener event handler assigned to
#          adjust the size of the divider
#   Usage: wsadmin -f SplitPane5.py
#            or
#          jython SplitPane5.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JPanel
from   javax.swing import JSplitPane

#-------------------------------------------------------------------------------
# Name: SplitPane5()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SplitPane5( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SplitPane5',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        self.sp = JSplitPane(
            JSplitPane.VERTICAL_SPLIT,
            self.sizeOptions(),
            JButton( 'Bottom' )
        )
#       print '\nInitial size:', self.sp.getDividerSize()
        frame.add( self.sp )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: sizeOptions()
    # Role: Create, and return a group of buttons used to resize the SplitPane
    #       divider
    #---------------------------------------------------------------------------
    def sizeOptions( self ) :
         pane = JPanel( GridLayout( 1, 0 ) )
         pane.add(
             JButton(
                 'Small',
                 actionPerformed = self.resize
             )
         )
         pane.add(
             JButton(
                 'Medium',
                 actionPerformed = self.resize
             )
         )
         pane.add(
             JButton(
                 'Large',
                 actionPerformed = self.resize
             )
         )
         return pane

    #---------------------------------------------------------------------------
    # Name: resize()
    # Role: ActionListener actionPerformed event handler for divider resizing
    #---------------------------------------------------------------------------
    def resize( self, event ) :
        sizes = {
            'Small'  : 0,
            'Medium' : 10,
            'Large'  : 20
        }
        name = event.getActionCommand()
        self.sp.setDividerSize( sizes[ name ] )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SplitPane5() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
