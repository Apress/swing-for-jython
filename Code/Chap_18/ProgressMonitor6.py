#-------------------------------------------------------------------------------
#    Name: ProgressMonitor6.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script shows how a ProgressMonitor might be used
#    Note: 
#   Usage: wsadmin -f ProgressMonitor6.py
#            or
#          jython ProgressMonitor6.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   time        import sleep

from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import Insets

from   java.util   import Random

from   javax.swing import BorderFactory
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JPanel
from   javax.swing import ProgressMonitor
from   javax.swing import SwingWorker

#-------------------------------------------------------------------------------
# Name: progressTask
# Role: Background processing of task that takes a long time...
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class progressTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, changeHandler = None ) :
        if changeHandler :
            SwingWorker.__init__(
                self,
                propertyChange = changeHandler
            )
        else :
            SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Use a (pseudo) random number generator to simulate progress
        #-----------------------------------------------------------------------
        try :
            random   = Random()
            progress = 0
            self.super__setProgress( progress )
            # Simulated startup time
            sleep( ( random.nextInt( 1400 ) + 100 ) / 1000.0 )
            while progress < 100 :
                sleep( ( random.nextInt( 1400 ) + 100 ) / 1000.0 )
                progress = min(
                    progress + random.nextInt( 10 ) + 1, 100
                )
                self.super__setProgress( progress )
        except KeyboardInterrupt, ki :
            pass
        except :
            Type, value = sys.exc_info()[ :2 ]
            print 'Error:', str( Type )
            print 'value:', str( value )
            sys.exit()

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        pass

#-------------------------------------------------------------------------------
# Name: ProgressMonitor6()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ProgressMonitor6( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'ProgressMonitor',
            size = ( 280, 125 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.getContentPane().setBorder(
            BorderFactory.createEmptyBorder( 20, 20, 20, 20 )
        )

        panel = JPanel()
        self.button = panel.add(
            JButton(
                'Start',
                actionPerformed = self.start
            )
        )
        frame.add(
            panel,
            BorderLayout.NORTH
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: start()
    # Role: ActionListener event handler for "start" button
    #---------------------------------------------------------------------------
    def start( self, event ) :
        self.button.setEnabled( 0 )
        self.PM = ProgressMonitor(
            self.frame,      # parentComponent
            'Message text',  # message (Object)
            ' ',             # note (String)
            0,               # minimum value
            100              # maximum value
        )
        self.task = progressTask( self.propertyUpdate )
        self.task.execute()

    #---------------------------------------------------------------------------
    # Name: propertyUpdate()
    # Role: PropertyChangeListener event handler for progressTask instance
    #---------------------------------------------------------------------------
    def propertyUpdate( self, event ) :
        PM, task = self.PM, self.task
        if event.getPropertyName() == 'progress' :
            progress = event.getNewValue()  # integer % complete
            lo, hi   = PM.getMinimum(), PM.getMaximum()
            here     = int( ( hi - lo ) * 0.01 * progress ) + lo
#           print '%3d%% of %3d..%3d = %3d' % ( progress, lo, hi, here )
            PM.setProgress( here )
            PM.setNote( '%d%% Complete' % progress )
            done = task.isDone()
            if PM.isCanceled() or done :
                if not done :
                    task.cancel( 1 )
                self.button.setEnabled( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ProgressMonitor6() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
