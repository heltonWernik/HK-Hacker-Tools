# This is a simple python programm to find a key if you know the plain text and the cipher text. 
import base64
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="input", help="The input, (plain text)")
    parser.add_option("-o", "--output", dest="output", help="The Output, (cipher text)")
    (options, arguments) = parser.parse_args()
    if not options.input:
        parser.error("(x) Please specify the plain text, input, use --help for more info.")
    elif not options.output:
        parser.error("(x) Please specify the cipher text, output, use --help for more info.")
    return options

options = get_arguments()
_input = options.input
_output = base64.decodestring(options.output)
key = ""
for i in range(min(len(_input),len(_output))):
	key += chr(ord(_input[i])^ord(_output[i]))

print "[+] I find the key ---> " + key