#-------------------------------------------------------------------------------
#    Name: 01_WFD.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple script to display a JWindow, a JFrame & a JDialog.
#          Class setter methods are used for each modification.
#          This technique most closely matches what is done in Java.
#    Note: Using Jython it is best to close the command prompt to exit
#   Usage: C:\IBM\WebSphere\AppServer\bin\wsadmin -f 01_WFD.py
#            or
#          C:\jython2.5.3\bin\jython 01_WFD.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/20  rag  0.0  New
#-------------------------------------------------------------------------------
import javax.swing as swing

w = swing.JWindow()
w.setSize( 200, 200 )
w.setLocation( 200, 200 )
w.setVisible( 1 )

f = swing.JFrame( 'JFrame' )
f.setSize( 200, 200 )
f.setLocation( 450, 200 )
f.setVisible( 1 )

d = swing.JDialog()
d.setSize( 200, 200 )
d.setLocation( 700, 200 )
d.setVisible( 1 )

if 'AdminConfig' in dir() :
    #---------------------------------------------------------------------------
    # If executed using wsadmin, pressing <Enter> will terminate the script
    # C:\IBM\WebSphere\AppServer\bin\wsadmin -f 01_WinFrame.py
    #---------------------------------------------------------------------------
    raw_input( '\nPress <Enter> to terminate the application:' )