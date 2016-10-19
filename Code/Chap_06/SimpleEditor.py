#-------------------------------------------------------------------------------
#    Name: SimpleEditor.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that allow the user to enter/edit text
#    Note: The caretUpdate() method uses a "brute force" (inefficient) technique
#          that shouldn't be used for "large amounts" of data.
#   Usage: wsadmin -f SimpleEditor.py
#            or
#          jython SimpleEditor.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue

from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JTextArea
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: SimpleEditor()
# Role: Create, and display our simple application
#-------------------------------------------------------------------------------
class SimpleEditor( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Build and display our graphical application
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'Simple Editor',
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # The JTextArea will be used to hold the user entered text.
        #-----------------------------------------------------------------------
        self.area = JTextArea(
            rows = 8,
            columns = 32,
            caretUpdate = self.caretUpdate
        )
        frame.add( JScrollPane( self.area ), BorderLayout.CENTER )
        self.words = JLabel( '# words: 0  # lines: 0' )
        frame.add( self.words, BorderLayout.SOUTH )

        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: caretUpdate()
    # Role: Build and display our graphical application
    # Note: This is a brute force implementation, just to demonstrate some ideas
    #---------------------------------------------------------------------------
    def caretUpdate( self, event, regexp = None ) :
        if not regexp :
            regexp = re.compile( '\W+', re.MULTILINE )
        pos = event.getDot()
        text = self.area.getText()
        if text.strip() == '' :
            words = lines = 0
        else :
            words = len( re.split( regexp, text ) )
            lines = len( text.splitlines() )
        msg = '# words: %d  # lines: %d' % ( words, lines )
        self.words.setText( msg )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SimpleEditor() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
