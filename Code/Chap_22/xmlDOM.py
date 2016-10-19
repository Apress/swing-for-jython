#-------------------------------------------------------------------------------
#    Name: xmlDOM.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script demonstrating the use of XML parsing using the
#          simple Document Object Model (DOM) approach
#    Note: This script does not require WebSphere
#   Usage: wsadmin -f xmlDOM.py <filename>
#            or
#          jython xmlDOM.py <filename>
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.0   New - ...
#-------------------------------------------------------------------------------
import sys

from java.io           import File
from javax.xml.parsers import DocumentBuilder
from javax.xml.parsers import DocumentBuilderFactory
from org.w3c.dom       import Document, Element, Node, NodeList

#-------------------------------------------------------------------------------
# Name: traverse()
# Role: Recursive routine used to traverse the DOM tree
#-------------------------------------------------------------------------------
def traverse( node, indent = 0 ) :
    prefix = '%*s' % ( indent, '' )
    while node :
        if node.getNodeType() == Node.ELEMENT_NODE :
            print '%s<%s>'  % ( prefix, node.getNodeName() )
            traverse( node.getFirstChild(), indent + 2 )
            print '%s</%s>' % ( prefix, node.getNodeName() )
        elif node.getNodeType() == Node.TEXT_NODE :
            value = node.getNodeValue()
            if value :
                value = value.strip()
                if value :
                    print '%s"%s"' % ( prefix, value )
        node = node.getNextSibling()

#-------------------------------------------------------------------------------
# Name: dom()
# Role: Instantiate the object classes required to demonstrate the DOM parsing
#-------------------------------------------------------------------------------
def dom( filename ):
    try :
        doc  = DocumentBuilderFactory.newInstance(
        ).newDocumentBuilder().parse(
            File( filename )
        )
        root = doc.getDocumentElement()
        root.normalize()
        traverse( root )
    except :
        print '\nError: %s\nvalue: %s' % sys.exc_info()[ :2 ]

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: Verify that the script was executed, not imported, and that 1 parameter
#       was provided.
#-------------------------------------------------------------------------------
which  = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
jython = ( which[ 0 ] == 'j' )  # 0 in wsadmin 1 in jython environment
if __name__ == '__main__' :
    argc = len( sys.argv )
    if argc == jython + 1 :
        dom( sys.argv[ jython ] )
    else :
        print '\nError - unexpected number of parameters:', argc
        print '\nUsage: %s xmlDOM.py <filename>' % which
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py <filename>' % ( which, __name__ )
    sys.exit()
