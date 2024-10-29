import os
import sqlite3

from jinja2 import Environment, PackageLoader, select_autoescape

from .classes import ERDDAP
from .sql_script import SQL_CREATE


def obj2db(erddap: ERDDAP, db_filename: str, parse_source_attributes: bool = False) -> None:
    """Convert a XML datasets ERDDAP configuration to a DB sqlite.

    Args:
        erddap (ERDDAP): python object to convert.
        db_filename (str): database sqlite filename.
        parse_source_Attributes (bool, optional): Flag to enable the parsing of the sourceAttributes nodes. Defaults to False.
    """

    # Create empty database file
    if os.path.isfile(db_filename):
        os.remove(db_filename)
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Create empty tables if database
    cursor.executescript(SQL_CREATE)

    # Render the template
    env = Environment(loader=PackageLoader("erddapcfg"), autoescape=select_autoescape())
    template = env.get_template("db_insert.j2")
    output = template.render(erddap=erddap)

    # Insert dataset children in db
    template = env.get_template("db_insert_dataset_children.j2")
    output += template.render(parent_child=erddap.parent_child)

    # Execute the inserts in db
    cursor.executescript(output)

    # Save db
    connection.commit()
    connection.close()
