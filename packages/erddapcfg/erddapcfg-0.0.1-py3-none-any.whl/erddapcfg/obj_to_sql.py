from jinja2 import Environment, PackageLoader, select_autoescape

from .classes import ERDDAP
from .sql_script import SQL_CREATE


def obj2sql(erddap: ERDDAP, sql_filename: str, parse_source_attributes: bool = False) -> None:
    """Convert a XML datasets ERDDAP configuration to a sql script.

    Args:
        erddap (ERDDAP): python object to convert.
        sql_filename (str): sql filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    output = [SQL_CREATE]

    # Render the template
    env = Environment(loader=PackageLoader("erddapcfg"), autoescape=select_autoescape())
    template = env.get_template("db_insert.j2")
    output.append(template.render(erddap=erddap))

    # Insert dataset children in db
    template = env.get_template("db_insert_dataset_children.j2")
    output.append(template.render(parent_child=erddap.parent_child))

    # Save sql
    with open(sql_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
