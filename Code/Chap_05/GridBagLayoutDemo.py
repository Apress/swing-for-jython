#-------------------------------------------------------------------------------
#    Name: GridBagLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that positions application components
#          using a GridBagLayout layout manager to show a more complicated way
#          to position components within a pane.
#    Note: The buttons don't have an ActionListener event handler assigned.
#   Usage: wsadmin -f GridBagLayoutDemo.py
#            or
#          jython GridBagLayoutDemo.py
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
# Name: GridBagLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class GridBagLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'GridBagLayoutDemo',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.addComponents( frame.getContentPane() )

        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addComponents()
    # Role: Add some buttons to the specified container using the GridBagLayout
    #       layout manager to control the size, and position of each button.
    #---------------------------------------------------------------------------
    def addComponents( self, container ) :
        container.setLayout( GridBagLayout() )
        c = GridBagConstraints()       # Start with the default constraints

        print '\n default constraints:'
        print '     gridx:', c.gridx
        print '     gridy:', c.gridx
        print ' gridwidth:', c.gridwidth
        print 'gridheight:', c.gridheight
        print '   weightx:', c.weightx
        print '   weighty:', c.weighty
        print '    anchor:', c.anchor
        print '      fill:', c.fill
        print '    insets:', c.insets
        print '     ipadx:', c.ipadx
        print '     ipady:', c.ipady

        for name in '1,2,3 being the third number'.split( ',' ) :
            container.add( JButton( name ) )

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
    EventQueue.invokeLater( GridBagLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
