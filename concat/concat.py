import sys, io, os, re

def print_help():
    '''Prints standard help message to stdout'''

    print (sys.argv[0]  + ''' - script to _concatenate any kind of text files using simple syntax'''
             '''\nUsage: ''' + sys.argv[0] + ''' [fileName outputFile|-h]'''
             '''\nWhere:'''
             '''\n    fileName - main file to start joining files from'''
             '''\n    outputFile - file to write to (if missing, will write to stdout)'''
             '''\n    -h or --help - print this message''')
    return

def log(status, *args):
    print status, ' '.join(args)

class Linker(object):

    def __init__(self, file_read_name, file_write_name):
        self.file_read_name = file_read_name
        self.file_write_name = file_write_name

    def process(self):
        text = self._concat(self.file_read_name)
        file_write_handle = io.open(self.file_write_name, 'w')
        file_write_handle.write(text)
        file_write_handle.close()

    def _concat(self, file_name, line_prefix=''):
        '''Outputs processed input file
        If that file doesn't exist, ValueError is raised.
        '''

        if not (type(file_name) in (str, unicode)):
            raise TypeError('file_name must be string or unicode (is: ' + str(type(file_name)) + ')')

        file_handle = None
        lines = []
        try:
            file_handle = io.open(file_name, 'r')
            lines = file_handle.readlines()
        except IOError as err:
            raise ValueError('Couldn\'t open file: ' + err.filename)

        file_handle.close()

        absolute_file_path = os.path.dirname(file_name)
        regex = re.compile(r'^(?P<leading_whitespace>[ \t]*)//IMPORT (?P<file_name>.*)$')
        output = u''
        lineNo = 1
        for line in lines:
            match = regex.match(line)
            if match:
                #TODO: infinite recursion detection
                path = absolute_file_path + '/' + match.group('file_name')
                #leading whitespace is empty at first call but then gets accumulated 
                leading_whitespace = line_prefix + match.group('leading_whitespace')
                import_text = u''
                try:
                    #recursive imports are handled via recursion
                    import_text = self._concat(path, leading_whitespace)
                except ValueError as err:
                    log('Import error: file: \'{0}\', line: {1}\n{2}\n\tContinuing'
                            .format(absolute_file_path, str(lineNo), str(err)))
                output += import_text
            else:
                output += line_prefix + line

            lineNo += 1
        
        #append a newline if file not is empty and does not have trailing newline
        if output != '' and output[-1] != '\n':
            output += u'\n'

        return output


def main():
    args = sys.argv

    if len(args) == 1 or len(args) > 3:
        print_help()
        return 1

    write_to = None #TODO: stdout output doesn't work
    if len(args) == 3:
        write_to = args[2]

    if args[1] in ('-h', '--help'):
        printHelp()
        return 0
    else:
        parser = Parser(argv[1], write_to)
        parser.process()

    return 0

if __name__ == '__main__':
    main()

