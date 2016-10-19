#-------------------------------------------------------------------------------
#    Name: List3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that counts the number of occurrences of
#          the user specified word.
#   Usage: wsadmin -f List3.py
#            or
#          jython List3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import BorderLayout
from   java.awt    import GridLayout
from   java.awt    import EventQueue
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JList
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: List3()
# Role: Create, and display our application window
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class List3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create and display the application window
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'List3',
            size = ( 200, 200 ),
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        data = (
            'Now is the time for all good spam ' +
            'to come to the aid of their eggs'
        ).split( ' ' )
        self.info = JList( data )
        frame.add(
            JScrollPane(
                self.info,
                preferredSize = ( 200, 110 )
            ),
            BorderLayout.NORTH
        )
        panel = JPanel( layout = GridLayout( 0, 2 ) )
        panel.add(
            JButton(
                'Count',
                actionPerformed = self.count
            )
        )
        self.text = panel.add( JTextField( 10 ) )
        frame.add( panel, BorderLayout.CENTER )
        self.msg  = JLabel( 'Occurance count' )
        frame.add( self.msg, BorderLayout.SOUTH )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: count()
    # Role: Retrieve the "word" from the input field, and count the number of
    #       times it occurs in the list
    #---------------------------------------------------------------------------
    def count( self, event ) :
        word = self.text.getText()
        model = self.info.getModel()
        occurs = 0
        for index in range( model.getSize() ) :
            if model.getElementAt( index ) == word :
                occurs += 1
        self.msg.setText(
            '"%s" occurs %d time(s)' %
           ( word, occurs )
        )
        self.text.setText( '' )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( List3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
