#-------------------------------------------------------------------------------
#    Name: CardLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample / example wsadmin Jython script that positions application
#          components using a CardLayout layout manager
#    Note: Only the numbered buttons have an ActionListener event handler
#          assigned
#   Usage: wsadmin -f CardLayoutDemo.py
#            or
#          jython CardLayoutDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import BorderLayout
from   java.awt    import CardLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel

#-------------------------------------------------------------------------------
# Name: CardLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class CardLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'CardLayout',
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        cp = frame.getContentPane()
        self.addButtons( cp, BorderLayout.NORTH )
        self.addCards( cp, BorderLayout.CENTER )

        frame.setSize( 300, 125 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addButtons()
    # Role: Add some buttons to the specified container
    #---------------------------------------------------------------------------
    def addButtons( self, container, position ) :
        panel = JPanel()
        for name in '1,2,3'.split( ',' ) :
            panel.add(
                JButton(
                    name,
                    actionPerformed = self.buttonPress
                )
            )
        container.add( panel, position )

    #---------------------------------------------------------------------------
    # Name: addCards()
    # Role: Add some ...
    #---------------------------------------------------------------------------
    def addCards( self, container, position ) :
        card1 = JPanel()
        card1.add(
            JLabel(
                'The quick brown fox jumped over the lazy dog.'
            )
        )

        card2 = JPanel()
        for name in 'A,B,C'.split( ',' ) :
            card2.add( JButton( name ) )

        card3 = JPanel()
        card3.add(
            JLabel(
                'Now is the time for all good men to come to...'
            )
        )

        # Using a local reference to the panel simplifies the code
        cards = self.cards = JPanel( CardLayout() )
        cards.add( card1, '1' )
        cards.add( card2, '2' )
        cards.add( card3, '3' )

        container.add( cards, position )

    #---------------------------------------------------------------------------
    # Name: buttonPress()
    # Role: Action Listener event handler 
    #---------------------------------------------------------------------------
    def buttonPress( self, event ) :
        deck = self.cards.getLayout()
        deck.show( self.cards, event.getActionCommand() )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( CardLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
