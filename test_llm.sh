python lexigraph/lexigraph/lexigraph.py ${1} ${2} ${3} "${4}" 2> log/${2}_${3}.log
cp lexigraph/lexigraph/output.png log/${2}_${3}.png
#python lexigraph/lexigraph/lexigraph.py ${1} ${2} ${3} 2> >(tee log/${2}.log >&2);

