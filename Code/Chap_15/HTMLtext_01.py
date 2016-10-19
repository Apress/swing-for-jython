#-------------------------------------------------------------------------------
#    Name: HTMLtext_01.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to display HTML in a JLabel field
#    Note: The Swing Event Dispatch thread is not used
#   Usage: wsadmin -f HTMLtext_01.py
#            or
#          jython HTMLtext_01.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

from javax.swing import JFrame
from javax.swing import JLabel

frame = JFrame(
            'HTMLtext_01',
            size = ( 200, 200 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
text  = '<html>'
text += '<sup>My</sup> '
text += '<sub><i>Label</i></sub> '
text += '<font color="#FF0000">is</font> '
text += '<font color="#00FF00"><b>far</b></font> '
text += '<font color="#0000FF">too busy,</font> '
text += "<u>isn't it?</u>"
label = frame.add( JLabel( text ) )
frame.setVisible( 1 )
raw_input()