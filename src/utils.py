from io import StringIO
import csv
import typing as t
from flask import make_response

if t.TYPE_CHECKING:
    from flask.wrappers import Response


def csv_response(rows: t.Iterable) -> Response:
    """Make rows to Flask Response

    Args:
        rows (Iterable): rows to write csv file

    Returns:
        Response: Flask Response
    """
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(rows)
    res = make_response(si.getvalue())
    res.headers["Content-Disposition"] = "attachment; filename=export.csv"
    res.headers["Content-type"] = "text/csv"
    return res
