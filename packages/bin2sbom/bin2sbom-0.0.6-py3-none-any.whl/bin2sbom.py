import json
import logging
import sys
from pathlib import Path
from uuid import uuid4

import click
from cpe import CPE
from cve_bin_tool.checkers import BUILTIN_CHECKERS
from cve_bin_tool.strings import parse_strings
from cve_bin_tool.version_scanner import ProductInfo, ScanInfo

logging.basicConfig(force=True)


def generate(directory: Path):

    if not directory.is_dir():
        logging.critical(f"Not a directory! {directory}")
        exit(1)

    syft_template = """
    {
        "artifacts": [],
        "schema": {
            "version": "16.0.7",
            "url": "https://raw.githubusercontent.com/anchore/syft/main/schema/json/schema-16.0.7.json"
        }
    }
    """

    source = {
        "id": "b398bb342bf15ece229760698dc7e0e98836eef2ce55640919e0bb0af631f01d",
        "name": directory.name,
        # "version": "2.2.2",
        "type": "directory",
        "metadata": {"path": "."},
    }

    artifacts = {}

    checkers = {
        checker.name: checker.load()
        for checker in BUILTIN_CHECKERS.values()
        if checker.name != "sqlite"
    }

    scan_infos = []

    for filename in directory.rglob("*"):
        if not filename.is_file():
            continue

        if "zlib" not in str(filename):
            continue

        logging.info(filename)

        lines = parse_strings(filename)

        for dummy_checker_name, checker in checkers.items():
            checker = checker()
            result = checker.get_version(lines, str(filename))
            # do some magic so we can iterate over all results, even the ones that just return 1 hit
            if "is_or_contains" in result:
                results = [dict()]
                results[0] = result
            else:
                results = result

            for result in results:
                if "is_or_contains" in result:
                    version = "UNKNOWN"
                    if "version" in result and result["version"] != "UNKNOWN":
                        version = result["version"]
                    elif result["version"] == "UNKNOWN":
                        file_path = filename
                        logging.debug(
                            f"{dummy_checker_name} was detected with version UNKNOWN in file {file_path}"
                        )
                    else:
                        logging.error(f"No version info for {dummy_checker_name}")

                    if version != "UNKNOWN":
                        file_path = filename
                        logging.debug(
                            f'{file_path} {result["is_or_contains"]} {dummy_checker_name} {version}'
                        )
                        for vendor, product in checker.VENDOR_PRODUCT:
                            location = filename
                            if location is None:
                                location = "NotFound"

                            scan_infos.append(
                                ScanInfo(
                                    ProductInfo(vendor, product, version, location),
                                    file_path,
                                )
                            )

    for scan_info in scan_infos:

        cpe = CPE(
            f"cpe:/a:{scan_info.product_info.vendor}:{scan_info.product_info.product}:{scan_info.product_info.version}"
        )
        cpe_str = cpe.as_uri_2_3()
        if cpe_str not in artifacts:
            artifacts[cpe_str] = dict(
                id=uuid4(),
                locations=[],
                name=scan_info.product_info.product,
                version=scan_info.product_info.version,
                cpes=[cpe_str],
                type="library",
            )

        location = dict(
            path=str(scan_info.product_info.location)
            .replace(str(directory.resolve()), "")
            .strip("/")
        )
        artifacts[cpe_str]["locations"].append(location)

    artifacts = list(artifacts.values())

    sbom = json.loads(syft_template.strip())
    sbom["artifacts"] = artifacts
    sbom["source"] = source
    return sbom


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def cli(directory: Path):
    sbom = generate(directory=sys.argv[1])
    print(json.dumps(sbom, indent=4, default=str))


if __name__ == "__main__":
    cli()
