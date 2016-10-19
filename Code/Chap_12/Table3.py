#-------------------------------------------------------------------------------
#    Name: Table3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing a JTable instance
#    Note: Shows how to make the Table read-only using the roTM class
#   Usage: wsadmin -f Table3.py
#            or
#          jython Table3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import ListSelectionModel
from   javax.swing import JScrollPane
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: roTM()
# Role: Provide a read-only table model class
#-------------------------------------------------------------------------------
class roTM( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self, data, headings ) :
        DefaultTableModel.__init__( self, data, headings )

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Return 0 (false) to indicate that no cell is editable
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return 0

#-------------------------------------------------------------------------------
# Name: Table3()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Table3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        info = r'''
08/22/2011|   726|C:\IBM\WebSphere\scripts\Swing\ListPort.py
07/29/2011|   826|C:\IBM\WebSphere\AppServer80\bin\listports.00.py
05/18/2011| 1,822|C:\IBM\WebSphere\AppServer60\scripts\ListPorts.py
01/17/2011| 5,915|C:\IBM\WebSphere\scripts\Swing\SwingPorts\ListPorts.0.3.py
10/19/2010| 3,415|C:\IBM\WebSphere\AppServer70\bin\ListPorts.py
05/12/2010| 2,535|C:\IBM\WebSphere\scripts\new\ListPorts.py
04/09/2010|   914|C:\IBM\WebSphere\scripts\ListPort locations.txt
09/01/2009| 1,758|C:\IBM\WebSphere\AppServer\scripts\ListPorts.py
06/23/2009| 1,715|C:\IBM\WebSphere\scripts\ListPorts.py
12/12/2008| 2,195|C:\IBM\WebSphere\scripts\Chap 08 - Intro to Admin Objects\ListPorts.py
10/09/2008| 2,440|C:\IBM\WebSphere\scripts\Chap 09 - AdminConfig\ListPorts.py
05/03/2008| 1,697|C:\IBM\WebSphere\AppServer70\scripts\ListPorts.py
05/03/2008| 1,680|C:\IBM\WebSphere\scripts\archive\ListPorts.05.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts\archive\ListPorts.06.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts\archive\ListPorts.07.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts.70.new\ListPorts.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts.70.old\ListPorts.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts.old\ListPorts.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts.old\ListPorts.py.txt
05/03/2008| 1,680|C:\IBM\WebSphere\scripts.old\archive\ListPorts.05.py
05/03/2008| 1,697|C:\IBM\WebSphere\scripts.old\archive\ListPorts.06.py
05/01/2008| 1,034|C:\IBM\WebSphere\scripts\archive\ListPorts.02.py
05/01/2008| 1,514|C:\IBM\WebSphere\scripts\archive\ListPorts.03.py
05/01/2008| 1,655|C:\IBM\WebSphere\scripts\archive\ListPorts.04.py
05/01/2008| 1,034|C:\IBM\WebSphere\scripts.old\archive\ListPorts.02.py
05/01/2008| 1,514|C:\IBM\WebSphere\scripts.old\archive\ListPorts.03.py
05/01/2008| 1,655|C:\IBM\WebSphere\scripts.old\archive\ListPorts.04.py
04/30/2008| 2,332|C:\IBM\WebSphere\scripts\archive\ListPorts.01.py
04/30/2008| 2,332|C:\IBM\WebSphere\scripts.old\archive\ListPorts.01.py
04/23/2008|   828|C:\IBM\WebSphere\V7 Notes\listports.00.py
04/23/2008|   506|C:\IBM\WebSphere\V7 Notes\listports.py
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
            'Table3',
            size = ( 300, 200 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        headings = 'Date,size,Location'.split( ',' )
        frame.add(
            JScrollPane(
                JTable(
                    roTM( self.data, headings ),
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
    EventQueue.invokeLater( Table3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
