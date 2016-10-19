#-------------------------------------------------------------------------------
#    Name: consoleTimeout_03.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple wsadmin Jython Swing application to display and modify the
#          WebSphere Application Server Admin console inactivity timeout value.
#    Note: Iteration #3 - Add WSAStask class a SwingWorker class descendent
#   Usage: wsadmin -f consoleTimeout_03.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Import the necessary Java, Python, AWT & Swing classes
#-------------------------------------------------------------------------------
import java
import re
import sys

from   java.awt    import EventQueue
from   java.awt    import FlowLayout

from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JTextField
from   javax.swing import SwingWorker

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
        # Simple error message
        #-----------------------------------------------------------------------
        problem = 'A problem was encountered while %s the TuningParams object.'

        #-----------------------------------------------------------------------
        # Simplify (shorten) references to self.messageText value
        #-----------------------------------------------------------------------
        messageText = self.messageText

        #-----------------------------------------------------------------------
        # Disable the text field and update the message area
        #-----------------------------------------------------------------------
        self.app.textField.setEnabled( 0 )
        self.app.message.setText(
            '<html>working...' + ( '&nbsp;' * 20 )
        )

        value = self.app.textField.getText()    # JTextField value
        #-----------------------------------------------------------------------
        # What kind of value was specified?
        #-----------------------------------------------------------------------
        if not re.search( re.compile( '^\d+$' ), value ) :
            messageText = 'Invalid numeric value: "%s"' % value
        else :
            if not self.app.tuningParms :
                try :
                    AdminConfig.create(
                        'TuningParams',
                        self.app.sesMgmt,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    messageText = 'The TuningParams object' + \
                                  'has been created successfully'
                except :
                    messageText = problem % 'creating'
            else :
                try :
                    AdminConfig.modify(
                        self.app.tuningParms,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    messageText = 'Update complete.'
                except :
                    messageText = problem % 'updating'

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #       Enable the text and display the status message
    #---------------------------------------------------------------------------
    def done( self ) :
        self.app.textField.setEnabled( 1 )
        self.app.message.setText( self.messageText )

#-------------------------------------------------------------------------------
# Name: consoleTimeout_03
# Role: Define the consoleTimeout_03 class
#-------------------------------------------------------------------------------
class consoleTimeout_03( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'consoleTimeout_03',
            resizable = 0,
            layout = FlowLayout(),
            size = ( 180, 120 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        dep = AdminConfig.getid( '/Deployment:isclite/' )
        if dep :
            #-------------------------------------------------------------------------
            # To manipulate the AdminConsole app we need to locate the Application-
            # Deployment object associated with the app, and the ApplicationConfig
            # object associated with the app. If no ApplicationConfig object exists,
            # create one.
            #-------------------------------------------------------------------------
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

            #-------------------------------------------------------------------------
            # Does a SessionManager exist?  If not, create one
            #-------------------------------------------------------------------------
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

            #-------------------------------------------------------------------------
            # Get the tuningParams config ID, if one exists.
            #-------------------------------------------------------------------------
            self.tuningParms = AdminConfig.showAttribute(
                self.sesMgmt,
                'tuningParams'
            )
            if not self.tuningParms :
                timeout = ''
                messageText = "tuningParams object doesn't exist."
            else :
                timeout = AdminConfig.showAttribute(
                    self.tuningParms,
                    'invalidationTimeout'
                )
                messageText = ''

            #-------------------------------------------------------------------------
            # Add the components to the frame...
            #-------------------------------------------------------------------------
            frame.add( JLabel( 'Timeout:' ) )
            self.textField = frame.add(
                JTextField(
                    3,
                    text = timeout,
                    actionPerformed = self.update
                )
            )
            frame.add( JLabel( 'minutes' ) )

            self.message = frame.add( JLabel( messageText ) )
        else :
            frame.add(
                JLabel(
                    '<html>The AdminConsole application<br>' + \
                    'is not available on the<br>' + \
                    'specified profile.'
                )
            )
            frame.pack()

        frame.setVisible( 1 )

    #-----------------------------------------------------------------------------
    # Name: update()
    # Role: Invoked when the user presses <Enter> on the input field
    # Note: This event handler does too much!
    #       The actual work (i.e., calls to AdminConfig methods ) should be done
    #       on a separate (i.e., SwingWorker) thread
    #-----------------------------------------------------------------------------
    def update( self, event ) :
        WSAStask( self ).execute()

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
# Note: wsadmin in WebSphere Application Server v 6.1 uses 'main', not '__main__'
#       However, it is important to note that the version of Jython that is
#       provided with WSAS V 6.1 does not include the SwingWorker class
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( consoleTimeout_03() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires the WebSphere Application Server product.'
        print 'Usage: wsadmin -f consoleTimeout_03.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
