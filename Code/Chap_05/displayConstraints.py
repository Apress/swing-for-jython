#-------------------------------------------------------------------------------
#    Name: displayConstraints.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Utility routine to display non-default GridBagConstraints for the
#          specified object
#    Note: See Figure 5-21 for an example of how this might be used
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from java.awt import GridBagConstraints

def displayConstraints( c, default = None, const = None ) :
    if default == None :
        default = GridBagConstraints()
    if const == None :
        const = {
            GridBagConstraints.ABOVE_BASELINE          : 'ABOVE_BASELINE',
            GridBagConstraints.ABOVE_BASELINE_LEADING  : 'ABOVE_BASELINE_LEADING',
            GridBagConstraints.ABOVE_BASELINE_TRAILING : 'ABOVE_BASELINE_TRAILING',
            GridBagConstraints.BASELINE                : 'BASELINE',
            GridBagConstraints.BASELINE_LEADING        : 'BASELINE_LEADING',
            GridBagConstraints.BASELINE_TRAILING       : 'BASELINE_TRAILING',
            GridBagConstraints.BELOW_BASELINE          : 'BELOW_BASELINE',
            GridBagConstraints.BELOW_BASELINE_LEADING  : 'BELOW_BASELINE_LEADING',
            GridBagConstraints.BELOW_BASELINE_TRAILING : 'BELOW_BASELINE_TRAILING',
            GridBagConstraints.BOTH                    : 'BOTH',
            GridBagConstraints.CENTER                  : 'CENTER',
            GridBagConstraints.EAST                    : 'EAST',
            GridBagConstraints.FIRST_LINE_END          : 'FIRST_LINE_END',
            GridBagConstraints.FIRST_LINE_START        : 'FIRST_LINE_START',
            GridBagConstraints.HORIZONTAL              : 'HORIZONTAL',
            GridBagConstraints.LAST_LINE_END           : 'LAST_LINE_END',
            GridBagConstraints.LAST_LINE_START         : 'LAST_LINE_START',
            GridBagConstraints.LINE_END                : 'LINE_END',
            GridBagConstraints.LINE_START              : 'LINE_START',
            GridBagConstraints.NONE                    : 'NONE',
            GridBagConstraints.NORTH                   : 'NORTH',
            GridBagConstraints.NORTHEAST               : 'NORTHEAST',
            GridBagConstraints.NORTHWEST               : 'NORTHWEST',
            GridBagConstraints.PAGE_END                : 'PAGE_END',
            GridBagConstraints.PAGE_START              : 'PAGE_START',
            GridBagConstraints.RELATIVE                : 'RELATIVE',
            GridBagConstraints.REMAINDER               : 'REMAINDER',
            GridBagConstraints.SOUTH                   : 'SOUTH',
            GridBagConstraints.SOUTHEAST               : 'SOUTHEAST',
            GridBagConstraints.SOUTHWEST               : 'SOUTHWEST',
            GridBagConstraints.VERTICAL                : 'VERTICAL',
            GridBagConstraints.WEST                    : 'WEST' 
        }
    results = []
    if c.gridx      != default.gridx      : results.append( '     gridx: %d' % c.gridx         )
    if c.gridy      != default.gridy      : results.append( '     gridy: %d' % c.gridy         )
    if c.gridwidth  != default.gridwidth  : results.append( ' gridwidth: %d' % c.gridwidth     )
    if c.gridheight != default.gridheight : results.append( 'gridheight: %s' % c.gridheight    )
    if c.weightx    != default.weightx    : results.append( '   weightx: %s' % `c.weightx`     )
    if c.weighty    != default.weighty    : results.append( '   weighty: %s' % `c.weighty`     )
    if c.anchor     != default.anchor     : results.append( '    anchor: %d' % c.anchor        )
    if c.fill       != default.fill       : results.append( '      fill: %s' % const[ c.fill ] )
    if c.insets     != default.insets     : results.append( '    insets: %s' % c.insets        )
    if c.ipadx      != default.ipadx      : results.append( '     ipadx: %d' % c.ipadx         )
    if c.ipady      != default.ipady      : results.append( '     ipady: %d' % c.ipady         )
    if len( results ) :
        print 'Non-default constraint values:'
        print '\n'.join( results )
    else :
        print 'All constraint values match defaults'
