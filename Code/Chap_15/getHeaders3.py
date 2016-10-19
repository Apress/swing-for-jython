#-------------------------------------------------------------------------------
#    Name: getHeaders3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script using Jsoup to locate header tags
#    Note: Display just the H3 JFrame HTML headers in a scrollable list, and
#          some HTML for those sections on the console (i.e., stdout)
#   Usage: set jsoup=-wsadmin_classpath C:\Programs\jsoup\jsoup-1.8.1.jar
#          wsadmin %jsoup% -f getHeaders3.py
#            or
#          set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar
#          jython getHeaders3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
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
    print '\nFor example:\n\n%s getHeaders3.py' % which
    sys.exit()

from   java.awt         import EventQueue

from   java.lang        import StringBuilder

from   javax.swing      import JFrame
from   javax.swing      import JScrollPane
from   javax.swing      import JTextArea
from   javax.swing      import SwingWorker

from   org.jsoup.nodes  import TextNode

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
        self.result = StringBuilder()

    #---------------------------------------------------------------------------
    # Name: append()
    # Role: Add to the text
    #---------------------------------------------------------------------------
    def append( self, text ) :
        newline = [ '', '\n' ][ self.result.length() > 0 ]
        self.result.append( newline + text )

    #---------------------------------------------------------------------------
    # Name: head()
    # Role: Invoked when tag is first seen
    #---------------------------------------------------------------------------
    def head( self, node, depth ) :
        name = node.nodeName()
        if name == 'h3' and node.hasText() :
            text = node.text()
            if text.find( 'inherited' ) < 0 :
                self.append( '%s: %s' % ( name, text ) )

    #---------------------------------------------------------------------------
    # Name: tail()
    # Role: Invoked when end tag is seen
    #---------------------------------------------------------------------------
    def tail( self, node, depth ) :
        name = node.nodeName()
        if name == 'table' :
            print node
#       What do we want / need to do here ?

    #---------------------------------------------------------------------------
    # Name: toString()
    # Role: Return the accumulated string
    #---------------------------------------------------------------------------
    def toString( self ) :
        return str( self.result )

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
    def __init__( self, url, result ) :
        self.url    = url              # URL to be retrieved
        self.result = result
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: getPlainText()
    # Role: Traverse the specified jsoup element & return a string contain the
    #       header tags contained therein.
    #---------------------------------------------------------------------------
    def getPlainText( self, element ) :
        visitor = FormattingVisitor( self.url )
        walker  = NodeTraversor( visitor )
        walker.traverse( element )
        return visitor.toString()

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
            self.result.setText( 'connecting...' )
            doc = Jsoup.connect( self.url ).get()
            #-------------------------------------------------------------------
            # Use Jsoup methods to locate the HTML links & associated text
            #-------------------------------------------------------------------
            self.result.setText( 'processing...' )
            #-------------------------------------------------------------------
            # Traverse the HTML, looking for <H#...> tags
            #-------------------------------------------------------------------
            self.text = self.getPlainText( doc )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            print '\nError:', Type
            print 'value:', value
            self.result.setText( 'Exception: %s' % value )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        self.result.setText( self.text )

#-------------------------------------------------------------------------------
# Name: getHeaders3()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class getHeaders3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'JFrame headers',
            size = ( 500, 250 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        textArea = JTextArea()
        frame.add( JScrollPane( textArea ) )
        url = 'http://docs.oracle.com/javase/7/docs/api/javax/swing/JFrame.html'
        headerTask( url, textArea ).execute()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( getHeaders3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
