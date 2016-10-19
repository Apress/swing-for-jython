#-------------------------------------------------------------------------------
#    Name: iFrameEvents2.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script demonstrating some simple internal frames
#          event information details.
#    Note: This iteration adds a menu bar that allows the creation of additional
#          internal frames.
#   Usage: wsadmin -f iFrameEvents2.py
#            or
#          jython iFrameEvents2.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import EventQueue
from   java.awt    import Toolkit

from   javax.swing import event
from   javax.swing import JDesktopPane
from   javax.swing import JFrame
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem
from   javax.swing import JInternalFrame
from   javax.swing import JScrollPane
from   javax.swing import JTextArea

#-------------------------------------------------------------------------------
# Name: eventAdapter()
# Role: Used to implement a special internal frame to show InternalFrameEvent
#-------------------------------------------------------------------------------
class eventAdapter( event.InternalFrameAdapter ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: eventAdapter class constructor
    #---------------------------------------------------------------------------
    def __init__( self, textArea ) :
        self.textArea = textArea
        self.regexp = re.compile( '\[INTERNAL_FRAME_(\w+)]' )

    #---------------------------------------------------------------------------
    # Name: log()
    # Role: Utility method used to identify and log the event type, and the
    #       title of the internal frame for which the event was generated.
    #---------------------------------------------------------------------------
    def log( self, event ) :
        title = event.getInternalFrame().getTitle()
        mo = re.search( self.regexp, event.toString() )
        if mo :
            Type = mo.group( 1 ).capitalize()
        else :
            Type = 'unknown'
        self.textArea.append( '\n%s : %s' % ( title, Type ) )

    #---------------------------------------------------------------------------
    # Name: internalFrame*()
    # Role: InternalFrameAdapter event handlers
    #---------------------------------------------------------------------------
    def internalFrameActivated( self, ife ) :   self.log( ife )
    def internalFrameClosed( self, ife ) :      self.log( ife )
    def internalFrameClosing( self, ife ) :     self.log( ife )
    def internalFrameDeactivated( self, ife ) : self.log( ife )
    def internalFrameDeiconified( self, ife ) : self.log( ife )
    def internalFrameIconified( self, ife ) :   self.log( ife )
    def internalFrameOpened( self, ife ) :      self.log( ife )

#-------------------------------------------------------------------------------
# Name: eventLogger()
# Role: Used to implement a special internal frame to show InternalFrameEvent
#       details
#-------------------------------------------------------------------------------
class eventLogger( JInternalFrame ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: eventLogger class constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        JInternalFrame.__init__(
            self,
            'eventLogger',
            1,               # Resizeable  - yes
            0,               # Closeable   - no
            0,               # Maximizable - no
            1,               # Iconifiable - yes
            visible = 1,
            bounds = ( 0, 0, 250, 250 )
        )
        self.textArea = JTextArea(
             '',             # Inital text
             20,             # rows
             40,             # columns
             editable = 0    # read-only
        )
        self.eventListener = eventAdapter( self.textArea )
        self.add( JScrollPane( self.textArea ) )

    #---------------------------------------------------------------------------
    # Name: getListener()
    # Role: getter for returning reference to internal eventAdapter instance
    #---------------------------------------------------------------------------
    def getListener( self ) :
        return self.eventListener

#-------------------------------------------------------------------------------
# Name: iFrameEvents2()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class iFrameEvents2( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: addIframe()
    # Role: Terminate the applicaiton
    #---------------------------------------------------------------------------
    def addIframe( self, event ) :
        desktop = self.desktop
        self.iFrameCount += 1
        i = self.iFrameCount % 10
        inner = JInternalFrame(
            'Inner Frame #%d' % self.iFrameCount,
            1,                          # Resizeable
            1,                          # Closeable
            1,                          # Maximizable
            1,                          # Iconifiable
            bounds = ( i * 20 + 20, i * 20 + 20, 200, 200 )
        )
        inner.addInternalFrameListener( self.logger.getListener() )
        inner.setVisible( 1 )
        desktop.add( inner, i, 0 )

    #---------------------------------------------------------------------------
    # Name: exit()
    # Role: Terminate the applicaiton
    #---------------------------------------------------------------------------
    def exit( self, event ) :
        sys.exit()

    #---------------------------------------------------------------------------
    # Name: menuBar()
    # Role: Create, and return, the application menu bar
    #---------------------------------------------------------------------------
    def menuBar( self ) :
        result = JMenuBar()
        newMenu = result.add( JMenu( 'New' ) )
        newMenu.add(
            JMenuItem(
                'InnerFrame',
                actionPerformed = self.addIframe
            )
        )
        newMenu.addSeparator()
        newMenu.add(
            JMenuItem(
                'Exit',
                actionPerformed = self.exit
            )
        )
        return result

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        #-----------------------------------------------------------------------
        # First, we determine the size & location of the application frame
        #-----------------------------------------------------------------------
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        w = screenSize.width  >> 1          # 1/2 screen width
        h = screenSize.height >> 1          # 1/2 screen height
        x = ( screenSize.width  - w ) >> 1
        y = ( screenSize.height - h ) >> 1
        frame = JFrame(
            'iFrameEvents2',
            bounds = ( x, y, w, h ),        # location & size
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        #-----------------------------------------------------------------------
        # Next, we create, and add the menubar
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.menuBar() )
        #-----------------------------------------------------------------------
        # Then, we replace the frame ContentPane with a JDesktopPane instance
        # for all of the inner frames, and populate it with our eventLogger
        # inner frame instance.
        #-----------------------------------------------------------------------
        self.desktop = desktop = JDesktopPane()
        self.logger = eventLogger()
        desktop.add( self.logger, 0, 0 )
        frame.setContentPane( desktop )
        #-----------------------------------------------------------------------
        # Initialize the number of inner frames created
        #-----------------------------------------------------------------------
        self.iFrameCount = 0
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( iFrameEvents2() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
