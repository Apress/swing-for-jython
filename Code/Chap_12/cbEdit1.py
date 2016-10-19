#-------------------------------------------------------------------------------
#    Name: cbEdit1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with a custom ComboBox cell editor
#    Note: There is no indication that the values in column 2 use a ComboBox as
#          an editor until a cell in that column is double clicked.
#   Usage: wsadmin -f cbEdit1.py
#            or
#          jython cbEdit1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   java.lang   import String

from   javax.swing import DefaultCellEditor
from   javax.swing import JComboBox
from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JTable

from   javax.swing.table  import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: cbEditor()
# Role: Customized cell editor to verify user input for valid port values
#-------------------------------------------------------------------------------
class cbEditor( DefaultCellEditor ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        choices = 'The,quick,brown,fox,jumped'.split( ',' )
        choices.extend( 'over,the,lazy,spam'.split( ',' ) )
        self.comboBox = JComboBox( choices )
        DefaultCellEditor.__init__( self, self.comboBox )

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
        head = 'Name,Value'.split( ',' )
        self.data = [
            [ 'Which', 'spam' ]
        ]
        DefaultTableModel.__init__( self, self.data, head )

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Return 0 (false) for read-only cells.  Only column 1 is editable
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return col == 1

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return String

    #---------------------------------------------------------------------------
    # Name: getValueAt()
    # Role: Retrieve the specified value at the indicated row & col
    #---------------------------------------------------------------------------
    def getValueAt( self, row, col ) :
        return self.data[ row ][ col ]

    #---------------------------------------------------------------------------
    # Name: setValueAt()
    # Role: Save the specified (String) value at the indicated row & col
    #---------------------------------------------------------------------------
    def setValueAt( self, value, row, col ) :
        print 'tm.setValueAt():', value, type( value )
        self.data[ row ][ col ] = value

#-------------------------------------------------------------------------------
# Name: cbEdit1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class cbEdit1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'cbEdit1',
            size = ( 200, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm() )
        table.setDefaultEditor( String, cbEditor() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( cbEdit1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
