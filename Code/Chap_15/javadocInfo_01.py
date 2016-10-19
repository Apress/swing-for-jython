#-------------------------------------------------------------------------------
#    Name: javadocInfo_01.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing application for viewing the Swing documentation.
#    Note: Use Jsoup to connect to the Javadoc pages and retrieve the text and
#          display the list of classes in a JComboBox
#   Usage: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_01.py
#            or
#     ...  JYTHONPATH must include path to jsoup*.jar
#          e.g., set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar;
#          jython javadocInfo_01.py
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
        print 'e.g.: wsadmin -wsadmin_classpath jsoup-1.8.1.jar -f javadocInfo_01.py'
    else :
        print 'Have the path to the jsoup*.jar in the JYTHONPATH environment'
        print 'variable when jython is executed.\n'
        print r'set JYTHONPATH=C:\Programs\jsoup\jsoup-1.8.1.jar'
        print 'jython javadocInfo_01.py'
    sys.exit()

from   java.awt    import BorderLayout
from   java.awt    import EventQueue

from   javax.swing import JComboBox
from   javax.swing import JFrame
from   javax.swing import JLabel
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
    def __init__( self, comboBox, label, url ) :
        self.cb  = comboBox                # Save provided references
        self.msg = label
        self.url = url                     # URL to be used
        self.doc = None
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Disable the text (input) field, if it exists
        #-----------------------------------------------------------------------
        try :
            self.msg.setText( 'working...' )
            self.doc = Jsoup.connect( self.url ).get()
            self.msg.setText( 'ready' )
        except :
            Type, value = sys.exc_info()[ :2 ]
            print 'Error:', str( type )
            print 'value:', str( value )
            self.msg.setText( str( value ) )

        #-----------------------------------------------------------------------
        # Was the specified URL retrieved?
        #-----------------------------------------------------------------------
        if self.doc :
            self.cb.removeAllItems()
            for link in self.doc.getElementsByTag( 'a' ) :
                self.cb.addItem( str( link.text() ) )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #       Enable the text and button, and display the status message
    #---------------------------------------------------------------------------
    def done( self ) :
#       print 'done'
        pass

#-------------------------------------------------------------------------------
# Name: javadocInfo_01()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class javadocInfo_01( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'javadocInfo_01',
            locationRelativeTo = None,
            size = ( 250, 90 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        self.cb = JComboBox( [ 'One moment please' ] )
        frame.add( self.cb, BorderLayout.NORTH )
        self.msg = JLabel()
        frame.add( self.msg, BorderLayout.SOUTH )
        soupTask( self.cb, self.msg, JAVADOC_URL ).execute()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( javadocInfo_01() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
