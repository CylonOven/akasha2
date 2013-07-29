# 0*<space><string>:
# uses <key string>: <arg string>
# <data string>
# And data string is everything between the last uses string and the next string: or end of file

# This parser breaks up an object into a series of pieces. It only
# pays attention to nesting to grab the right pieces. In display list
# creation, the hierarchy is flattened.

# Each piece consists of an object of the keyword strings type, a list
# of use keywords and associated data and the "string" following which
# is the data for this piece.

# To make things easier, all of the text between the first colon word
# and the start of the buffer is ignored.

# We are going to try this as a generator where the input is a string
# and the output is a series of pieces or, as I'm now thinking of
# them, colon objects.

# How to start the code:
#define the class
#define a constructor method and filling in as best we can figure out.

class colon parser:
    """ """
    def __init__(self, source string):
        self.composite list = []

#Feeling a bit lost about what to do. In my mind, what I think I want
#to do is writing three gatherers. A gatherer collect information
#until there is a state change. For example, when a colon keyword has
#been discovered, the: gatherer runs to the end of the line and
#extracts the keyword. Next, if the line begins with uses, the uses
#gatherer runs collecting the uses keyword and the uses keyword
#data. The last gatherer invoked when a line does not begin with
#uses. The everything gatherer complex characters until the first line
#starts with:

#Are gatherers ad hoc? Each one has a test to see if it should
#run. Each one has an extractor which pulls all the data elements and
#pushes them into the right part of an object and I'm wondering if
#there is a test for done. Colon word and uses both are done at the
#end of the line. The everything gatherer is done at the start of the
#next colon word.

class chunk gathering:
    """ """
   def __init__ (self,):
       """ """
       # not sure what to put here yet


:form
uses get: <target url>
uses class: <class name>

1)     :div   
2)     uses class: foo
3)     this is some text
     :text area
     uses preload: more text

:form
get: <target url>
class: <class name>
     :div   
     class: foo
     this is some text
     class:
     this is more text
 
    :text area
     preload: more text

:product
	uses product image: sss.jpeg
	uses description: that is a marvie product
