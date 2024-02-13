from json import dumps, load
from os.path import dirname, join

from jsonpath_ng import parse
from rstcloth import RstCloth

TERMS_LIST = [
    "properties.turbine",
    "properties.turbine.properties.manufacturer_name",
    "properties.turbine.properties.manufacturer_display_name",
    "properties.turbine.properties.model_name",
    "properties.turbine.properties.model_description",
    "properties.turbine.properties.platform_name",
    "properties.turbine.properties.platform_description",
    "properties.turbine.properties.rotor_diameter",
    "properties.turbine.properties.drive_type",
    "properties.turbine.properties.regulation_type",
    "properties.turbine.properties.rated_power",
    "properties.turbine.properties.cut_in_rpm",
    "properties.turbine.properties.available_hub_heights",
    "properties.turbine.properties.grid_frequencies",
    "properties.design_bases",
    "properties.design_bases.items.properties.label",
    "properties.design_bases.items.properties.name",
    "properties.design_bases.items.properties.certification",
    "properties.design_bases.items.properties.certification.properties.certificate_reference",
    "properties.design_bases.items.properties.certification.properties.standard",
    "properties.design_bases.items.properties.certification.properties.standard_edition",
    "properties.design_bases.items.properties.design_class",
    "properties.design_bases.items.properties.design_class.oneOf[0].properties.class_label",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.class_label",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.annual_average_wind_speed",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.annual_average_air_density",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.reference_wind_speed",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.weibull_shape_factor",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.vertical_shear_exponent",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.inflow_angle",
    "properties.design_bases.items.properties.design_class.oneOf[1].properties.design_lifetime",
    "properties.design_bases.items.properties.turbulence",
    "properties.design_bases.items.properties.turbulence.anyOf[0].properties.category",
    "properties.design_bases.items.properties.turbulence.anyOf[1].properties.category",
    "properties.design_bases.items.properties.turbulence.anyOf[1].properties.reference_turbulence_intensity",
    "properties.design_bases.items.properties.turbulence.anyOf[1].properties.slope",
    "properties.design_bases.items.properties.turbulence.anyOf[2].properties.category",
    "properties.design_bases.items.properties.turbulence.anyOf[2].properties.wind_speed",
    "properties.design_bases.items.properties.turbulence.anyOf[2].properties.normal_turbulence_intensity",
    "properties.design_bases.items.properties.turbulence.anyOf[2].properties.extreme_turbulence_intensity",
    "properties.design_bases.items.properties.turbulence.anyOf[3].properties.category",
    "properties.design_bases.items.properties.turbulence.anyOf[3].properties.wind_speed",
    "properties.design_bases.items.properties.turbulence.anyOf[3].properties.normal_turbulence_intensity",
    "properties.design_bases.items.properties.turbulence.anyOf[3].properties.normal_hours_per_lifetime",
    "properties.design_bases.items.properties.turbulence.anyOf[3].properties.extreme_turbulence_intensity",
    "properties.design_bases.items.properties.standard_climate",
    "properties.design_bases.items.properties.standard_climate.properties.operating_temperature_range",
    "properties.design_bases.items.properties.standard_climate.properties.survival_temperature_range",
    "properties.design_bases.items.properties.cold_climate",
    "properties.design_bases.items.properties.cold_climate.properties.operating_temperature_range",
    "properties.design_bases.items.properties.cold_climate.properties.survival_temperature_range",
    "properties.design_bases.items.properties.hot_climate",
    "properties.design_bases.items.properties.hot_climate.properties.operating_temperature_range",
    "properties.design_bases.items.properties.hot_climate.properties.survival_temperature_range",
]


def generate_terms():
    schema_file = join(dirname(__name__), "power-curve-schema", "schema.json")
    terms_file = join(dirname(__name__), "docs", "terms.rst")

    with open(schema_file, "r", encoding="utf-8") as fp:
        schema = load(fp)

    def get_term_dict(path):
        value = parse(path).find(schema)[0].value

        clean_value = {}
        clean_value["key"] = (
            path.replace("properties.", "")
            .replace("items.", "")
            .replace(".oneOf", "")
            .replace(".anyOf", "")
        )
        clean_value["level"] = clean_value["key"].count(".")
        clean_value["title"] = value.get("title", None)
        clean_value["description"] = value.get("description", None)
        clean_value["examples"] = value.get("examples", None)
        clean_value["comment"] = value.get("comment", None)
        return clean_value

    def add_term(doc, term_dict):
        if term_dict["level"] == 0:
            doc.h2(term_dict["key"])
        elif term_dict["level"] == 1:
            doc.h3(term_dict["key"])
        elif term_dict["level"] == 2:
            doc.h4(term_dict["key"])
        doc.newline()

        if term_dict["comment"] is not None:
            doc.attention(term_dict["comment"])
            doc.newline()

        if term_dict["description"] is not None:
            doc.content(term_dict["description"])
            doc.newline()

        if term_dict["examples"] is not None:
            doc.content("Examples: ")
            doc.newline()
            for example in term_dict["examples"]:
                doc.codeblock(dumps(example, indent=4), language="js")
                doc.newline()

    with open(terms_file, "w", encoding="utf-8") as output_file:
        doc = RstCloth(output_file)
        doc.title("Terms used in the schema")
        doc.newline()
        doc.h1("Contents")
        doc.table_of_contents()
        doc.newline()
        doc.h1("Document Sections")
        doc.newline()
        for path in TERMS_LIST:
            add_term(doc, get_term_dict(path))
