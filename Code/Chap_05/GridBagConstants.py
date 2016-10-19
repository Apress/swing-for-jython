#-------------------------------------------------------------------------------
#    Name: GridBagConstraints.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Note: This is not a Swing application, it just displays the actual constant
#          values.
#   Usage: wsadmin -f Box1.py
#            or
#          jython Box1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

from java.awt import GridBagConstraints

const = {
          'ABOVE_BASELINE'          : GridBagConstraints.ABOVE_BASELINE,
          'ABOVE_BASELINE_LEADING'  : GridBagConstraints.ABOVE_BASELINE_LEADING,
          'ABOVE_BASELINE_TRAILING' : GridBagConstraints.ABOVE_BASELINE_TRAILING,
          'BASELINE'                : GridBagConstraints.BASELINE,
          'BASELINE_LEADING'        : GridBagConstraints.BASELINE_LEADING,
          'BASELINE_TRAILING'       : GridBagConstraints.BASELINE_TRAILING,
          'BELOW_BASELINE'          : GridBagConstraints.BELOW_BASELINE,
          'BELOW_BASELINE_LEADING'  : GridBagConstraints.BELOW_BASELINE_LEADING,
          'BELOW_BASELINE_TRAILING' : GridBagConstraints.BELOW_BASELINE_TRAILING,
          'BOTH'                    : GridBagConstraints.BOTH,
          'CENTER'                  : GridBagConstraints.CENTER,
          'EAST'                    : GridBagConstraints.EAST,
          'FIRST_LINE_END'          : GridBagConstraints.FIRST_LINE_END,
          'FIRST_LINE_START'        : GridBagConstraints.FIRST_LINE_START,
          'HORIZONTAL'              : GridBagConstraints.HORIZONTAL,
          'LAST_LINE_END'           : GridBagConstraints.LAST_LINE_END,
          'LAST_LINE_START'         : GridBagConstraints.LAST_LINE_START,
          'LINE_END'                : GridBagConstraints.LINE_END,
          'LINE_START'              : GridBagConstraints.LINE_START,
          'NONE'                    : GridBagConstraints.NONE,
          'NORTH'                   : GridBagConstraints.NORTH,
          'NORTHEAST'               : GridBagConstraints.NORTHEAST,
          'NORTHWEST'               : GridBagConstraints.NORTHWEST,
          'PAGE_END'                : GridBagConstraints.PAGE_END,
          'PAGE_START'              : GridBagConstraints.PAGE_START,
          'RELATIVE'                : GridBagConstraints.RELATIVE,
          'REMAINDER'               : GridBagConstraints.REMAINDER,
          'SOUTH'                   : GridBagConstraints.SOUTH,
          'SOUTHEAST'               : GridBagConstraints.SOUTHEAST,
          'SOUTHWEST'               : GridBagConstraints.SOUTHWEST,
          'VERTICAL'                : GridBagConstraints.VERTICAL,
          'WEST'                    : GridBagConstraints.WEST
}
result = {}
for n, v in const.items() :
    if result.has_key( v ) :
        result[ v ].append( n )
    else :
        result[ v ] = [ n ]

names = result.keys()
names.sort()

for name in names :
    print '%4d : %s' % ( name, ', '.join( result[ name ] ) )
