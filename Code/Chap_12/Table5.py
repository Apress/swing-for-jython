#-------------------------------------------------------------------------------
#    Name: Table5.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing various table cell renderers
#   Usage: wsadmin -f Table5.py
#            or
#          jython Table5.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.lang   import Boolean
from   java.lang   import Float
from   java.lang   import Double
from   java.lang   import Integer
from   java.util   import Date
from   java.text   import DateFormat
from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import ListSelectionModel
from   javax.swing import JScrollPane
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: myTM()
# Role: Personalize the table model to provide appropriate column data types
#-------------------------------------------------------------------------------
class myTM( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self, data, headings ) :
        info = []
        df   = DateFormat.getDateInstance( DateFormat.SHORT )
        for tf, date, size, f, d in data :
            info.append(
                [
                    Boolean( tf == '1' ),
                    df.parse( date ),
                    Integer( size.strip().replace( ',', '' ) ),
                    Float( f ),
                    Double( d )
                ]
            )
        DefaultTableModel.__init__( self, info, headings )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return [ Boolean, Date, Integer, Float, Double ][ col ]

#-------------------------------------------------------------------------------
# Name: Table5()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Table5( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        info = r'''
1|08/22/2011|   726| 0.0| 3.14159
0|05/12/2010| 2,535| 1.1| 6.28318
1|06/23/2009| 1,715| 2.2| 9.42477
0|05/03/2008| 1,697| 3.3|12.56636
1|04/23/2008|   506| 4.4|15.70795
'''
        self.data = [                       # list comprehension
            line.split( '|' )               # each row is an array
            for line in info.splitlines()   # each line is a row
            if line                         # ignore blank lines
        ]

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Table5',
            size = ( 300, 150 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        headings = 'T/F,Date,Integer,Float,Double'.split( ',' )
        frame.add(
            JScrollPane(
                JTable(
                    myTM( self.data, headings ),
                    selectionMode = ListSelectionModel.SINGLE_SELECTION
                )
            )
        )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Table5() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
