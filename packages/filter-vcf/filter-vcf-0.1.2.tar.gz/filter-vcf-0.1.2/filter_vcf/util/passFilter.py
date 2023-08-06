from logging import Logger


def pass_filter(vcf_string: str, log: Logger) -> str:
    # Set filter to PASS for all variants
    vcf_all_pass = []

    for line in vcf_string.split("\n"):
        if line != "":
            if line.startswith("#"):
                vcf_all_pass.append(line)

            else:
                working_line = line.split("\t")
                working_filter = working_line[6]

                if working_filter.upper() not in ["PASS", "."]:
                    working_line[6] = working_filter + ";Pass"
                    vcf_all_pass.append("\t".join(working_line))

                elif working_filter.upper() == ".":
                    working_line[6] = "Pass"
                    vcf_all_pass.append("\t".join(working_line))

                else:
                    vcf_all_pass.append("\t".join(working_line))

    # Concat to single string, and add newline to end
    vcf_all_pass = "\n".join(vcf_all_pass)
    vcf_all_pass = vcf_all_pass + "\n"

    return vcf_all_pass


def pass_only(vcf_string: str, log: Logger) -> str:
    # Extract variants with PASS in filter column
    vcf_only_pass = []

    for line in vcf_string.split("\n"):
        if line != "":
            if line.startswith("#"):
                vcf_only_pass.append(line)

            else:
                filter_match = ";PASS;"
                working_line = line.split("\t")
                working_filter = ";" + working_line[6] + ";"

                if filter_match in working_filter.upper():
                    vcf_only_pass.append("\t".join(working_line))

    # Concat to single string, and add newline to end
    vcf_only_pass = "\n".join(vcf_only_pass)
    vcf_only_pass = vcf_only_pass + "\n"

    return vcf_only_pass
