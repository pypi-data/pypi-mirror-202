import json
import datetime
import codecs


def format_item(item, date_format):
    if isinstance(item, datetime.date):
        return item.strftime(date_format)
    elif isinstance(item, datetime.date):
        return item.__str__()
    elif isinstance(item, dict):
        for k, v in item.items():
            item[k] = format_item(v, date_format)
    elif isinstance(item, list):
        for k, v in enumerate(item):
            item[k] = format_item(v, date_format)
    return item


def write_to_file(data, path, date_format="%Y-%m-%d"):
    """Export extracted fields to json

    Appends .json to path if missing and generates json file in specified directory, if not then in root

    Parameters
    ----------
    data : dict
        Dictionary of extracted fields
    path : str
        directory to save generated json file
    date_format : str
        Date format used in generated file

    Notes
    ----
    Do give file name to the function parameter path.

    Examples
    --------
        >>> from invoice2data.output import to_json
        >>> to_json.write_to_file(data, "/exported_json/invoice.json")
        >>> to_json.write_to_file(data, "invoice.json")

    """
    for invoice in data:
        for k, v in invoice.items():
            invoice[k] = format_item(v, date_format)

    if path.endswith(".json"):
        filename = path
    else:
        filename = path + ".json"

    with codecs.open(filename, "w", encoding="utf-8") as json_file:
        json.dump(
            data,
            json_file,
            indent=4,
            sort_keys=False,
            ensure_ascii=False,
        )
