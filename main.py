import argparse
import os

parser = argparse.ArgumentParser(description='Converts Brainfuck to C++, then compiles')
parser.add_argument('input', help='Input file')
parser.add_argument('-o', '--output', help='Output executable', default='out' + ('.exe' if os.name == 'nt' else ''))
parser.add_argument('-c', '--compiler', help='Compile to use', default='clang++')
parser.add_argument('-m', '--memory', help='Memory cells needed', default=512, type=int)
args = parser.parse_args()

out_cpp = f"""#include <stdio.h>
#include <iostream>

unsigned char tape[{args.memory}];
unsigned char *i;

int main() {{
    i = tape;\n"""

conversion = {
    ">": "    i++;\n",
    "<": "    i--;\n",
    "+": "    (*i)++;\n",
    "-": "    (*i)--;\n",
    ".": "    std::cout << *i;\n",
    ",": "    (*i) = (unsigned char)std::getchar();\n",
    "[": "    while ((*i) != 0) {{\n",
    "]": "    }}\n"
    #"[": "label_{}:\n    if ((*i) != 0) {{\n",
    #"]": "    }} if ((*i) != 0)\n    goto label_{};\n"
}

infile = open(args.input, 'r')
outfile = open(args.output + '.cpp', 'w')

inchars = infile.read()
level = 0
for i in inchars:
    if i in conversion:
        if i == "[":
            level += 1
            out_cpp += conversion[i].format(level)
        elif i == "]":
            out_cpp += conversion[i].format(level)
            level -= 1
        else:
            out_cpp += conversion[i]
        
out_cpp += "    return 0;\n}"
        
outfile.write(out_cpp)

infile.close()
outfile.close()
