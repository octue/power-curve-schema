import json
from icecream import ic
from rstcloth import RstCloth


def _generate(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in _generate(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in _generate(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]


def summarise(input_file_name, output_file_name):
    """Summarise the contents of a schema and output to restructuredText"""
    with open(input_file_name, mode="r", encoding="utf-8") as fp:
        schema = json.load(fp)

    with open(output_file_name, "w") as output_file:
        doc = RstCloth(output_file)
        doc.title("Contents Summary")
        doc.newline()
        doc.content("stuff")
        ic(dir(doc))
        doc.h2("Contents")
        doc.table_of_contents()
        doc.newline()
        doc.h2("Code -- shebang")
        doc.definition("name", "the text of the dnion")

    print(schema.keys())
    # ic(schema)
