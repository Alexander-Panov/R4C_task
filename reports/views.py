from django.http import HttpResponse

from reports.tools.WritableTempFile import WritableTempFile
from reports.tools.excel import create_xlsx_report


# Create your views here.
def download_file(request):
    filename = 'week_report.xlsx'

    with WritableTempFile(suffix=".xlsx") as tmp:
        mime_type = create_xlsx_report(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
