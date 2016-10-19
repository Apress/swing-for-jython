#-------------------------------------------------------------------------------
#    Name: PortEdit.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with a custom cell editor that verifies
#          that the user input is a valid port number
#    Note: A simple range test is sufficient. See the stopCellEditing() method.
#   Usage: wsadmin -f PortEdit.py
#            or
#          jython PortEdit.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import EventQueue

from   java.lang   import Integer
from   java.lang   import String

from   javax.swing import DefaultCellEditor
from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JTable
from   javax.swing import JTextField

from   javax.swing.border import LineBorder

from   javax.swing.table  import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: portEditor()
# Role: Customized cell editor to verify user input for valid port values
#-------------------------------------------------------------------------------
class portEditor( DefaultCellEditor ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.textfield = JTextField(
            horizontalAlignment = JTextField.RIGHT
        )
        DefaultCellEditor.__init__( self, self.textfield )

    #---------------------------------------------------------------------------
    # Name: stopCellEditing()
    # Role: Verify user input
    #---------------------------------------------------------------------------
    def stopCellEditing( self ) :
        try :
            val = Integer.valueOf( self.textfield.getText() )
            if not ( -1 < val < 65536 ) :
                raise NumberFormatException()
            result = DefaultCellEditor.stopCellEditing( self )
        except :
            self.textfield.setBorder( LineBorder( Color.red ) )
            result = 0                 # false
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
            [ 'Min Port', Integer(   0   ) ],
            [ 'Max Port', Integer( 65535 ) ]
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
        return [ String, Integer ][ col ]

    #---------------------------------------------------------------------------
    # Name: getValueAt()
    # Role: Retrieve the specified value at the indicated row & col
    #---------------------------------------------------------------------------
    def getValueAt( self, row, col ) :
        return self.data[ row ][ col ]

    #---------------------------------------------------------------------------
    # Name: setValueAt()
    # Role: Save the specified (Integer) value at the indicated row & col
    #---------------------------------------------------------------------------
    def setValueAt( self, value, row, col ) :
        print 'tm.setValueAt():', value, type( value )
        self.data[ row ][ col ] = Integer( value )

#-------------------------------------------------------------------------------
# Name: PortEdit()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class PortEdit( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'PortEdit',
            size = ( 200, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        table = JTable( tm() )
        table.setDefaultEditor( Integer, portEditor() )
        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( PortEdit() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
