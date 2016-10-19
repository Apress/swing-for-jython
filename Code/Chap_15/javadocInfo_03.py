#-------------------------------------------------------------------------------
#    Name: javadocInfo_03.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing application for viewing the Swing Javadoc
#    Note: When a class is selected retrieve it's HTML and display it in the
#          adjacent (scrollable) TextArea
#   Usage: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_03.py
#            or
#     ...  JYTHONPATH must include path to jsoup*.jar
#          e.g., set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar;
#          jython javadocInfo_03.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

which = [ 'wsadmin ... -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
try :
    from org.jsoup import Jsoup
except :
    print '\nError: This script requires the jsoup library.'
    if 'AdminConfig' in dir() :
        print 'e.g.: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_03.py'
    else :
        print 'Have the path to the jsoup*.jar in the JYTHONPATH environment'
        print 'variable when jython is executed.\n'
        print r'set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar'
        print 'jython javadocInfo_03.py'
    sys.exit()

from   java.awt    import BorderLayout
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Toolkit

from   javax.swing import DefaultListModel
from   javax.swing import JFrame
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTextArea
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel
from   javax.swing import SwingWorker

JAVADOC_URL = 'http://docs.oracle.com/javase/7/docs/api/allclasses-noframe.html'

#-------------------------------------------------------------------------------
# Name: soupTask
# Role: Background processing of long running Jsoup calls
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class soupTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: Since this class manipulates the Swing Application that creates it
    #       (i.e., making changes to specific application components), it needs
    #       to save references to the necessary/appropriate components.
    #---------------------------------------------------------------------------
    def __init__( self, List, area, url, result ) :
        self.List = List               # Save provided references
        self.msg  = area
        self.url  = url                # URL to be used
        self.doc  = None
        self.docLinks = result         # lookup result
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Invoke jsoup to retrieve the page containing all item names & links
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Is it possible for an exception to be thrown
        #-----------------------------------------------------------------------
        try :
            #-------------------------------------------------------------------
            # Inform the user of what is occurring, and try to retrieve the data
            #-------------------------------------------------------------------
            self.msg.setText( 'connecting...' )
            self.doc = Jsoup.connect( self.url ).get()
            #-------------------------------------------------------------------
            # Use Jsoup methods to locate the HTML links & associated text
            #-------------------------------------------------------------------
            self.msg.setText( 'processing...' )
            #-------------------------------------------------------------------
            # Warning: Don't update the visible model within the loop.
            #-------------------------------------------------------------------
            model = DefaultListModel()
            for link in self.doc.getElementsByTag( 'a' ) :
                name = link.text()
                href = link.attr( 'abs:href' )
                self.docLinks[ name ] = href
                model.addElement( name )
            #-------------------------------------------------------------------
            # Replace the visible model with the one containing the real data
            #-------------------------------------------------------------------
            self.List.setModel( model )
            self.msg.setText( 'Make a selection' )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            print '\nError:', Type
            print 'value:', value
            self.msg.setText( value )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        pass

#-------------------------------------------------------------------------------
# Name: textTask
# Role: Background processing of remote URL retrieval for display in a TextArea
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class textTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: Since this class manipulates the Swing Application that creates it
    #       (i.e., making changes to specific application components), it needs
    #       to save references to the necessary/appropriate components.
    #---------------------------------------------------------------------------
    def __init__( self, area, url ) :
        self.area = area               # Save area to be updated
        self.url  = url                # URL to be retrieved
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Use jsoup to retreive the remote URL
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Is it possible for an exception to be thrown
        #-----------------------------------------------------------------------
        try :
            #-------------------------------------------------------------------
            # Inform the user of what is occurring, and try to retrieve the data
            #-------------------------------------------------------------------
            self.area.setText( 'connecting...' )
            doc = Jsoup.connect( self.url ).get()
            self.area.setText( str( doc.normalise() ) )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            self.area.setText(
                '\nError: %s\nValue: %s' % ( Type, value )
            )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        pass

#-------------------------------------------------------------------------------
# Name: javadocInfo_03()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class javadocInfo_03( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        #-----------------------------------------------------------------------
        # Size the frame to use 1/2 of the screen
        #-----------------------------------------------------------------------
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        frameSize  = Dimension( screenSize.width >> 1, screenSize.height >> 1 )
        frame = JFrame(
            'javadocInfo_03',
            size = frameSize,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        #-----------------------------------------------------------------------
        # Reposition the frame to be in the center of the screen
        #-----------------------------------------------------------------------
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )
        #-----------------------------------------------------------------------
        # Initialize the list to have exactly 1 element
        #-----------------------------------------------------------------------
        self.List = JList(
            [ 'One moment please...' ],
            valueChanged  = self.pick,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        #-----------------------------------------------------------------------
        # Put the List in a ScrollPane and place it in the middle of a pane
        #-----------------------------------------------------------------------
        pane = JPanel( layout = BorderLayout() )
        pane.add(
            JScrollPane( self.List ),
            BorderLayout.CENTER
        )
        #-----------------------------------------------------------------------
        # Add a TextField [for the URL of the selected entry] at the bottom
        #-----------------------------------------------------------------------
        self.msg = JTextField()
        pane.add( self.msg, BorderLayout.SOUTH )
        #-----------------------------------------------------------------------
        # Add the pane and a scrollable TextArea to a SplitPane in the frame
        #-----------------------------------------------------------------------
        self.area = JTextArea()
        frame.add(
            JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                pane,
                JScrollPane( self.area )
            )
        )
        #-----------------------------------------------------------------------
        # Create a separate thread to locate & proces the remote URL
        #-----------------------------------------------------------------------
        self.Links = {}      # Initialize the Links dictionary
        soupTask(
            self.List,       # The visible JList instance
            self.msg,        # The message area (JTextField)
            JAVADOC_URL,     # Remote web page URL to be processed
            self.Links       # Dictionary of links found
        ).execute()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: pick()
    # Role: ListSelectionListener event handler
    #---------------------------------------------------------------------------
    def pick( self, e ) :
        #-----------------------------------------------------------------------
        # Note: Ignore valueIsAdjusting events
        #-----------------------------------------------------------------------
        if not e.getValueIsAdjusting() :
            List  = self.List
            model = List.getModel()
            #-------------------------------------------------------------------
            # Ignore events for initial "One moment please..." list
            #-------------------------------------------------------------------
            if model.getSize() > 1 :
                #---------------------------------------------------------------
                # Is an item selected, or not?
                #---------------------------------------------------------------
                index = List.getSelectedIndex()
                if index > -1 :
                    choice = model.elementAt( index )
                    url = self.Links[ choice ]
                    self.msg.setText( url )
                    textTask(
                        self.area,    # The text area to be updated
                        url           # Remote web page URL to be processed
                    ).execute()
                else :
                    self.msg.setText( 'Make a selection' )
                    self.area.setText( 'No item selected' )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( javadocInfo_03() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
