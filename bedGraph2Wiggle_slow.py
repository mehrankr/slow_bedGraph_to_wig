import gzip
import argparse
import datetime as dt
parser = argparse.ArgumentParser(description="Converting bedgraph to wiggle format of file")
parser.add_argument('bg_file', help="Full path to bedgraph file for conversion")
parser.add_argument('chr', help="Chromosome ID in chrz for z in {1..23,X,Y,M}")
parser.add_argument('-outfile', default='Not entered' , help="Name of output file\
        (With directory if different\
        than current directory")
parser.add_argument('-gz', default=False, type=bool, help="Boolean indicating\
        if the zip file should be written")
args = parser.parse_args()
bg_file = args.bg_file
chr = args.chr
out_file = args.outfile
gz = args.gz

def write_to_file(gz, out_file, out_wig):
    if gz:
        if "gz" not in out_file:
            out_file = out_file + '.gz'
        out_write = gzip.open(out_file, 'wb')
        for each_line in out_wig:
            out_write.write(each_line)
    else:
        out_write = open(out_file, 'w')
        for each_line in out_wig:
            out_write.write(each_line)
  
line_ad = 'fixedStep chrom=chrZ start=60001 step=1\n'
if out_file == 'Not entered':
        in_ext = bg_file.split('.')[-1]
        out_file = bg_file.split(in_ext)[0] + chr + ".wig"
else:
    out_file = out_file + "-" + chr

bedg = open(bg_file,"r")
other_chr = True

print "Files loaded, searching for :" + chr

while other_chr:
    temp = bedg.readline()
    if chr+"\t" in temp:
        other_chr = False

print chr + " found, conversion begins"

out_wig = [temp]
last_line = line_ad
count = 1
temp_count = 0
for each_line in bedg:
    chr = last_line.split(" ")[1].split("=")[1]
    st = int(last_line.split(" ")[2].split("=")[1])
    vals = each_line.split("\t")
    for i in range(1,3):
        vals[i] = int(vals[i])
    vals[3] = float(vals[3])
    if vals[0]!=chr or (st+temp_count)!=vals[1]:
        line_ad = 'fixedStep chrom='+vals[0]+" start=" + str(vals[1]) + " step=1\n"
        out_wig.append(line_ad)
        last_line = out_wig[-1]
        temp_count = 0
    for position in range(vals[1],vals[2]):
        temp_count = temp_count + 1
        ad_outwig = str(position) + "\t" + str(vals[3]) + "\n"
        out_wig.append(ad_outwig)
    if count%100000==0:
        print str(count) + " genomic positions done at: " + str(dt.datetime.now())
        write_to_file(gz, out_file, out_wig)
        out_wig = []
    count = count+1

bedg.close()
out_write.close()
