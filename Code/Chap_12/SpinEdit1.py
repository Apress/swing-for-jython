#-------------------------------------------------------------------------------
#    Name: SpinEdit1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing use of a JSpinner cell editor
#    Note: This script does not work with wsadmin, only Jython
#   Usage: jython SpinEdit1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   java.lang   import String

from   javax.swing import AbstractCellEditor
from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JSpinner
from   javax.swing import JTable
from   javax.swing import JTextField
from   javax.swing import SpinnerListModel

from   javax.swing.table import DefaultTableModel
from   javax.swing.table import TableCellEditor

#-------------------------------------------------------------------------------
# Name: editor()
# Role: Personalize spinner editor
#-------------------------------------------------------------------------------
class editor( AbstractCellEditor, TableCellEditor ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        values = 'Bacon,Eggs,Spam'.split( ',' )
        self.spinner = JSpinner( SpinnerListModel( values ) )
        self.spinner.setEditor(
            JSpinner.ListEditor( self.spinner )
        )

    #---------------------------------------------------------------------------
    # Name: getCellEditorValue()
    # Role: Returns the current spinner selection
    #---------------------------------------------------------------------------
    def getCellEditorValue( self ) :
        return self.spinner.getValue()

    #---------------------------------------------------------------------------
    # Name: getTableCellEditorComponent()
    # Role: Returns the component to be used to edit the cell values
    #---------------------------------------------------------------------------
    def getTableCellEditorComponent(
        self,                          # object reference
        table,                         # JTable
        value,                         # Object
        isSelected,                    # boolean
        row,                           # int
        column                         # int
    ) :
        self.spinner.setValue( value );
        return self.spinner;

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
            [ 'This', 'Bacon' ],
            [ 'That', 'Eggs'  ],
        ]
        DefaultTableModel.__init__( self, self.data, head )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return String

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Return 0 (false) for read-only cells.  Only column 1 is editable
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return col == 1

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
        self.data[ row ][ col ] = value

#-------------------------------------------------------------------------------
# Name: SpinEdit()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SpinEdit( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SpinEdit',
            size = ( 200, 106 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm(), rowHeight = 20 )
        table.setDefaultEditor( String, editor() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if globals().has_key( 'AdminConfig' ) :
        print '\nWarning: This script requires Jython, not wsadmin'
    else :
        EventQueue.invokeLater( SpinEdit() )
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: jython %s.py' % __name__
    sys.exit()