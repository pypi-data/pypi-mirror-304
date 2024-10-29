from jinja2 import Environment, PackageLoader, select_autoescape

from .classes import ERDDAP
from .utils import change_line_ending


def obj2xml(erddap: ERDDAP, xml_filename: str, parse_source_Attributes: bool = False) -> None:
    """Convert a python object to a XML datasets ERDDAP configuration.

    Args:
        erddap (ERDDAP): python object to convert.
        xml_filename (str): xml filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    # Render the template
    env = Environment(loader=PackageLoader("erddapcfg"), autoescape=select_autoescape())
    template = env.get_template("datasets.xml.j2")
    output = template.render(erddap=erddap)

    # Add xml declaration
    output = "<?xml version='1.0' encoding='ISO-8859-1'?>\n" + output

    # Custom unescape the CDATA blocks
    output = output.replace("::CDATA_START", "<![CDATA[")
    output = output.replace("::CDATA_STOP", "]]>")

    # Save xml
    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(output)
    change_line_ending(xml_filename)
