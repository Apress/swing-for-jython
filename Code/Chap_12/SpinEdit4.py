#-------------------------------------------------------------------------------
#    Name: SpinEdit4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script using a spinner renderer
#    Note: Attempt #1 to fix the "broken" renderer
#   Usage: wsadmin -f SpinEdit4.py
#            or
#          jython SpinEdit4.py
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
from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JSpinner
from   javax.swing import JTable
from   javax.swing import JTextField
from   javax.swing import SpinnerListModel

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Global list of values for JSpinner editor & renderer
#-------------------------------------------------------------------------------
choices = 'Bacon,Eggs,Spam'.split( ',' )

#-------------------------------------------------------------------------------
# Name: editor()
# Role: Personalize spinner editor
#-------------------------------------------------------------------------------
class editor( DefaultCellEditor ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        DefaultCellEditor.__init__( self, JTextField() )
        self.spinner = JSpinner( SpinnerListModel( choices ) )
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
# Name: sRenderer
# Role: A renderer for our JSpinner cells
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class sRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.DTCR    = DefaultTableCellRenderer()
        self.spinner = JSpinner( SpinnerListModel( choices ) )

    #---------------------------------------------------------------------------
    # Name: getTableCellRendererComponent()
    # Role: Return the component containing the rendered value
    # Note: Called frequently, don't create a new component each time
    #---------------------------------------------------------------------------
    def getTableCellRendererComponent(
        self,
        table,               # table containing cell being rendered
        value,               # Object  - value being rendered
        isSelected,          # boolean - Is value selected?
        hasFocus,            # boolean - Does this cell have focus?
        row,                 # int     - Row # (0..N)
        col                  # int     - Col # (0..N)
    ) :
        comp = self.DTCR.getTableCellRendererComponent(
            table, value, isSelected, hasFocus, row, col
        )
#       print '[ %d, %d ] : %s on %s' % ( row, col, comp.getForeground(), comp.getBackground() )
        result = self.spinner
        result.setForeground( comp.getForeground() )
        result.setBackground( comp.getBackground() )
        result.setValue( value )
        return result

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
        return [ String, JSpinner ][ col ]

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
# Name: SpinEdit4()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SpinEdit4( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SpinEdit4',
            size = ( 200, 106 ),
#           size = ( 200, 116 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm(), rowHeight = 20 )
#       table = JTable( tm(), rowHeight = 25 )
        table.setDefaultRenderer( JSpinner, sRenderer() )
        table.setDefaultEditor( JSpinner, editor() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SpinEdit4() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
