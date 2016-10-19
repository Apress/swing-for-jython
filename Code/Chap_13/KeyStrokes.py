#-------------------------------------------------------------------------------
#    Name: KeyStrokes.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing JTable 'SPACE' KeyStrokes
#    Note: This is a "Swing" script only because it imports javax.swing JTable
#   Usage: wsadmin -f KeyStrokes.py
#            or
#          jython KeyStrokes.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from javax.swing import JTable

table = JTable()
keys  = [
            str( key )
            for key in table.getRegisteredKeyStrokes()
        ]
print 'Number of JTable KeyStrokes:', len( keys )

width = max( [ len( key ) for key in keys ] )

print 'JTable "Space" Keys:'
print '\n'.join(
                   [
                       '%*s' % ( width, key )
                       for key in keys if key.endswith( 'SPACE' )
                   ]
               )