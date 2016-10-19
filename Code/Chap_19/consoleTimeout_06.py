#-------------------------------------------------------------------------------
#    Name: consoleTimeout_06.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple wsadmin Jython Swing application to display and modify the
#          WebSphere Application Server Admin console inactivity timeout value.
#    Note: Iteration #6 - Add another type of internal frame, one with a button
#   Usage: wsadmin -f consoleTimeout_06.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------
'''
Command: consoleTimeout_06.py
Purpose: A simple wsadmin Jython script to display / modify the WebSphere
         Application Server administation console timeout value.
 Author: Robert A. (Bob) Gibson <bgibson@us.ibm.com>
   From: Swing for Jython
website: http://www.apress.com/978148420818
   Note: This script is provided "AS IS". See the "Help -> Notice" for details.
  Usage: wsadmin -f consoleTimeout_06.py
Example: ./wsadmin.sh -f consoleTimeout_06.py
'''

#-------------------------------------------------------------------------------
# "ASIS" notice - Displayed by Help -> Notice event handler
#-------------------------------------------------------------------------------
disclaimer = '''
By accessing and/or using these sample files, you acknowledge that you have
read, understood, and agree, to be bound by these terms. You agree to the
binding nature of these english language terms and conditions regardless of
local language restrictions. If you do not agree to these terms, do not use the
files. International Business Machines corporation provides these sample files
on an "As Is" basis for your internal, non-commercial use and IBM disclaims all
warranties, express or implied, including, but not limited to, the warranty of
non-infringement and the implied warranties of merchantability or fitness for a
particular purpose.  IBM shall not be liable for any direct, indirect,
incidental, special or consequential damages arising out of the use or operation
of this software.  IBM has no obligation to provide maintenance, support,
updates, enhancements or modifications to the sample files provided.
'''

#-------------------------------------------------------------------------------
# Import the necessary Java, Jython, AWT & Swing modules & classes
#-------------------------------------------------------------------------------
import java
import re
import sys

from   java.awt          import EventQueue
from   java.awt          import FlowLayout
from   java.awt          import Font
from   java.awt          import Point

from   java.awt.event    import ActionListener

from   javax.swing       import JButton
from   javax.swing       import JDesktopPane
from   javax.swing       import JFrame
from   javax.swing       import JInternalFrame
from   javax.swing       import JLabel
from   javax.swing       import JMenu
from   javax.swing       import JMenuBar
from   javax.swing       import JMenuItem
from   javax.swing       import JOptionPane
from   javax.swing       import JTextField
from   javax.swing       import SwingWorker

from   javax.swing.event import InternalFrameListener

#-----------------------------------------------------------------------
# Font used to display help text
#-----------------------------------------------------------------------
monoFont = Font( 'Courier', Font.PLAIN, 12 )

