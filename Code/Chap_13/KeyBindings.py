#-------------------------------------------------------------------------------
#    Name: KeyBindings.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing JTable KeyBinding & mappings as a
#          table
#    Note: 
#   Usage: wsadmin -f KeyBindings.py
#            or
#          jython KeyBindings.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Point
from   java.awt    import Toolkit

from   java.lang   import String

from   javax.swing import JComponent
from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JScrollPane
from   javax.swing import JTextField

from   java.text   import DateFormat

from   java.util   import Date

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: setColumnWidths()
# Role: Compute, and set the preferred column widths and viewport size
#-------------------------------------------------------------------------------
def setColumnWidths( table ) :
    #---------------------------------------------------------------------------
    # It's possible for this table to not have a header...
    #---------------------------------------------------------------------------
    header = table.getTableHeader()
    if header :
        hRenderer = header.getDefaultRenderer()
    else :
        hRenderer = None

    #---------------------------------------------------------------------------
    # Variables used to access the table properties and data
    #---------------------------------------------------------------------------
    tcm    = table.getColumnModel()         # Table Column Model
    data   = table.getModel()               # To access table data
    margin = tcm.getColumnMargin()          # gap between columns

    #---------------------------------------------------------------------------
    # For each column, determine the maximum width required
    #---------------------------------------------------------------------------
    rows = data.getRowCount()               # Number of rows
    cols = tcm.getColumnCount()             # Number of cols

    #---------------------------------------------------------------------------
    # Used for parse & format date strings & objects
    #---------------------------------------------------------------------------
    df   = DateFormat.getDateInstance( DateFormat.MEDIUM )

    tWidth = 0                              # Table width
    for i in range( cols ) :                # For col 0..N
        col = tcm.getColumn( i )            # TableColumn: col i
        idx = col.getModelIndex()           # model index: col i

        #-----------------------------------------------------------------------
        # To determine the preferred column width, we
        # must use the current renderer for this column
        #-----------------------------------------------------------------------
        render = col.getHeaderRenderer()    # header renderer,
        if not render :                     #   
            render = hRenderer              #   or a default

        #-----------------------------------------------------------------------
        # Get preferred header width for column i
        #-----------------------------------------------------------------------
        if render :
            comp = render.getTableCellRendererComponent(
                table,
                col.getHeaderValue(),
                0,
                0,
                -1,
                i
            )
            cWidth = comp.getPreferredSize().width
        else :
            cWidth = -1
        #-----------------------------------------------------------------------
        # Compute the maximum width required for the data values in this column
        #-----------------------------------------------------------------------
        Type = data.getColumnClass( i )          # dataType: col i
        for row in range( rows ) :
            v = data.getValueAt( row, idx )      # value
            if Type == Date :
                val = df.format( v )             # formatted date
                r = table.getDefaultRenderer( String )
            else :
                val = Type( v )
                r = table.getCellRenderer( row, i )
            comp = r.getTableCellRendererComponent(
                table,
                val,                             # formatted value
                0,                               # not selected
                0,                               # not in focus
                row,                             # row num
                i                                # col num
            )
            cWidth = max( cWidth, comp.getPreferredSize().width )

        if cWidth > 0 :
            col.setPreferredWidth( cWidth + margin )

        #-----------------------------------------------------------------------
        # Table width = sum of column widths
        #-----------------------------------------------------------------------
        tWidth += col.getPreferredWidth()

    #---------------------------------------------------------------------------
    # Set the preferred viewport size so we don't (initially) see scrollbars
    # Note: This assumes a uniform row height for every row
    #---------------------------------------------------------------------------
    table.setPreferredScrollableViewportSize(
        Dimension(
            tWidth,
            rows * table.getRowHeight()
        )
    )

#-------------------------------------------------------------------------------
# Name: myTM()
# Role: Cells are read-only Strings
#-------------------------------------------------------------------------------
class myTM( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return String

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: read-only table model
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return 0

#-------------------------------------------------------------------------------
# Name: KeyBindings()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class KeyBindings( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: data()
    # Role: Build the table of key bindings to action names
    #---------------------------------------------------------------------------
    def data( self ) :
        table  = JTable()    # use an empty (default) table
        iMap   = table.getInputMap(
            JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT
        )
        # List of mapped keystrokes & actions
        keystrokes = [
            ( key, iMap.get( key ) )
            for key in table.getRegisteredKeyStrokes()
        ]
        #------------------------------------------------------
        # Dict of key names & modified keystrokes
        #------------------------------------------------------
        keys = {}       # Dict, index = key name  -> modifiers
        acts = {}       # Dict, index = keyStroke -> actionName
        for key, act in keystrokes :
            val = str( key )      # e.g., shift ctrl pressed TAB
            acts[ val ] = act     # e.g., selectNextColumnCell
            pos = val.rfind( ' ' )
            prefix, name = val[ :pos ], val[ pos + 1: ]
            if keys.has_key( name ) :
                keys[ name ].append( prefix )
            else :
                keys[ name ] = [ prefix ]
        #------------------------------------------------------
        # The list of unique key names, in alphabetical order
        #------------------------------------------------------
        names = keys.keys()
        names.sort()
        prefixes = [
            'pressed',            # unmodified keystroke
            'ctrl pressed',       # Ctrl-<keystroke>
            'shift pressed',      # Shift-<keystroke>
            'shift ctrl pressed'  # Shift-Ctrl-<keystroke>
        ]
        #------------------------------------------------------
        # For each key name (in alphabetical order)
        #------------------------------------------------------
        result = []               # The 2D table of strings
        for name in names :       # For each key name (e.g., TAB)
            here = [ name ]       # Current table row
            #
            # columns are in a fixed order, based upon prefix
            #
            for prefix in prefixes :
                kName = ' '.join( [ prefix, name ] )
                here.append( acts.get( kName, '' ) )
            result.append( here )
        return result

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'KeyBindings',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        headings = (
            'KeyStroke,Unmodified,Ctrl,Shift,Shift-Ctrl'
        ).split( ',' )
        table = JTable(
            myTM( self.data(), headings ),
            columnSelectionAllowed = 1
        )
        table.setAutoResizeMode( JTable.AUTO_RESIZE_OFF )
        setColumnWidths( table )        
        frame.add( JScrollPane( table ) )
        frame.pack()
        size = frame.getSize()
        loc  = frame.getLocation()
        frame.setLocation(
            Point(
                loc.x - ( size.width  >> 1 ),
                loc.y - ( size.height >> 1 )
            )
        )

        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( KeyBindings() )
    if 'AdminConfig' in dir() :
        if sys.version.startswith( '2.1' ) :
            msg = '\nPress <Enter> to terminate this application: '
        else :
            msg = ''
        raw_input( msg )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
