#-------------------------------------------------------------------------------
#    Name: consoleTimeout_04.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple wsadmin Jython Swing application to display and modify the
#          WebSphere Application Server Admin console inactivity timeout value.
#    Note: Iteration #4 - Add menu items
#   Usage: wsadmin -f consoleTimeout_04.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------
'''
Command: consoleTimeout_04.py
Purpose: A simple wsadmin Jython script to display / modify the WebSphere
         Application Server administation console timeout value.
 Author: Robert A. (Bob) Gibson <bgibson@us.ibm.com>
   From: Swing for Jython
website: http://www.apress.com/978148420818
   Note: This script is provided "AS IS". See the "Help -> Notice" for details.
  Usage: wsadmin -f consoleTimeout_04.py
Example: ./wsadmin.sh -f consoleTimeout_04.py
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

from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   java.awt    import Font

from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JMenu
from   javax.swing import JMenuBar 
from   javax.swing import JMenuItem
from   javax.swing import JOptionPane
from   javax.swing import JTextField
from   javax.swing import SwingWorker

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
        # Simplify (shorten) references to self.messageText value
        #-----------------------------------------------------------------------
        messageText = self.messageText

        #-----------------------------------------------------------------------
        # Disable the text field and update the message area
        #-----------------------------------------------------------------------
        frame = self.app
        frame.textField.setEnabled( 0 )
        value = frame.textField.getText()
        frame.message.setText(
            '<html>working...' + ( '&nbsp;' * 20 )
        )

        #-----------------------------------------------------------------------
        # What kind of value was specified?
        #-----------------------------------------------------------------------
        if not re.search( re.compile( '^\d+$' ), value ) :
            messageText = 'Invalid numeric value: "%s"' % value
        else :
            if not frame.tuningParms :
                try :
                    AdminConfig.create(
                        'TuningParams',
                        frame.sesMgmt,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    messageText = 'The TuningParams object' + \
                                  'has been created successfully'
                except :
                    messageText = 'A problem was encountered ' + \
                                  'while creating the ' + \
                                  'TuningParams object.'
            else :
                try :
                    AdminConfig.modify(
                        frame.tuningParms,
                        [[ 'invalidationTimeout', value ]]
                    )
                    AdminConfig.save()
                    messageText = 'Update complete.'
                except :
                    messageText = 'A problem was encountered ' + \
                                  'while updating the ' + \
                                  'TuningParams object.'

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #       Enable the text and display the status message
    #---------------------------------------------------------------------------
    def done( self ) :
        frame = self.app
        frame.textField.setEnabled( 1 )
        frame.message.setText( self.messageText )

#-------------------------------------------------------------------------------
# Name: consoleTimeout_04
# Role: Define the consoleTimeout_04 class
#-------------------------------------------------------------------------------
class consoleTimeout_04( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: menuBar()
    # Role: create, and return appliation MenuBar
    #---------------------------------------------------------------------------
    def menuBar( self ) :
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
    # Name: run()
    # Role: Method called when thread execution begins
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'consoleTimeout_04',
            resizable = 0,
            layout = FlowLayout(),
            size = ( 180, 150 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Add the menu bar to the frame
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.menuBar() )

        dep = AdminConfig.getid( '/Deployment:isclite/' )
        #-----------------------------------------------------------------------
        # Check first for an error situation...
        #-----------------------------------------------------------------------
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

            #-------------------------------------------------------------------
            # Does a SessionManager exist?  If not, create one
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
            #-------------------------------------------------------------------
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

            #-------------------------------------------------------------------
            # Add the components to the frame...
            #-------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    # Name: Exit()
    # Role: File -> Exit event handler
    #---------------------------------------------------------------------------
    def Exit( self, event ) :
        sys.exit( 0 )

    #---------------------------------------------------------------------------
    # Name: about()
    # Role: Help -> About event handler
    #---------------------------------------------------------------------------
    def about( self, event ) :
        text = __doc__.replace( '<', '&lt;'
        ).replace( '>', '&gt;'
        ).replace( ' ', '&nbsp;'
        ).replace( '\n', '<br>' )
        JOptionPane.showMessageDialog(
            self.frame,
            JLabel(
                '<html>' + text,
                font = monoFont
            ),
            'About',
            JOptionPane.PLAIN_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: notice()
    # Role: Help -> Notice event handler
    #---------------------------------------------------------------------------
    def notice( self, event ) :
        JOptionPane.showMessageDialog(
            self.frame,
            disclaimer,
            'Notice',
            JOptionPane.WARNING_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: update()
    # Role: Invoked when the user presses <Enter>
    # Note: Instances of javax.swing.SwingWorker are not reusuable, so we create
    #       new instances for every update.
    #---------------------------------------------------------------------------
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
        EventQueue.invokeLater( consoleTimeout_04() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires the WebSphere Application Server product.'
        print 'Usage: wsadmin -f consoleTimeout_04.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
