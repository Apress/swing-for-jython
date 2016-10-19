#-------------------------------------------------------------------------------
#    Name: NumbEdit.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing default numeric renderers & editors
#   Usage: wsadmin -f NumbEdit.py
#            or
#          jython NumbEdit.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   java.lang   import Byte, Double, Float, Integer
from   java.lang   import Number, Long, Short
from   java.lang   import String

from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JTable

from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: tm()
# Role: Personalize the table model to provide appropriate column data types
#-------------------------------------------------------------------------------
class tm( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        head = 'Byte,Double,Float,Integer,Long,Short'.split( ',' )
        self.data = [
            [ Byte( Byte.MIN_VALUE ),
              Double( Double.MIN_VALUE ),
              Float( Float.MIN_VALUE ),
              Integer( Integer.MIN_VALUE ),
              Long( Long.MIN_VALUE ),
              Short( Short.MIN_VALUE ) ],

            [ Byte( Byte.MAX_VALUE ),
              Double( Double.MAX_VALUE ),
              Float( Float.MAX_VALUE ),
              Integer( Integer.MAX_VALUE ),
              Long( Long.MAX_VALUE ),
              Short( Short.MAX_VALUE ) ]
        ]
        DefaultTableModel.__init__( self, self.data, head )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return [ Byte, Double, Float, Integer, Long, Short ][ col ]

    #---------------------------------------------------------------------------
    # Name: getValueAt()
    # Role: Retrieve the specified value at the indicated row & col
    #---------------------------------------------------------------------------
    def getValueAt( self, row, col ) :
        return self.data[ row ][ col ]

    #---------------------------------------------------------------------------
    # Name: setValueAt()
    # Role: Save the specified value at the indicated row & col
    #---------------------------------------------------------------------------
    def setValueAt( self, value, row, col ) :
        print 'tm.setValueAt():', value, type( value )
        Type = self.getColumnClass( col )
        self.data[ row ][ col ] = Type( value )

#-------------------------------------------------------------------------------
# Name: NumbEdit()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class NumbEdit( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'NumbEdit',
            size = ( 500, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( NumbEdit() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
