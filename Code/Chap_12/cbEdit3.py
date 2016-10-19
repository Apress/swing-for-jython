#-------------------------------------------------------------------------------
#    Name: cbEdit3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with ComboBox cell editor & renderer
#    Note: This example increases the row height to make the cell contents more
#          readable.
#   Usage: wsadmin -f cbEdit3.py
#            or
#          jython cbEdit3.py
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

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Global list of values for combo box editor & renderer
#-------------------------------------------------------------------------------
choices = 'The,quick,brown,fox,jumped'.split( ',' )
choices.extend( 'over,the,lazy,spam'.split( ',' ) )

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
        self.comboBox = JComboBox( choices )
        DefaultCellEditor.__init__( self, self.comboBox )

#-------------------------------------------------------------------------------
# Name: cbRenderer
# Role: This renderer extends a component.
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class cbRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        DefaultTableCellRenderer.__init__( self )
        self.comboBox = JComboBox( choices )

    #---------------------------------------------------------------------------
    # Name: getTableCellRendererComponent()
    # Role: Return the component containing the rendered value
    # Note: Called frequently, don't create a new component each time
    #---------------------------------------------------------------------------
    def getTableCellRendererComponent(
        self,
        table,               # JTable  - table for which cell is being rendered
        value,               # Object  - value being rendered
        isSelected,          # boolean - Is value selected?
        hasFocus,            # boolean - Does this cell have focus?
        rowIndex,            # int     - Row # (0..N)
        vColIndex            # int     - Col # (0..N)
    ) :
        self.comboBox.setSelectedItem( value )
        return self.comboBox

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
            [ 'Uno' , choices[ 0 ] ],
            [ 'Dos' , choices[ 1 ] ],
            [ 'Tres', choices[ 2 ] ]
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
        return [ String, JComboBox ][ col ]

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
# Name: cbEdit3()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class cbEdit3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'cbEdit3',
            size = ( 200, 125 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm(), rowHeight = 20 )
        table.setDefaultRenderer( JComboBox, cbRenderer() )
        table.setDefaultEditor( JComboBox, cbEditor() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( cbEdit3() )
    if 'AdminConfig' in dir() :
        if sys.version.startswith( '2.1' ) :
            msg = '\nPress <Enter> to terminate this application:\n'
        else :
            msg = ''
        raw_input( msg )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
