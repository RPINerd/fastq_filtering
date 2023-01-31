import datetime
import logging
from Bio import SeqIO
import argparse
import re
import sys

def main(args):

    #TODO this is ugly
    keep_bool = len(args.keep) > 0
    drop_bool = len(args.drop) > 0
    keep_list = args.keep if (keep_bool) else None
    drop_list = args.drop if (drop_bool) else None

    #- Debug
    logging.debug("Keep: {}\nDrop: {}".format(str(keep_list), str(drop_list)))

    tot_input = 0
    dropped = 0
    pruned = []
    for record in SeqIO.parse(args.fastq, "fastq"):
        
        tot_input += 1

        if drop_bool:
            drop_flag = False
            for reg in drop_list:
                if re.search(reg, str(record.seq)):
                    dropped += 1
                    drop_flag = True
                    break

        if drop_flag:
            continue
        elif keep_bool:
            for reg in keep_list:
                if re.search(reg, str(record.seq)):
                    pruned.append(record)
                    break
    
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
    parser.add_argument("-k", "--keep", nargs="*", help="Keep reads matching this regex", required=False)
    parser.add_argument("-d", "--drop", nargs="*", help="Drop reads matching this regex", required=False)
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