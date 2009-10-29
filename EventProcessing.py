from EventEngine import EventEngine
from Address import Address

class Behavior():

    @staticmethod
    def audio(string):
        address = Address('/Defaults/audioplay')
    	result = EventEngine.root.getByAddress(address.__str__()).use(string)
        print "result from behavior audio: "+result
        return result

    @staticmethod
    def text(file):
        f =  open(file)
        string = f.read()
        return string

class Formatter():

    @staticmethod
    def ajax(head, string):
        #return 'ajaxreturn'
        if not string:
            string = ""
	return '<div id="get"><div class="toolbar"><h1>'+head+'</h1><a class="back" href="#">Back</a></div><div class="info" style="text-align: left; ">'+string.replace("\n","<br/>\n")+'</div></div>'


