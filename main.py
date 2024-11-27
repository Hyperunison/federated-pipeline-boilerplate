from typing import List, Dict
from src.Service.UCDMResolver import UCDMConvertedField


def get_input_files(ucdm: List[Dict[str, str]], parameters: Dict[str, str]) -> Dict[str, str]:
    return {
        "samplesheet.csv": build_samplesheet(ucdm),
        "nextflow.config": file_get_contents('nextflow.config'),        # origin nextflow.config managed by biobank administrators
    }


def get_output_file_masks(parameters) -> Dict[str, str]:
    return {
        ".nextflow.log": "/basic/.nextflow.log",
        "samplesheet.csv": "/samplesheet.csv",
        "report.html": "/basic/report.html",
        "output/": "/output/",
    }


def get_nextflow_cmd(input_files: Dict[str, str], parameters, run_name, weblog_url):
    return "nextflow run hello -c nextflow.config -name {} -with-report report.html -with-weblog {} -with-trace -ansi-log".format(
        run_name,
        weblog_url,
    )


def build_samplesheet(ucdm: List[Dict[str, str]]) -> str:
    if not ucdm:
        return ""

    headers = ucdm[0].keys()

    lines = ["\t".join(headers)]  # Header row
    for row in ucdm:
        lines.append("\t".join(row.get(header, "") for header in headers))

    return "\n".join(lines)

def file_get_contents(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
