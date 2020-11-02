import argparse
import random
import sys

class Shuf:
    def __init__(self, lines, count, repeat):
        self.count = count
        self.lines = lines
        self.repeat = repeat

    def randLine(self):
        return random.choice(self.lines)

    def generateLines(self):
        random.shuffle(self.lines)

    def printLines(self):
        #repeat false and count None
        if self.repeat==False and self.count is None:
            self.generateLines()
            for line in self.lines:
                sys.stdout.write(line)
        elif self.repeat==True and self.count is None:
            #repeat true count is none
            #infinite
            while(self.repeat):
                random.shuffle(self.lines)
                for line in self.lines:
                    sys.stdout.write(line)
        elif self.repeat==True and self.count is not None:
            #-r true -n provided
            for i in range(self.count):
                sys.stdout.write(self.randLine())
        elif self.repeat==False and self.count is not None:
            #-r false and -n provided
            self.generateLines()
            minval = min(len(self.lines), self.count)
            for i in range(minval):
                sys.stdout.write(self.lines[i])
        else:
            print("I don't know how it got here")
class C:
    pass
        
def main():
    #version_msg = '%(prog) 3.0'
    #usage_msg = '%(prog) [OPTION]... FILE or %(prog) -i LO-HI [OPTION]...'
    usage_1 = '%(prog)s [options]... FILE or '
    usage_2 = '%(prog)s -i LO-HI [options]...'
    parser = argparse.ArgumentParser(prog='shuf.py',
                usage=usage_1+usage_2)

    #-i
    parser.add_argument('-i', '--input-range', type=str, action='store',
                        dest="input_range", nargs='?', default=None,
                        help="treat each number LO through HI as an input line")
    #-n
    parser.add_argument('-n', '--head-count', type=int, action='store',
                        dest='head_count', nargs='?', default=None,
                        help="output at most COUNT lines")

    #-r
    parser.add_argument('-r', '--repeat', action='store_true',
                        dest='repeat', default=False,
                        help="output lines can be repeated")

    #positional arg
    parser.add_argument('filename', metavar='filename', type=str,
                        nargs='?', default=None)
    
    c = C()
    args = parser.parse_args(namespace=c)
    #sys.stdout.write(args['input_range'])
    #print(c.input_range)
    #print(c.head_count)
    #print(c.repeat)
    #print(c.filename)

    #test for bad inputs
    #check n
    if c.head_count != None:
        if c.head_count < 0:
            parser.error("head_count should be a positive integer.")
    inputs = []
    #check i
    low = 0
    high = 0
    if c.input_range != None:
        try:
            str1, str2 = c.input_range.split('-')
        except ValueError as e:
            parser.error("bad input range")
        #print(str1)
        #print(str2)
        try:
            low = int(str1)
            high = int(str2)
        except ValueError as e:
            parser.error("bad input range")
        #print(low)
        #print(high)
        #check if too many other inputs
        if c.filename is not None:
            parser.error("too many inputs")
        if low > high:
            parser.error("bad input range")
        inputs = [str(i)+"\n" for i in range(low, high+1)]
        #print("hi")
        #print(inputs)
    elif c.filename is None or c.filename == "-":
        #read from input
        #print("hellooo")
        inputs = sys.stdin.readlines()
        #print(inputs)
    else:
        #it's a file!
        f = open(c.filename, 'r')
        inputs = f.readlines()
        f.close()
        #print(inputs)
    
    #sys.stdout.write(args)
    if len(inputs) > 0:
        generator = Shuf(inputs, c.head_count, c.repeat)
        generator.printLines()

if __name__ == '__main__':
    main()
    
