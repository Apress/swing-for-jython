#-------------------------------------------------------------------------------
#    Name: KeyStrokes2.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython script showing JTable 'SPACE' KeyStrokes & the name of
#          each associated action.
#    Note: This is a "Swing" script only because it imports javax.swing JTable
#   Usage: wsadmin -f KeyStrokes2.py
#            or
#          jython KeyStrokes2.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from javax.swing import JTable

table = JTable()
keys  = [
            key
            for key in table.getRegisteredKeyStrokes()
        ]
print 'Number of JTable KeyStrokes:', len( keys )

width = max( [ len( str( key ) ) for key in keys ] )

print 'JTable "Space" Keys:'
for key in keys :
    if str( key ).endswith( 'SPACE' ) :
        cond = table.getConditionForKeyStroke( key )
        act  = table.getInputMap( cond ).get( key )
        print '%*s : %s' % ( width, str( key ), act )
