#-------------------------------------------------------------------------------
#    Name: desc.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to verify a Regular Expression (RegExp)
#          for identifying the scripting object methods within the help text
#          for each of the original scripting objects.
#    Note: This requires a WebSphere Application Server environment.
#          Since the AdminTask scripting object is a framework, its help text
#          must be handled in a different manner
#   Usage: wsadmin -f desc.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/03  rag  0.0  New - ...
#-------------------------------------------------------------------------------
import re

pat = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )

objs = [
     ( 'Help'        , Help         ),
     ( 'AdminApp'    , AdminApp     ),
     ( 'AdminConfig' , AdminConfig  ),
     ( 'AdminControl', AdminControl )
]

print '    Object   | #Lines | 1st method'
print '-------------+--------+--------------------'
for name, obj in objs :
    text = obj.help()
    mo = re.search( pat, text )
    desc = text[ :mo.start( 1 ) ].strip().splitlines()
    method = text[ mo.start( 1 ) : mo.end( 1 ) ]
    print '%-12s | %6d | %s' % ( name, len( desc ), method )
