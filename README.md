# fastq_filtering

Provided a single, or list of, regular expressions, filter out all reads from a given fastq file which match said expression(s). One use case could be dropping reads with a large amount of poly-A sequences:

`python3 fqfilter.py -f Sample01.fastq -d "[A]{25}"`

## Options

`-f`/`--fastq`      - Input fastq file to filter, Required  
`-k`/`--keep`       - Regex expression(s) to keep  
`-d`/`--drop`       - Regex expression(s) to drop  
`-s`/`--sync`       - Synchronize R1/R2 fastq's for downstream processing  
`-v`/`--verbose`    - Debug output  
