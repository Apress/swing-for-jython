#-------------------------------------------------------------------------------
#    Name: GridBagLayout3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that positions application components
#          using a GridBagLayout layout manager to show a more complicated way
#          to position components within a pane.
#    Note: The buttons don't have an ActionListener event handler assigned.
#   Usage: wsadmin -f GridBagLayout3.py
#            or
#          jython GridBagLayout3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import Component
from   java.awt    import EventQueue
from   java.awt    import GridBagConstraints
from   java.awt    import GridBagLayout
from   javax.swing import BoxLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel

#-------------------------------------------------------------------------------
# Name: GridBagLayout3()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class GridBagLayout3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'GridBagLayout3',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.addComponents( frame.getContentPane() )

#       frame.pack()
#       print frame.getSize()
        frame.setSize( 410, 210 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addComponents()
    # Role: Add some buttons to the specified container using the GridBagLayout
    #       layout manager to control the size, and position of each button.
    #---------------------------------------------------------------------------
    def addComponents( self, container ) :
        container.setLayout( GridBagLayout() )

        names = '1,2,3 being the third number'.split( ',' )
        for col in range( len( names ) ) :
            c = GridBagConstraints()
            c.gridx = col    # gridx is the grid column
            c.gridy = col    # gridy is the grid row #
            container.add( JButton( names[ col ] ), c )

        c = GridBagConstraints()
        c.gridx = 1
        c.gridy = 3          # put on a new row
        c.ipady = 32         # make this one taller
        container.add( JButton( 'Four shalt thou not count' ), c )

        c = GridBagConstraints()
        c.gridx = 1          # middle column
        c.gridy = 4          # put on a new row
        c.gridwidth = 3      # make this one 3 columns wide
        container.add( JButton( 'Five is right out' ), c )

    #---------------------------------------------------------------------------
    # Name: buttonPress()
    # Role: Event handler
    #---------------------------------------------------------------------------
    def buttonPress( self, event ) :
        print event

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( GridBagLayout3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
