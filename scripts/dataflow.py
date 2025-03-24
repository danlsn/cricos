import datetime
import re
from pprint import pprint

from dataflows import load, Flow, sources
from frictionless import formats, Dialect, Schema, Field, fields, transform, steps, Package
from frictionless.formats import ExcelControl
from frictionless.resources import FileResource, TableResource, Resource
from slugify import slugify


def main():
    pkg = Package('../raw/*.xlsx')

    pkg.name = "cricos-providers-courses-and-locations"

    pkg.title = "CRICOS Providers, Courses and Locations"

    for resource in pkg.resources:
        try:
            resource.dialect = Dialect(
                header_rows=[3],
                skip_blank_rows=True,
                controls=[ExcelControl(sheet="Institutions", stringified=True)],
            )

            resource.infer(stats=True)

            pat = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})")
            match = pat.search(resource.name)
            effective_date = datetime.date(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )


            for fld in resource.schema.fields:
                fld.name = slugify(fld.name, to_lower=True, separator="_")
                resource.schema.set_field_type(fld.name, "string")

            resource = transform(
                resource,
                steps=[
                    steps.field_add(
                        name="effective_date",
                        value=effective_date,
                        descriptor={"type": "date"},
                    )
                ],
            )

            pprint(resource.read_rows())
            print(resource)
        except Exception as e:
            print(f"Error: {e}")

    resource = Resource(
        name="cricos_institutions_at_2025_03_11",
        path=r"../raw/cricos-providers-courses-and-locations-as-at-2025-3-11-11-35-09.xlsx",
        dialect=Dialect(
            header_rows=[3],
            skip_blank_rows=True,
            controls=[ExcelControl(sheet="Institutions", stringified=True)],
        ),
    )
    resource.infer(stats=True)

    for fld in resource.schema.fields:
        fld.name = slugify(fld.name, to_lower=True, separator="_")
        resource.schema.set_field_type(fld.name, "string")

    resource = transform(
        resource,
        steps=[
            steps.field_add(
                name="effective_date",
                value=datetime.date(2025, 3, 11),
                descriptor={"type": "date"},
            )
        ],
    )

    pprint(resource.read_rows())
    print(resource)


if __name__ == "__main__":
    main()
