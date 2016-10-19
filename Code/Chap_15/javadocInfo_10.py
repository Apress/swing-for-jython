#-------------------------------------------------------------------------------
#    Name: javadocInfo_10.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing application to display the Swing Javadoc
#    Note: Replace the textTask class with the headerTask to display the results
#          in a JTabbedPane
#   Usage: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_10.py
#            or
#     ...  JYTHONPATH must include path to jsoup*.jar
#          e.g., set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar;
#          jython javadocInfo_10.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

which = [ 'wsadmin ... -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
try :
    from org.jsoup import Jsoup
except :
    print '\nError: This script requires the jsoup library.'
    if 'AdminConfig' in dir() :
        print 'e.g.: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_10.py'
    else :
        print 'Have the path to the jsoup*.jar in the JYTHONPATH environment'
        print 'variable when jython is executed.\n'
        print r'set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar'
        print 'jython javadocInfo_10.py'
    sys.exit()

from   java.awt    import BorderLayout
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Toolkit

from   javax.swing import DefaultListModel
from   javax.swing import JEditorPane
from   javax.swing import JFrame
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTabbedPane
from   javax.swing import JTextArea
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel
from   javax.swing import SwingWorker

from   org.jsoup.select import NodeTraversor
from   org.jsoup.select import NodeVisitor

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
    def __init__( self, List, text, url, nameLinkDict ) :
        self.List       = List         # Save provided references
        self.text       = text         # User input (filter) field
        self.url        = url          # URL to be used
        self.docLinks   = nameLinkDict # lookup result
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
            model = self.List.getModel()
            model.set( 0, 'Connecting...' )
            self.doc  = Jsoup.connect( self.url ).get()
            #-------------------------------------------------------------------
            # Use Jsoup methods to locate the HTML links & associated text
            #-------------------------------------------------------------------
            model.set( 0, 'Processing...' )
            #-------------------------------------------------------------------
            # Warning: Don't update the visible model within the loop.
            # Note: the 'abs:href' notation causes jsoup to return an absolute
            #       (i.e., complete) URL.
            #-------------------------------------------------------------------
            self.model = DefaultListModel()
            for link in self.doc.getElementsByTag( 'a' ) :
                name = link.text()
                href = link.attr( 'abs:href' )
                self.docLinks[ name ] = href
                self.model.addElement( name )
            #-------------------------------------------------------------------
            # Replace the visible model with the one containing the real data
            #-------------------------------------------------------------------
            self.List.setModel( self.model )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            print '\nsoupTask Error:', Type
            print 'value:', value
            sys.exit()

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        self.text.selectAll()
        self.text.requestFocusInWindow()

#-------------------------------------------------------------------------------
# Name: FormattingVisitor
# Role: jsoup NodeVisitor implementation to process HTML elements
#-------------------------------------------------------------------------------
class FormattingVisitor( NodeVisitor ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, url ) :
        self.Tabs   = JTabbedPane()
        self.header = re.compile( '[hH][1-6]$' )
        self.h3Text = ''

    #---------------------------------------------------------------------------
    # Name: head()
    # Role: Invoked when open tag is first seen
    # Note: node.text() = "the combined text of this element and all its children"
    #---------------------------------------------------------------------------
    def head( self, node, depth ) :
        name = node.nodeName()
        if re.match( self.header, name ) :
            self.h3Text = [ '', node.text() ] [ name[ 1 ] == '3' ]

    #---------------------------------------------------------------------------
    # Name: tail()
    # Role: Invoked when end tag is seen
    #---------------------------------------------------------------------------
    def tail( self, node, depth ) :
        name = node.nodeName()
        if self.h3Text and name == 'table' :
            node.attr( 'border', '1' )
            ePane = JEditorPane(
                'text/html',                # mime type
                '<html>' + str( node ),     # content
                editable = 0
            )
            self.Tabs.addTab( self.h3Text, JScrollPane( ePane ) )
#           print 'addTab( "%s" )' % self.h3Text

    #---------------------------------------------------------------------------
    # Name: toString()
    # Role: Return a multi-line string of the JTabbedPane titles
    #---------------------------------------------------------------------------
    def toString( self ) :
        tp = self.Tabs
        return '\n'.join(
            [
                tp.getTitleAt( i )
                for i in range( tp.getTabCount() )
            ]
        )

#-------------------------------------------------------------------------------
# Name: headerTask
# Role: Background processing of long running Jsoup calls
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class headerTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, url, splitPane ) :
        self.url   = url               # URL to be retrieved
        self.sPane = splitPane         # splitPane to be updated
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: showMessage()
    # Role: Utility routine used to verify the component type in the right side
    #       of the JSplitPane, and replace it, if necessary, to display the
    #       given message
    #---------------------------------------------------------------------------
    def showMessage( self, message ) :
       comp = self.sPane.getRightComponent()
       Type = str( comp.getClass() ).split( '.' )[ -1 ]
       if Type == 'JEditorPane' :
           comp.setText( '<html><h3>%s</h3></html>' % message )
       else :
           area = JEditorPane(
               'text/html',
               '<html><h3>%s</h3></html>' % message
           )
           self.sPane.setRightComponent( area )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Invoke jsoup to retrieve the page containing all item names & links
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Is it possible for an exception to occur?
        #-----------------------------------------------------------------------
        try :
            #-------------------------------------------------------------------
            # Inform the user of what is occurring, and try to retrieve the data
            #-------------------------------------------------------------------
            self.showMessage( 'Connecting...' )
            doc = Jsoup.connect( self.url ).get()
            #-------------------------------------------------------------------
            # Use Jsoup methods to locate the HTML links & associated text
            #-------------------------------------------------------------------
            self.showMessage( 'Processing...' )
            #-------------------------------------------------------------------
            # Traverse the HTML, looking for <H3> tags and their tables...
            #-------------------------------------------------------------------
            visitor = FormattingVisitor( self.url )
            walker  = NodeTraversor( visitor )
            walker.traverse( doc )