#-------------------------------------------------------------------------------
# Name: WSAStask
# Role: Background processing of potentially long running WSAS scripting object
#       calls
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class WSAStask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: Since this class manipulates the Swing Application that creates it
    #       (i.e., making changes to specific application components), it needs
    #       to save a reference to the Swing Application that instantiates it.
    #---------------------------------------------------------------------------
    def __init__( self, app ) :
        self.app = app                     # application reference
        self.messageText = ''
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Define some literal message to make the code more readable
        #-----------------------------------------------------------------------
        success   = 'The TuningParams object has been created successfully'
        problem   = 'A problem was encountered while %s the TuningParams object.'
        badCreate = problem % 'creating'
        badUpdate = problem % 'updating'

        #-----------------------------------------------------------------------
        # Disable the text field and update the message area
        #-----------------------------------------------------------------------
        frame = self.app.inner             # Active Inner Frame
        frame.working()
        value = frame.getValue()
        frame.message.setText(
            '<html>working...' + ( '&nbsp;' * 20 )
        )

        #-----------------------------------------------------------------------
        # What kind of value was specified?
        #-----------------------------------------------------------------------
        if not re.search( re.compile( '^\d+$' ), value ) :
            self.messageText = 'Invalid numeric value: "%s"' % value
        else :
            if not self.app.tuningParms :
                try :
                    self.tuningParms = AdminConfig.create(
                        'TuningParams',
                        self.app.sesMgmt,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    self.messageText = success
                except :
                    self.messageText = badCreate
            else :
                try :
                    AdminConfig.modify(
                        self.app.tuningParms,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    self.messageText = 'Update complete.'
                except :
                    self.messageText = badUpdate

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #       Enable the text and button, and display the status message
    #---------------------------------------------------------------------------
    def done( self ) :
        frame = self.app.inner
        frame.finished()
        frame.message.setText( self.messageText )


#-------------------------------------------------------------------------------
# Name: InternalFrame
# Role: Provide a class for our internal frames
# Note: Unfortunately, multiple inheritance from two Java classes isn't allowed.
#       However, we can inherit from a class and an interface.
#-------------------------------------------------------------------------------
class InternalFrame( JInternalFrame, InternalFrameListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self,
        title,
        outer,
        size,
        location = None,
        layout = None
    ) :
        if location == None :
            location = Point( 0, 0 )
        if layout == None :
            layout = FlowLayout()
        JInternalFrame.__init__(
            self,
            title,
            0,               # resizeable = false
            0,               # closable  = false
            size = size,
            internalFrameListener = self,
            layout = layout
        )
        self.setLocation( location )   # keyword parm doesn't exist
        self.outer = outer             # application object
#       print 'InternalFrame.__init__()'

    #---------------------------------------------------------------------------
    # Name: internalFrameActivated()
    # Role: Event handler called when an internal frame instance is activated
    #---------------------------------------------------------------------------
    def internalFrameActivated( self, e ) :
        self.outer.inner = e.getInternalFrame()
#       print 'InternalFrame.internalFrameActivated()'

    #---------------------------------------------------------------------------
    # Name: internalFrameClosed()
    # Role: Event handler called when an internal frame instance is closed
    # Note: This event is ignored since these objects aren't closable
    #---------------------------------------------------------------------------
    def internalFrameClosed( self, e ) :
#       print 'InternalFrame.internalFrameClosed()'
        pass

    #---------------------------------------------------------------------------
    # Name: internalFrameClosing()
    # Role: Event handler called when an internal frame instance is being closed
    # Note: This event is ignored since these objects aren't closable
    #---------------------------------------------------------------------------
    def internalFrameClosing( self, e ) :
#       print 'InternalFrame.internalFrameClosing()'
        pass

    #---------------------------------------------------------------------------
    # Name: internalFrameDeactivated()
    # Role: Event handler called when an internal frame instance is deactivated
    #---------------------------------------------------------------------------
    def internalFrameDeactivated( self, e ) :
        self.outer.inner.message.setText( '' )
#       print 'InternalFrame.internalFrameDeactivated()'

    #---------------------------------------------------------------------------
    # Name: internalFrameDeiconified()
    # Role: Event handler called when an internal frame instance is deiconified
    # Note: This event is ignored
    #---------------------------------------------------------------------------
    def internalFrameDeiconified( self, e ) :
#       print 'InternalFrame.internalFrameDeiconified()'
        pass

    #---------------------------------------------------------------------------
    # Name: internalFrameIconified()
    # Role: Event handler called when an internal frame instance is iconified
    # Note: This event is ignored
    #---------------------------------------------------------------------------
    def internalFrameIconified( self, e ) :
#       print 'InternalFrame.internalFrameIconified()'
        pass

    #---------------------------------------------------------------------------
    # Name: internalFrameOpened()
    # Role: Event handler called when an internal frame instance is opened
    # Note: This event is ignored
    #---------------------------------------------------------------------------
    def internalFrameOpened( self, e ) :
#       print 'InternalFrame.internalFrameOpened()'
        pass

    #---------------------------------------------------------------------------
    # Name: getValue()
    # Role: value getter - specific to InternalFrame implementation
    #---------------------------------------------------------------------------
    def getValue( self ) :
        print 'InternalFrame.getValue() - not yet implemented'
        return None

    #---------------------------------------------------------------------------
    # Name: setValue()
    # Role: value setter - specific to InternalFrame implementation
    #---------------------------------------------------------------------------
    def setValue( self, value ) :
        print 'InternalFrame.setValue() - not yet implemented'

    #---------------------------------------------------------------------------
    # Name: working()
    # Role: Abstract method - Invoked when background processing begins
    #---------------------------------------------------------------------------
    def working( self ) :
        print 'InternalFrame.working() - not yet implemented'

    #---------------------------------------------------------------------------
    # Name: finished()
    # Role: Abstract method - Invoked when background processing is complete
    #---------------------------------------------------------------------------
    def finished( self ) :
        print 'InternalFrame.finished() - not yet implemented'


#-------------------------------------------------------------------------------
# Name: TextField
# Role: Implement an InternalFrame containing only a JTextField
#-------------------------------------------------------------------------------
class TextField( InternalFrame ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, outer ) :
        InternalFrame.__init__(
            self,
            'TextField',
            outer,
            size = ( 180, 85 ),
            location = Point( 5, 5 )
        )
        self.add( JLabel( 'Timeout (minutes):' ) )
        self.text = self.add( 
            JTextField(
                3,
                actionPerformed = outer.update
            )
        )
        self.message = self.add( JLabel() )
        self.setVisible( 1 )
        self.text.requestFocusInWindow()

    #---------------------------------------------------------------------------
    # Name: internalFrameActivated()
    # Role: Event handler called when the internal frame is activated
    #---------------------------------------------------------------------------
    def internalFrameActivated( self, e ) :
        self.outer.inner = e.getInternalFrame()
        self.setValue( self.outer.timeout )

    #---------------------------------------------------------------------------
    # Name: getValue()
    # Role: getter
    #---------------------------------------------------------------------------
    def getValue( self ) :
        return self.text.getText()

    #---------------------------------------------------------------------------
    # Name: setValue()
    # Role: setter
    #---------------------------------------------------------------------------
    def setValue( self, value ) :
        self.value = value
        self.text.setText( value )

    #---------------------------------------------------------------------------
    # Name: working()
    # Role: Invoked by WSASTask background method
    #---------------------------------------------------------------------------
    def working( self ) :
        self.text.setEnabled( 0 )

    #---------------------------------------------------------------------------
    # Name: finished()
    # Role: Invoked by WSASTask done method
    #---------------------------------------------------------------------------
    def finished( self ) :
        self.text.setEnabled( 1 )


#-------------------------------------------------------------------------------
# Name: TextandButton
# Role: Implement an InternalFrame containing a JTextField & a JButton
#-------------------------------------------------------------------------------
class TextandButton( TextField ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, outer ) :
        InternalFrame.__init__(
            self,
            'TextField and Button',
            outer,
            size = ( 180, 125 ),
            location = Point( 5, 95 )
        )
        self.add( JLabel( 'Timeout: (minutes)' ) )
        self.text = self.add( 
            JTextField(
                3,
                actionPerformed = outer.update
            )
        )
        self.button = self.add( 
            JButton(
                'Update',
                actionPerformed = outer.update
            )
        )
        self.message = self.add( JLabel() )
        self.setVisible( 1 )
        self.text.requestFocusInWindow()


#-------------------------------------------------------------------------------
# Name: consoleTimeout_06
# Role: Demonstrate the use of InternalFrames, and various Layout managers
#-------------------------------------------------------------------------------
class consoleTimeout_06( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Method called when thread execution begins
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'consoleTimeout_06',
            size = ( 428, 474 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Add the menu bar to the frame
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.MenuBar() )

        #-----------------------------------------------------------------------
        # Internal frames must be added to a desktop pane
        #-----------------------------------------------------------------------
        desktop = JDesktopPane()

        #-----------------------------------------------------------------------
        # Here is where we have to decide what needs to be displayed.
        #-----------------------------------------------------------------------
        if globals().has_key( 'AdminConfig' ) :
            self.timeout = self.initialTimeout()
            self.inner = TextField( self )       # JTextField only
            desktop.add( self.inner )
            desktop.add( TextandButton( self ) ) # JTextField & JButton
        else :
            self.inner = self.noWSAS()           # WebSphere not found
            desktop.add( self.inner )

        #-----------------------------------------------------------------------
        # Next, we add the desktop to the application frame; make the application
        # frame visible, and request the focus on one of the inner frames
        #-----------------------------------------------------------------------
        frame.add( desktop )
        frame.setVisible( 1 )
        self.inner.setSelected( 1 )

    #---------------------------------------------------------------------------
    # Name: initialTimeout()
    # Role: Return the initial / current admin console timeout value, if possible
    # Note: We presume that the AdminConfig scripting object is available
    #---------------------------------------------------------------------------
    def initialTimeout( self ) :
        dep = AdminConfig.getid( '/Deployment:isclite/' )
        timeout = None
        if dep :
            #-------------------------------------------------------------------
            # To manipulate the AdminConsole app we need to locate the
            # ApplicationDeployment object associated with the app, and the
            # ApplicationConfig object associated with the ApplicationDeployment
            # object. If no ApplicationConfig object exists, we will create one.
            #-------------------------------------------------------------------
            appDep = AdminConfig.list(
                'ApplicationDeployment',
                dep
            )
            appConfig = AdminConfig.list(
                'ApplicationConfig',
                appDep
            )
            if not appConfig :
                appConfig = AdminConfig.create(
                    'ApplicationConfig',
                    appDep,
                    []
                )

            #-------------------------------------------------------------------
            # Does a SessionManager exist?  If not, create one
            # Note: Save a reference to it (sesMgmt) in the application
            #-------------------------------------------------------------------
            self.sesMgmt = AdminConfig.list(
                'SessionManager',
                appDep
            )
            if not self.sesMgmt :
                self.sesMgmt = AdminConfig.create(
                    'SessionManager',
                    appConfig,
                    []
                )

            #-------------------------------------------------------------------
            # Get the tuningParams config ID, if one exists.
            # If it doesn't, one will be created elsewhere
            #-------------------------------------------------------------------
            self.tuningParms = AdminConfig.showAttribute(
                self.sesMgmt,
                'tuningParams'
            )
            if not self.tuningParms :
                timeout = None
                print "Error: tuningParams object doesn't exist."
            else :
                timeout = AdminConfig.showAttribute(
                    self.tuningParms,
                    'invalidationTimeout'
                )
        return timeout

    #---------------------------------------------------------------------------
    # Name: noWSAS()
    # Role: We have a problem - we're not being executed by wsadmin
    #---------------------------------------------------------------------------
    def noWSAS( self ) :
        frame = InternalFrame(
            'Notice',
            outer = self,
            size = ( 400, 125 ),
            location = Point( 5, 5 )
        )
        html  = '<html>This application requires WebSphere Application '
        html += 'Server<br><br>See Help -> About for details.'
        frame.text = JLabel( html )
        frame.add( frame.text )
        frame.setVisible( 1 )
        return frame

    #---------------------------------------------------------------------------
    # Name: Exit()
    # Role: File -> Exit event handler
    #---------------------------------------------------------------------------
    def Exit( self, event ) :
        sys.exit( 0 )

    #---------------------------------------------------------------------------
    # Name: MenuBar()
    # Role: Create the application menu bar
    #---------------------------------------------------------------------------
    def MenuBar( self ) :
        #-----------------------------------------------------------------------
        # Start by creating our application menubar
        #-----------------------------------------------------------------------
        menu = JMenuBar()

        #-----------------------------------------------------------------------
        # "File" entry
        #-----------------------------------------------------------------------
        jmFile   = JMenu( 'File' )
        jmiExit  = JMenuItem(
            'Exit',
            actionPerformed = self.Exit
        )
        jmFile.add( jmiExit )
        menu.add( jmFile )

        #-----------------------------------------------------------------------
        # "Help" entry
        #-----------------------------------------------------------------------
        jmHelp   = JMenu( 'Help' )
        jmiAbout = JMenuItem(
            'About',
            actionPerformed = self.about
        )
        jmiNote  = JMenuItem(
            'Notice',
            actionPerformed = self.notice
        )
        jmHelp.add( jmiAbout )
        jmHelp.add( jmiNote  )
        menu.add( jmHelp )

        return menu

    #---------------------------------------------------------------------------
    # Name: about()
    # Role: Help -> About event handler
    # Note: One way to display the script docstring (i.e., __doc__) as it appears
    #       is to use <html> text.
    #---------------------------------------------------------------------------
    def about( self, event ) :
        message = __doc__[ 1: ].replace( ' ', '&nbsp;' )
        message = message.replace( '<', '&lt;' )
        message = message.replace( '>', '&gt;' )
        message = message.replace( '\n', '<br>' )
        message = '<html>' + message
        message = JLabel( message, font = monoFont )
        JOptionPane.showMessageDialog(
            self.frame,
            message,
            'About',
            JOptionPane.PLAIN_MESSAGE
        )

    #--------------------------------------------------------------------------
    # Name: notice()
    # Role: Help -> Notice event handler
    #--------------------------------------------------------------------------
    def notice( self, event ) :
        JOptionPane.showMessageDialog(
            self.frame,
            disclaimer,
            'Notice',
            JOptionPane.WARNING_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: update()
    # Role: Invoked when the user changes a value (in any number of ways).
    # Note: Instances of SwingWorker are not reusuable, so we need to create a
    #       new instances for every update.
    #---------------------------------------------------------------------------
    def update( self, event ) :
        self.timeout = self.inner.getValue()
        WSAStask( self ).execute()


#-------------------------------------------------------------------------------
# Name: Anonymous
# Role: Main entry point for the script, used to verify that the script was
#       executed, and not imported.
# Note: wsadmin in WebSphere Application Server v 6.1 uses 'main', not '__main__'
#       However, it is important to note that the version of Jython that is
#       provided with WSAS V 6.1 does not include the SwingWorker class
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( consoleTimeout_06() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires the WebSphere Application Server product.'
        print 'Usage: wsadmin -f consoleTimeout_06.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
