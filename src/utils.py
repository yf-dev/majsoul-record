from io import StringIO
import csv
from flask import make_response

def csv_response(rows):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(rows)
    res = make_response(si.getvalue())
    res.headers["Content-Disposition"] = "attachment; filename=export.csv"
    res.headers["Content-type"] = "text/csv"
    return res
