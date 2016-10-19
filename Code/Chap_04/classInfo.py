#-------------------------------------------------------------------------------
#    Name: classInfo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Provide a utility function that can be used to display information
#          about a class hierarchy.
#    Note: If either, or both of the "meth" or "attr" string values are
#          provided, they will be used to filter the list of methods, and/or
#          attributes to be displayed.
#    Note: The output of this is much better in the wsadmin environment than it
#          is using Jython.  However, it servers its purpose well in this simple
#          form, so changes needed to make the Jython output more readable are
#          left as an exercise for the reader.
#   Usage: from classInfo import classInfo
#          from javax.swing import JFrame
#          classInfo( JFrame, meth = '', attr = '' )
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
def classInfo( Class, meth = None, attr = None, pad = '' ) :
    print pad + str( Class )
    prefix = pad + '  '

    #---------------------------------------------------------------------------
    # Section used to display the (possibly filtered) list of class methods
    # Note: Methods will be indicated by lines containing ">" characters
    #---------------------------------------------------------------------------
    if type( meth ) == type( '' ) :
        comma, line = '', '' + prefix
        methods = [
            n for n, v in vars( Class ).items()
            if n.lower().find( meth.lower() ) > -1 and callable( v )
        ]
        methods.sort()
        for m in methods :
            if len( line + comma + m ) > 65 :
                print line.replace( '|', '>' )
                comma, line = '', '' + prefix
            line += comma + m
            comma = ', '
        if not line.endswith( '  ' ) :
            print line.replace( '|', '>' )

    #---------------------------------------------------------------------------
    # Section used to display the (possibly filtered) list of class attributes
    # Note: Attributes will be indicated by lines containing "*" characters
    #---------------------------------------------------------------------------
    if type( attr ) == type( '' ) :
        comma, line = '', '' + prefix
        attribs = [
            n for n, v in vars( Class ).items()
            if n.lower().find( attr.lower() ) > -1 and not callable( v )
        ]
        attribs.sort()
        for a in attribs :
            if len( line + comma + a ) > 65 :
                print line.replace( '|', '*' )
                comma, line = '', '' + prefix
            line += comma + a
            comma = ', '
        if not line.endswith( '  ' ) :
            print line.replace( '|', '*' )
      
    #---------------------------------------------------------------------------
    # Recursive invocation for base classes
    #---------------------------------------------------------------------------
    for b in Class.__bases__ :
        classInfo( b, meth, attr, pad + '| ' )
