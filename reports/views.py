import mimetypes
import os
from tempfile import NamedTemporaryFile

from django.http import HttpResponse
from django.shortcuts import render

from reports.excel import create_xlsx_report


# Create your views here.
def download_file(request):
    filename = 'week_report.xlsx'

    with NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        mime_type = create_xlsx_report(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # os.unlink(tmp.name)  # manually clearing tempfile
        return response
