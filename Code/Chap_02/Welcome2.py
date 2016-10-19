#-------------------------------------------------------------------------------
#    Name: Welcome2.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Demonstrate how to allow the close icon to terminate the script
#   Usage: wsadmin -f Welcome2.py
#            or
#          jython Welcome2.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from javax.swing import JFrame
win = JFrame( 'Welcome to Jython Swing' )
win.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )
win.size = ( 400, 100 )
win.show()
if 'AdminConfig' in dir() :
    raw_input( '\nPress <Enter> to terminate the application: ' )