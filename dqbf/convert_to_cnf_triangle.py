## Call abc -f to_cnf.sh to convert the input file to CNF format

import os
# import subprocess
from subprocess import check_output
import sys
import re
from convert_to_cnf import *

dir = './dqbf/'
cnf_output = 'cnf_output.txt'
abc_output = 'abc_output.txt'
dqdimacs_output = 'dqdimacs.txt'

def triangle_gen_DQDIMACS(cnf_file, v_u, v_v, v_w, v_t, v_c, v_d, v_others):
            
    with open(cnf_file, 'r') as f:
        lines = f.readlines()
    with open(dqdimacs_output, 'w') as f:
        ignore = True
        for line in lines:
            if 'cnf' in line:
                f.write(line)
                ignore = False
                
                if len(v_u) > 0 or len(v_v) > 0:
                    f.write('a ')
                    if len(v_u) > 0:
                        f.write(''.join(str(u) + ' ' for u in v_u))
                    if len(v_v) > 0:
                        f.write(''.join(str(v) + ' ' for v in v_v))
                    if len(v_w) > 0:
                        f.write(''.join(str(w) + ' ' for w in v_w))
                    if len(v_t) > 0:
                        f.write(''.join(str(t) + ' ' for t in v_t))
                    f.write('0\n')

                if len(v_others) > 0:
                    f.write('e ')
                    f.write(''.join(str(o) + ' ' for o in v_others))
                    f.write('0\n')

                for c in v_c:
                    f.write('d ' + str(c) + ' ')
                    f.write(''.join(str(u) + ' ' for u in v_u))
                    f.write(''.join(str(v) + ' ' for v in v_v))
                    f.write(''.join(str(w) + ' ' for w in v_w))
                    f.write('0\n')

                for d in v_d:
                    f.write('d ' + str(d) + ' ')
                    f.write(''.join(str(u) + ' ' for u in v_u))
                    f.write(''.join(str(v) + ' ' for v in v_v))
                    f.write(''.join(str(t) + ' ' for t in v_t))
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

    vec_u, vec_v, vec_w, vec_t, vec_c, vec_d, vec_pi, vec_others = determine_quantifier(ids, vars, nCis, nVar)
    
    triangle_gen_DQDIMACS(cnf_output, vec_u, vec_v, vec_w, vec_t, vec_c, vec_d, vec_others)

