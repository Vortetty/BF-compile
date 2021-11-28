import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Converts Brainfuck to C++, then compiles')
parser.add_argument('input', help='Input file')
parser.add_argument('-o', '--output', help='Output executable', default=None, type=str)
parser.add_argument('-c', '--compiler', help='Compile to use', default='clang++')
parser.add_argument('-m', '--memory', help='Memory cells needed', default=512, type=int)
parser.add_argument('-r', '--no-remove-cpp', help='Do not remove C++ file', action='store_false')
args = parser.parse_args()

if args.output is None:
    args.output = os.path.splitext(args.input)[0] + ('.exe' if os.name == 'nt' else '')

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
    ",": "    std::cout << \"\\nInput requested >>> \";std::cin >> (*i);\n",
    "[": "    while ((*i) != 0) {{\n",
    "]": "    }}\n"
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

subprocess.run(f"{args.compiler} {args.output}.cpp -o {args.output}", shell=True)

if args.no_remove_cpp:
    os.remove(args.output + '.cpp')
