from pathlib import Path
from pprint import pprint

from datapackage import Package, Resource


def main():
    if Path("datapackage.json").exists():
        package = Package("datapackage.json")
    else:
        package = Package()

    descriptor = {
        "path": "raw/cricos-providers-courses-and-locations-as-at-2025-3-11-11-35-09.xlsx",
        "name": "cricos-providers-courses-and-locations-as-at-2025-3-11-11-35-09",
        "type": "table",
        "format": "xlsx",
        "scheme": "file",
        "mediatype": "application/vnd.ms-excel",
        "encoding": "utf-8",
        "dialect": {
            "headerRows": [3],
            "commentRows": [1, 2, 3],
            "excel": {"sheet": "Institutions"},
        },
    }
    resource = Resource(descriptor)
    resource.save(
        "raw/cricos-providers-courses-and-locations-as-at-2025-3-11-11-35-09.dataresource.json"
    )
    pprint(resource.read(keyed=True))
    package.save("datapackage.json")


if __name__ == "__main__":
    main()
