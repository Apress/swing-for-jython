#-------------------------------------------------------------------------------
#    Name: Popup1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script using popup menus
#    Note: Right click on either input field to display the popup menu.
#   Usage: wsadmin -f Popup1.py
#            or
#          jython Popup1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from   __future__  import nested_scopes

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JMenuItem
from   javax.swing import JPopupMenu
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: Popup1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Popup1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: actionPerformed()
    # Role: Generic ActionListener event handler
    #---------------------------------------------------------------------------
    def actionPerformed( self, event ) :
        self.target.setText( event.getActionCommand() )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Popup1',
            layout = GridLayout( 0, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JLabel( 'One' ) )
        frame.add(
            JTextField(
                5,
                mousePressed  = self.PUcheck,
                mouseReleased = self.PUcheck
            )
        )
        self.PU = self.PUmenu()
        frame.add( JLabel( 'Two' ) )
        frame.add(
            JTextField(
                5,
                mousePressed  = self.PUcheck,
                mouseReleased = self.PUcheck
            )
        )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: PUmenu()
    # Role: Create popup menu
    #---------------------------------------------------------------------------
    def PUmenu( self ) :

        #-----------------------------------------------------------------------
        # Name: MenuItem()
        # Role: Return a JMenuItem with the given text, with actionPerformed set
        #-----------------------------------------------------------------------
        def MenuItem( text ) :
            return JMenuItem(
                text,
                actionPerformed = self.actionPerformed
            )

        popup  = JPopupMenu()
        popup.add( MenuItem( 'Spam'  ) )
        popup.add( MenuItem( 'Eggs'  ) )
        popup.add( MenuItem( 'Bacon' ) )
        return popup

    #-----------------------------------------------------------------------------
    # Name: PUcheck()
    # Role: MouseAdapter event handler
    #-----------------------------------------------------------------------------
    def PUcheck( self, event ) :
        if event.isPopupTrigger() :
            self.target = event.getSource()
            self.PU.show(
                event.getComponent(),
                event.getX(),
                event.getY()
            )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Popup1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()