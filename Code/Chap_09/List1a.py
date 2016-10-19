#-------------------------------------------------------------------------------
#    Name: List1a.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to display a list of words in a vector
#   Usage: wsadmin -f List1a.py
#            or
#          jython List1a.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/20  rag  0.1  Add - Change from using a simple array of strings to using
#                           a Java Vector of strings
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.util   import Vector
from   javax.swing import JFrame
from   javax.swing import JList

#-------------------------------------------------------------------------------
# Name: List1a()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List1a( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: data()
    # Role: Create and return a Vector of strings
    #---------------------------------------------------------------------------
    def data( self ) :
        result = Vector()
        items = 'Now is the time for all good spam'.split( ' ' )
        for item in items :
            result.add( item )
        return result

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List1a',
            size = ( 250, 200 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JList( self.data() ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List1a() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
