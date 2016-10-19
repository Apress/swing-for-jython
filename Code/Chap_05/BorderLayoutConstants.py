#-------------------------------------------------------------------------------
#    Name: BorderLayoutConstants.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: <purpose served by this script>
#    Note: <Any important limitations or restrictions> [Optional]
#   Usage: wsadmin -f BorderLayoutConstants.py
#            or
#          jython BorderLayoutConstants.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from java.awt import BorderLayout

width = max( [ len( name ) for name in dir( BorderLayout ) ] )

values = {}

for name in dir( BorderLayout ) :
    if name == name.upper() :
        value = eval( 'BorderLayout.%s' % name )
        if values.has_key( value ) :
            values[ value ].append( name )
        else :
            values[ value ] = [ name ]

names = values.keys()
names.sort()

name_width = max( [ len( name ) for name in names ] )
for name in names :
    print '%*s :' % ( -name_width, name ),
    values[ name ].sort()
    print ', '.join( values[ name ] )
