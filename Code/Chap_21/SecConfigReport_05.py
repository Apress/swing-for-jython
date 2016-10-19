#-------------------------------------------------------------------------------
#    Name: SecConfigReport_05.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to display the results of the AdminTask
#          generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f SecConfigReport_05.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/05  rag  0.5   Fix - resolve heading rows highlighting deficiencies
# 13/01/05  rag  0.4   Fix - highlight heading rows using color
# 13/01/05  rag  0.3   Add - TableModel & CellRenderer to make heading rows bold
# 13/01/05  rag  0.2   Fix - Ignore the trailing (empty delimiter)
# 13/01/05  rag  0.1   New - Initial try - simple display of text data
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import EventQueue
from   java.awt    import Font

from   java.lang   import String

from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JScrollPane
from   javax.swing import ListSelectionModel

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: reportTableModel
# Role: Define table data characteristics
#-------------------------------------------------------------------------------
class reportTableModel( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: Save the initial data for easy highlight removal
    #---------------------------------------------------------------------------
    def __init__( self, data, headings ) :
        DefaultTableModel.__init__( self, data, headings )

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Each cell in the table is read-only
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return 0

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Each cell in the table is a java.lang.String
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return String

#-------------------------------------------------------------------------------
# Name: reportRenderer
# Role: Display the method table cells using the appropriate width & hilighting
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class reportRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: Initialize the default cell background & foreground color variables
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.bg = self.fg = None

    #---------------------------------------------------------------------------
    # Name: getTableCellRendererComponent()
    # Role: Return the component containing the rendered value
    # Note: Called frequently, don't create a new component each time
    #---------------------------------------------------------------------------
    def getTableCellRendererComponent(
        self,
        table,               # JTable  - table containing value
        value,               # Object  - value being rendered
        isSelected,          # boolean - Is value selected?
        hasFocus,            # boolean - Does this cell have focus?
        row,                 # int     - Row # ( 0 .. N-1 )
        col                  # int     - Col # ( 0 .. N-1 )
    ) :
        #-----------------------------------------------------------------------
        # Start by retrieving the default renderer component (i.e., JLabel)
        #-----------------------------------------------------------------------
        DTCR = DefaultTableCellRenderer
        comp = DTCR.getTableCellRendererComponent(
            self, table, value, isSelected, hasFocus, row, col
        )
        if self.bg == self.fg :
            self.bg = comp.getBackground()
            self.fg = comp.getForeground()
        if value :
            if table.getValueAt( row, 0 ).startswith( '_' ) :
                comp.setBackground( Color.blue )
                comp.setForeground( Color.white )
                if col == 0 :
                    value = value[ 1: ]
                comp.setText( '<html><b>%s</b>' % value )
            else :
                comp.setBackground( self.bg )
                comp.setForeground( self.fg )

        return comp

#-------------------------------------------------------------------------------
# Name: SecConfigReport_05()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SecConfigReport_05( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SecConfigReport_05',
            size = ( 300, 300 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        data = []
        text = AdminTask.generateSecConfigReport()
        for line in text.splitlines()[ 2: ] :
            data.append(
                [
                    info.strip() for info in
                    line[ :-2 ].split( ';' )
                ]
            )

        table =  JTable(
            reportTableModel(
                data, ';;;'.split( ';' ),
            ),
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        table.setDefaultRenderer( String, reportRenderer() )
        frame.add( JScrollPane( table ) )

        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( SecConfigReport_05() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f SecConfigReport_05.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
