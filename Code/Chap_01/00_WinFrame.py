#-------------------------------------------------------------------------------
#    Name: 00_WinFrame.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Demonstrate the creation of a trivial JWindow and JFrame objects
#    Note: Using Jython it is best to close the command prompt to exit
#   Usage: C:\IBM\WebSphere\AppServer\bin\wsadmin -f 00_WinFrame.py
#            or
#          C:\jython2.5.3\bin\jython 00_WinFrame.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/20  rag  0.0  New
#-------------------------------------------------------------------------------
import java.awt    as awt
import javax.swing as swing

w = swing.JWindow()
w.setSize( 200, 200 )
w.setLocation( 200, 200 )
w.setVisible( 1 )

f = swing.JFrame( 'JFrame' )
f.setSize( 200, 200 )
f.setLocation( 500, 200 )
f.setVisible( 1 )

if 'AdminConfig' in dir() :
    #---------------------------------------------------------------------------
    # If this script is executed using wsadmin, pressing <Enter> will exit it.
    # C:\IBM\WebSphere\AppServer\bin\wsadmin -f 00_WinFrame.py
    #---------------------------------------------------------------------------
    raw_input( '\nPress <Enter> to terminate the application:' )