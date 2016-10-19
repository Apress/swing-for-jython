#-------------------------------------------------------------------------------
#    Name: consoleTimeout_02.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple wsadmin Jython Swing application to display and modify the
#          WebSphere Application Server Admin console inactivity timeout value.
#    Note: Iteration #2 - First Swing version using 
#          This version is "too simple".  See the text for details.
#   Usage: wsadmin -f consoleTimeout_02.py
#            or
#          jython consoleTimeout_02.py
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

#-------------------------------------------------------------------------------
# Name: consoleTimeout_02
# Role: Define the consoleTimeout_02 class
#-------------------------------------------------------------------------------
class consoleTimeout_02( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'consoleTimeout_02',
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
            appDep    = AdminConfig.list(
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
            self.text = frame.add(
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
        value = self.text.getText()
        if not re.search( re.compile( '^\d+$' ), value ) :
            text = 'Invalid numeric value: "%s"' % value
        else :
            if not self.tuningParms :
                try :
                    AdminConfig.create(
                        'TuningParams',
                        self.sesMgmt,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    text = 'The TuningParams object has ' + \
                           'been created successfully'
                except :
                    text = 'A problem was encountered while ' + \
                           'creating the TuningParams object.'
            else :
                try :
                    AdminConfig.modify(
                        self.tuningParms,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    text = 'Update successful.'
                except :
                    text = 'A problem was encountered while ' + \
                           'updating the TuningParams object.'
        self.message.setText( text )

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
# Note: wsadmin in WebSphere Application Server v 6.1 uses 'main', not '__main__'
#       However, it is important to note that the version of Jython that is
#       provided with WSAS V 6.1 does not include the SwingWorker class
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( consoleTimeout_02() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires the WebSphere Application Server product.'
        print 'Usage: wsadmin -f consoleTimeout_02.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
