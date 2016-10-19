#-------------------------------------------------------------------------------
#    Name: getHeaders6.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script using Jsoup to locate header tags
#    Note: Display the processed JFrame sections on a tabbed frame in an obvious
#          (bordered) table
#   Usage: set jsoup=-wsadmin_classpath C:\Programs\jsoup\jsoup-1.8.1.jar
#          wsadmin %jsoup% -f getHeaders6.py
#            or
#          set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar
#          jython getHeaders6.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

soupPath = r'C:\Programs\jsoup\jsoup-1.8.1.jar'
if 'JYTHON_JAR' in dir( sys ) :
    which = 'set JYTHONPATH=%s\njython' % soupPath
else :
    which = 'set jsoup=-wsadmin_classpath %s\nwsadmin %%jsoup%% -f' % soupPath

try :
    from org.jsoup import Jsoup
except :
    print '\nError: This script requires the jsoup library.'
    print '\nFor example:\n\n%s getHeaders6.py' % which
    sys.exit()

from   java.awt         import EventQueue

from   java.lang        import StringBuilder

from   javax.swing      import JEditorPane
from   javax.swing      import JFrame
from   javax.swing      import JScrollPane
from   javax.swing      import JTabbedPane
from   javax.swing      import SwingWorker

from   org.jsoup.select import NodeTraversor
from   org.jsoup.select import NodeVisitor

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
#           node.attr( 'border', '1' )
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
    def __init__( self, url, frame ) :
        self.url   = url               # URL to be retrieved
        self.frame = frame
        SwingWorker.__init__( self )

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
            print 'connecting...'
            doc = Jsoup.connect( self.url ).get()
            #-------------------------------------------------------------------
            # Use Jsoup methods to locate the HTML links & associated text
            #-------------------------------------------------------------------
            print 'processing...'
            doc.select( 'table' ).attr( 'border', '1' )
            #-------------------------------------------------------------------
            # Traverse the HTML, looking for <H3> tags and their tables...
            #-------------------------------------------------------------------
            visitor = FormattingVisitor( self.url )
            walker  = NodeTraversor( visitor )
            walker.traverse( doc )
#           Tabs = visitor.Tabs
#           print 'Tabs:', Tabs.getTabCount()
#           print visitor.toString()
            self.frame.add( visitor.Tabs )
            self.frame.validate()
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            print '\nError:', Type
            print 'value:', value

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        print 'done'

#-------------------------------------------------------------------------------
# Name: getHeaders6()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class getHeaders6( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'JFrame headers',
            size = ( 600, 250 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        url = 'http://docs.oracle.com/javase/7/docs/api/javax/swing/JFrame.html'
        headerTask( url, frame ).execute()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( getHeaders6() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
