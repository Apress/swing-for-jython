#-------------------------------------------------------------------------------
# Copyright (c) 1995, 2008, Oracle and/or its affiliates. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   - Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#   - Neither the name of Oracle or the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#    Name: GlassPaneDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Translation of the GlassPaneDemo.java from Oracle Swing Tutorials
#   Usage: wsadmin -f GlassPaneDemo.py
#            or
#          jython GlassPaneDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
# http://docs.oracle.com/javase/tutorial/uiswing/examples/components/...
#        GlassPaneDemoProject/src/components/GlassPaneDemo.java
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt          import Color
from   java.awt          import FlowLayout
from   java.awt          import EventQueue

from   java.awt.event    import ItemEvent
from   java.awt.event    import ItemListener
from   java.awt.event    import MouseEvent

from   javax.swing       import JButton
from   javax.swing       import JCheckBox
from   javax.swing       import JComponent
from   javax.swing       import JFrame
from   javax.swing       import JMenu
from   javax.swing       import JMenuBar
from   javax.swing       import JMenuItem
from   javax.swing       import SwingUtilities

from   javax.swing.event import MouseInputAdapter

#-------------------------------------------------------------------------------
# Name: GlassPaneDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#       that includes the use of the GlassPane and how it may be used.
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class GlassPaneDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        #-----------------------------------------------------------------------
        # Create and set up the window.
        #-----------------------------------------------------------------------
        frame = JFrame( 'GlassPaneDemo' )
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )

        #-----------------------------------------------------------------------
        # Start creating and adding components.
        #-----------------------------------------------------------------------
        changeButton = JCheckBox( 'Glass pane "visible"' )
        changeButton.setSelected( 0 )
        
        #-----------------------------------------------------------------------
        # Set up the content pane, where the 'main GUI' lives.
        #-----------------------------------------------------------------------
        contentPane = frame.getContentPane()
        contentPane.setLayout( FlowLayout() )
        contentPane.add( changeButton )
        contentPane.add( JButton( 'Button 1' ) )
        contentPane.add( JButton( 'Button 2' ) )

        #-----------------------------------------------------------------------
        # Set up the menu bar, which appears above the content pane.
        #-----------------------------------------------------------------------
        menuBar = JMenuBar()
        menu    = JMenu( 'Menu' )
        menu.add( JMenuItem( 'Do nothing' ) )
        menuBar.add( menu )
        frame.setJMenuBar( menuBar )

        #-----------------------------------------------------------------------
        # Set up the glass pane, which appears over both menu bar and
        # content pane and is an item listener on the change button
        #-----------------------------------------------------------------------
        myGlassPane = MyGlassPane( changeButton, menuBar, contentPane )
        changeButton.addItemListener( myGlassPane )
        frame.setGlassPane( myGlassPane )

        #-----------------------------------------------------------------------
        # Resize the frame to display the visible components contain therein,
        # and have the frame (application) make itself visisble.
        #-----------------------------------------------------------------------
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
# Name: CBListener()
# Role: Listen for CheckBox events in which our application is interested.
#       Redispatch them to the check box.
#-------------------------------------------------------------------------------
class CBListener ( MouseInputAdapter ) :

    def __init__( self, liveButton, menuBar, glassPane, contentPane ) :
        self.liveButton  = liveButton
        self.menuBar     = menuBar
        self.glassPane   = glassPane
        self.contentPane = contentPane

    def mouseMoved( self, e )    : self.redispatchMouseEvent( e, 0 )

    def mouseDragged( self, e )  : self.redispatchMouseEvent( e, 0 )

    def mouseClicked( self, e )  : self.redispatchMouseEvent( e, 0 )

    def mouseEntered( self, e )  : self.redispatchMouseEvent( e, 0 )

    def mouseExited( self, e )   : self.redispatchMouseEvent( e, 0 )

    def mousePressed( self, e )  : self.redispatchMouseEvent( e, 0 )

    def mouseReleased( self, e ) : self.redispatchMouseEvent( e, 1 )

    # A basic implementation of redispatching events.
    def redispatchMouseEvent( self, e, repaint) :
        glassPanePoint = e.getPoint()
        container      = self.contentPane
        containerPoint = SwingUtilities.convertPoint(
                                                      self.glassPane,
                                                      glassPanePoint,
                                                      self.contentPane
                                                    )

        if containerPoint.y < 0  :     # we're not in the content pane
            if ( containerPoint.y + self.menuBar.getHeight() >= 0 ) :
                # The mouse event is over the menu bar. Could handle specially.
                pass
            else :
                #---------------------------------------------------------------
                # The mouse event is over non-system window decorations, e.g.,
                # the ones provided by the Java look and feel.
                # Could handle specially.
                #---------------------------------------------------------------
                pass
        else :
            # The mouse event is probably over the content pane.
            # Find out exactly which component it's over.  
            component = SwingUtilities.getDeepestComponentAt(
                                                              container,
                                                              containerPoint.x,
                                                              containerPoint.y
                                                            )
                            
            if component and component == self.liveButton :
                # Forward events over the check box.
                componentPoint = SwingUtilities.convertPoint(
                                                              self.glassPane,
                                                              glassPanePoint,
                                                              component
                                                            )
                component.dispatchEvent( MouseEvent( component,
                                                     e.getID(),
                                                     e.getWhen(),
                                                     e.getModifiers(),
                                                     componentPoint.x,
                                                     componentPoint.y,
                                                     e.getClickCount(),
                                                     e.isPopupTrigger()
                                                    )
                                        )
        
        # Update the glass pane if requested.
        if repaint :
            self.glassPane.setPoint( glassPanePoint )
            self.glassPane.repaint()

#-------------------------------------------------------------------------------
# Name: MyGlassPane()
# Role: Provide our own glass pane so that it can paint.
#-------------------------------------------------------------------------------
class MyGlassPane ( JComponent, ItemListener ) :

    # React to change button clicks.
    def itemStateChanged( self, e ) :
        self.setVisible( e.getStateChange() == ItemEvent.SELECTED )

    def paintComponent( self, g ) :
        if self.point :
            g.setColor( Color.red )
            g.fillOval( self.point.x - 10, self.point.y - 10, 20, 20 )

    def setPoint( self, p ) :
        self.point = p

    def __init__( self, aButton, menuBar, contentPane ) :
        self.point = None
        listener   = CBListener( aButton, menuBar, self, contentPane )
        self.addMouseListener( listener )
        self.addMouseMotionListener( listener )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( GlassPaneDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application: ' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()