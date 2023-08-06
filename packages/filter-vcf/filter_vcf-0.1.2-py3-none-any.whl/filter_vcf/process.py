import vcfpy
import logging
from pathlib import Path
from filter_vcf.util.readVcf import read_vcf
from filter_vcf.util.sortVcf import sort_vcf
from filter_vcf.util.addDepth import add_depth


def process_vcf(vcf_in: str, filters: str):
    allowed_filters = filters.split(":")
    vcf_out = vcf_in.replace("nrm.vcf.gz", "nrm.filtered.vcf.gz")
    print(f"saving file {vcf_out}")

    logging.info("Filtering VCF using filters: {}".format(allowed_filters))
    reader = vcfpy.Reader.from_path(vcf_in)
    writer = vcfpy.Writer.from_path(vcf_out, reader.header)
    for record in reader:
        if common_member(record.FILTER, allowed_filters):
            writer.write_record(record)
    writer.close()
    reader.close()

    return Path(vcf_out)


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    # if both sets are exact matches, great, lets move on
    if a_set == b_set:
        return True
    # if they aren't exact matches and set a has more than one filter values
    # then we return false as we don't let combinations exist in the record for filter
    if len(a_set) != 1:
        return False
    if len(a_set.intersection(b_set)) > 0:
        return True
    else:
        return False
