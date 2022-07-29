import datetime
import logging
from Bio import SeqIO
import argparse
import re
import sys

def main(args):

    #- Debug
    logging.debug("Keep: " + args.keep)
    logging.debug("Drop: " + args.drop)

    tot_input = 0
    dropped = 0
    pruned = []
    for record in SeqIO.parse(args.fastq, "fastq"):
        tot_input += 1
        if re.search(args.drop, str(record.seq)):
            dropped += 1
            continue
        elif re.search(args.keep, str(record.seq)):
            pruned.append(record)
        else:
            continue
    
    logging.info("Filtering Stats:\n\tTotal Input Records: {tot} \
        \n\tDropped Records: {drp} \
        \n\tSaved Records: {kp}".format(tot = tot_input, drp = dropped, kp = len(pruned)))

    out_file = str(args.fastq).split(".", 1)[0] + "_filtered.fastq"
    #- Debug
    logging.debug("Output name: " + out_file)
    SeqIO.write(pruned, out_file, "fastq")

    return

if __name__ == "__main__":

    # Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fastq", help="Input fastq file", required=True)
    parser.add_argument("-k", "--keep", help="Keep reads matching this regex", required=False)
    parser.add_argument("-d", "--drop", help="Drop reads matching this regex", required=False)
    parser.add_argument("-s", "--sync", help="Sync the filtered file to its paired read", required=False)
    parser.add_argument("-v", "--verbose", help="Creates logging file with information for debugging", required=False, action='store_true')
    args = parser.parse_args()

    # Logging
    log_name = "fqfilter_{}.log".format(datetime.datetime.now().strftime("%y%m%d_%I_%M"))
    if args.verbose:
        logging.basicConfig(filename=log_name, encoding='utf-8', level=getattr(logging, "DEBUG", None))
    else:
        logging.basicConfig(filename=log_name, encoding='utf-8', level=getattr(logging, "INFO", None))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    logging.info('Logging started!')

    main(args)