#           Tabs = visitor.Tabs
#           print 'Tabs:', Tabs.getTabCount()
#           print visitor.toString()
            self.sPane.setRightComponent( visitor.Tabs )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            self.showMessage( '\nheaderTask Error: %s\nvalue: %s' % ( Type, value ) )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        pass

#-------------------------------------------------------------------------------
# Name: javadocInfo_10()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class javadocInfo_10( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - initialize application variables
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.prevText = None      # Previously specified user input (text)

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
            'javadocInfo_10',
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
        model = DefaultListModel()
        model.addElement( 'One moment please...' )
        self.List = JList(
            model,
            valueChanged  = self.pick,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        #-----------------------------------------------------------------------
        # Put the List in a ScrollPane and place it in the middle of a pane
        #-----------------------------------------------------------------------
        pane = JPanel( layout = BorderLayout() )
        pane.add(
            JScrollPane(
                self.List,
                minimumSize = ( 300, 50 )
            ),
            BorderLayout.CENTER
        )
        #-----------------------------------------------------------------------
        # Add a TextField [for the URL of the selected entry] at the bottom
        #-----------------------------------------------------------------------
        self.text = JTextField(
            'Enter text...',
            caretUpdate = self.caretUpdate
        )
        pane.add( self.text, BorderLayout.SOUTH )
        #-----------------------------------------------------------------------
        # Add the pane and a scrollable TextArea to a SplitPane in the frame
        #-----------------------------------------------------------------------
        self.area = JEditorPane(
            'text/html',
            '<html><h3>Nothing selected</h3></html>',
            editable = 0
        )
        self.splitPane = JSplitPane(
            JSplitPane.HORIZONTAL_SPLIT,
            pane,
            self.area
        )
        self.splitPane.setDividerLocation( 234 )
        frame.add( self.splitPane )
        #-----------------------------------------------------------------------
        # Create a separate thread to locate & proces the remote URL
        #-----------------------------------------------------------------------
        self.Links   = {}    # Initialize the Links dictionary
        self.classes = None  # complete list of all classes found
        soupTask(
            self.List,       # The visible JList instance
            self.text,       # User input field
            JAVADOC_URL,     # Remote web page URL to be processed
            self.Links,      # Dictionary of links found
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

            #---------------------------------------------------------------
            # Is a "valid" item selected?
            #---------------------------------------------------------------
            index = List.getSelectedIndex()
            if index > -1 :
                choice = model.elementAt( index )
                if self.Links.has_key( choice ) :
                    url = self.Links[ choice ]
                    headerTask( url, self.splitPane ).execute()
            else :
                message = 'Nothing selected'
                comp = self.splitPane.getRightComponent()
                Type = str( comp.getClass() ).split( '.' )[ -1 ]
                if Type == 'JEditorPane' :
                    comp.setText( '<html><h3>%s</h3></html>' % message )
                else :
                    area = JEditorPane(
                        'text/html',
                        '<html><h3>%s</h3></html>' % message,
                        editable = 0
                    )
                    self.splitPane.setRightComponent( area )

    #---------------------------------------------------------------------------
    # Name: caretUpdate()
    # Role: CaretListener event handler used to monitor JTextField for user input
    #---------------------------------------------------------------------------
    def caretUpdate( self, e ) :
        field = e.getSource()
        text  = field.getText()
        if self.prevText == None :
            self.prevText = text

        if self.classes == None :
            result = self.Links.keys()
            if len( result ) > 0 :
                result.sort()
                self.classes = result

        #-----------------------------------------------------------------------
        # Did the user just move the cursor, or did they change the text field?
        #-----------------------------------------------------------------------
        if text != self.prevText :
#           print 'dot: %2d  text: "%s"' % ( e.getDot(), text )
            model = DefaultListModel()
            items = [ item for item in self.classes if item.find( text ) > -1 ]
            if len( items ) > 0 :
                for item in items :
                    model.addElement( item )
            else :
                model.addElement( 'No matching classes found.' )
            self.List.setModel( model )
        self.prevText = text

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( javadocInfo_10() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
