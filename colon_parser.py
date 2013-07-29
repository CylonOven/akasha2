

class Func_lib():
    "a dict, (maybe use SQLite?) to hold and query code trasation functions"
    def __init__(self,):
        self.fun_dict = {}
    
    def add_func(self, key, func):
        self.fun_dict[key] = func
    
    def traslate_code(self, colonName, body, uses):
        return self.fun_dict[colonName](body, dict(uses))

### Template traslation functions all 3 are basicly the same...
def foo_function(body, kwargs):
    """:colon function template
    should return a tuple of strings, second to be put at the end of all nested functions
    """
    result = "<foo "
    for k,v in kwargs.items():
        result += "%s=%s "%(k,v)

    return result +">" + body , "</foo>"

def bar_function(body, kwargs):
    """:colon function template
    should return a tuple of strings, second to be put at the end of all nested functions
    """
    result = "<bar "
    for k,v in kwargs.items():
        result += "%s=%s "%(k,v)

    return result +">" + body , "</bar>"

def baz_function(body, kwargs):
    """:colon function template
    should return a tuple of strings, second to be put at the end of all nested functions
    """
    result = "<baz "
    for k,v in kwargs.items():
        result += "%s=%s "%(k,v)

    return result +">" + body , "</baz>"
###
func_lib = Func_lib()
func_lib.add_func("foo", foo_function)
func_lib.add_func("bar", bar_function)
func_lib.add_func("baz", baz_function)
###


class ColonParser():
    """ parses speach code into colonWord (:word) chunks
    Each chunk will parse out data from each uses line
    Each uses line ("uses foo:bar") will be given to the :word's pre-function as keyword arguments

    nesting works thusly:
       the pre-fuction of each :word will be called once the chunk is parsed,
       if there are any :words nested inside the body of the :word
       they will be parsed in turn,
       after the whole body of the :word has been parsed will the post-function be called for that :word


    """
    def __init__(self, input_string):
        self.composite_list = []
        self.source_lines = input_string.split("\n")
        self.parse_index = 0


    def complete_parse(self):
        """parse each block into self.composite_list"""
        traslated_code = ""
        next_chunk = self.get_next_colon_block()
        while next_chunk is not None:
            self.composite_list.append(next_chunk)
            beg, end  = next_chunk.traslate()
            mid = next_chunk.col_parser.complete_parse()
            next_chunk = self.get_next_colon_block()
            traslated_code += beg + mid + end
        return traslated_code

    def get_next_colon_block(self):
        self.parse_text()
        colon_block, rest = self.parse_colon_chunk()
        if bool(colon_block):
            return ColonChunk(colon_block)
        else:
            return None
        
    def parse_lines(self,):
        "generator, pops out each line at each call"
        #raise NotImplementedError()
        while self.parse_index < len(self.source_lines):
            yield self.parse_index, self.source_lines[self.parse_index] 
            self.parse_index += 1


    def reverse_parseing(self, i):
        "reverse the parsing by i lines"
        self.parse_index = max(0, self.parse_index -i)
        return self.parse_index

    def parse_text(self,):
        "Returns empty string or all lines before first indent level :block or lower"
        start_i = self.parse_index
        end_i   = None
        for index, line in self.parse_lines():
            line_indent = self.count_indent_level(line)
            if line_indent is None: continue
            if line[line_indent:].startswith(":"):
                end_i = index
                self.reverse_parseing(1)
                break
        else: end_i = self.parse_index
        return (self.source_lines[start_i:end_i],
                self.source_lines[end_i:]) 
        
    
    def parse_colon_chunk(self,):
        """Returns a tuple of  the string that starts from the beginning of the first :word and ends at the next :word on the same or left'er indent level
        if no remaining :words returns None"""
        start_i = None
        end_i   = None
        colon_found = False
        colon_indent = None
        for index, line in self.parse_lines():
            #print("parsing line |%s|"%line)
            line_indent = self.count_indent_level(line)
            if line_indent is None:
                continue
            
            elif colon_found is False and\
                 line[line_indent:].startswith(":"): 
                colon_found = True
                colon_indent = line_indent
                start_i = index
            
            elif colon_found is True and\
                 line_indent <= colon_indent and\
                 line[line_indent:].startswith(":"):
                end_i = index
                break
            
        else:  #looped though whole source without finding :word
            if start_i is not None:
                end_i = self.parse_index #:block is everything 
            else:
                start_i = end_i = self.parse_index #should never be done if run after parsetext()
                          
        return (self.source_lines[start_i:end_i],
                self.source_lines[end_i:])


    def count_indent_level(self,string):
        "returns the cound of spaces at the beginning of the string"
        indent = 0
        if string.isspace(): return 0 
        for char in string:
            if char == "\t": raise ValueError("tab detected in indent")
            if char.isspace(): indent += 1
            else: break
        return indent



class ColonChunk():
    """A chunk of speach code that starts with a :word,
    there may or may not be other :words nested inside the chunk

    1) save name of :word
    2) parse all uses statments into a list of tuples 
        uses class:foo -> [(class,foo), ... ] 
    3) if change of indent call ColenParser on chunk"""

    def __init__ (self, chunk_lines):
        """ """
        self.name = self.parse_name(chunk_lines[0])
        self.col_parser = ColonParser("\n".join(chunk_lines[1:]))
        self.body, self.nests = self.col_parser.parse_text()
        self.uses, self.body = self.parse_uses(self.body)
    
    def traslate(self,):
        return func_lib.traslate_code(self.name, "\n".join(self.body), self.uses)
        

    def parse_name(self, name_line):
        name = name_line.strip()
        name = name.strip(":")
        return name

    def parse_uses(self, lines):
        uses = []
        for i, line in enumerate(lines):
            if line.split(None, 1)[0] == "uses":
                kwarg, val = line.split(None, 1)[1].split(":")
                uses.append((kwarg, val))
                #print(kwarg, val)
            else: break
        return (uses,
                lines[i:])

"""\
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
"""
example_input = """\

#all text before the first :word should be ignored
:form
uses get: <target url>
uses class: <class name>

    :div   
    uses class: foo
    this is some text
    :text area
    uses preload: more text

:form
uses get: <other url>
uses class: <other class>
    :div
    uses foo: foo"""

foo_input = """
:foo
uses cats:dogs
uses pigs:flying
The foo is strong in this one
    :baz
    uses dunno:lol
    baz can't dance
    :baz
    uses one:two
    nor can this baz
        :bar
        uses dance:active
        uses music:on
        damn bar can dance
    :foo
    uses music:off
    dance party is over

:baz
uses dance:forever
dance dance dance
"""
cp
if __name__ == '__main__':
    print("testing string \n|%s|"%foo_input)
    print("")
    cp = ColonParser(foo_input)
    # for i, l in  cp.parse_lines():
    #     print(i, "|%s|"%l)cp
    # print(":chunk |%s|%s"%cp.parse_text())
    # print(":chunk |%s|%s"%cp.parse_colon_chunk())
    code = cp.complete_parse()
