## Call abc -f to_cnf.sh to convert the input file to CNF format

import os
# import subprocess
from subprocess import check_output
import sys
import re
from convert_to_cnf import *

cnf_output = 'cnf_output.txt'
abc_output = 'abc_output.txt'
dqdimacs_output = 'dqdimacs.txt'

def clique_determine_quantifier(ids, vars, nCis, nVar):
    vec_u, vec_v = [], []
    vec_i, vec_j = [], []
    vec_others = []
    vec_pi = []

    for i in range(1, nVar - nCis +1):
        vec_others.append(i)

    for i in range(nCis):
        if 'u' in vars[i]:
            vec_u.append(ids[i])
        elif 'v' in vars[i]:
            vec_v.append(ids[i])
        elif 'i' in vars[i]:
            vec_i.append(ids[i])
        elif 'j' in vars[i]:
            vec_j.append(ids[i])
        ### variable pi is for iscas coloring
        ### variable x, y, z are for triangular free amd edge coloring
        elif 'pi' in vars[i] or 'x' in vars[i] or 'y' in vars[i] or 'z' in vars[i]:
            vec_pi.append(ids[i])
        else:
            vec_others.append(ids[i])
    return vec_u, vec_v, vec_i, vec_j, vec_pi, vec_others


def clique_gen_DQDIMACS(cnf_file, v_u, v_v, v_i, v_j, v_pi, v_others):

    with open(cnf_file, 'r') as f:
        lines = f.readlines()
    with open(dqdimacs_output, 'w') as f:
        ignore = True
        for line in lines:
            if 'cnf' in line:
                f.write(line)
                ignore = False

                if len(v_i) > 0 or len(v_j) > 0:
                    f.write('a ')
                    if len(v_i) > 0:
                        f.write(''.join(str(i) + ' ' for i in v_i))
                    if len(v_j) > 0:
                        f.write(''.join(str(j) + ' ' for j in v_j))
                    f.write('0\n')

                for u in v_u:
                    f.write('d ' + str(u) + ' ')
                    f.write(''.join(str(i) + ' ' for i in v_i))
                    f.write('0\n')

                for v in v_v:
                    f.write('d ' + str(v) + ' ')
                    f.write(''.join(str(j) + ' ' for j in v_j))
                    f.write('0\n')
                
                if len(v_pi) > 0:
                    f.write('e ')
                    f.write(''.join(str(p) + ' ' for p in v_pi))
                    f.write('0\n')
                
                if len(v_others) > 0:
                    f.write('e ')
                    f.write(''.join(str(o) + ' ' for o in v_others))
                    f.write('0\n')

            elif not ignore:
                f.write(line)
            else:
                continue
    return

    

if __name__ == '__main__':
    convert_to_cnf(sys.argv[1], cnf_output)
    ids, vars, nCis, nVar= parse_abc_output()
    print(ids)
    print(vars)
    print("Number of Cis = " + str(nCis))
    print("Number of Vars = " + str(nVar))

    vec_u, vec_v, vec_i, vec_j, vec_pi, vec_others = clique_determine_quantifier(ids, vars, nCis, nVar)

    clique_gen_DQDIMACS(cnf_output, vec_u, vec_v, vec_i, vec_j, vec_pi, vec_others)

