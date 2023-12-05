
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from base.emails import send_order_mail

def save_invoice_pdf(context:dict={}):
    template = get_template("pdfs/invoice.html")
    html = template.render(context)
    response = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = f"invoice-{uuid.uuid4()}"
    file_path = str(settings.BASE_DIR) + f"/public/static/invoice/{file_name}.pdf"


    try:
        with open(str(settings.BASE_DIR) + f"/public/static/invoice/{file_name}.pdf", "wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
        

    except Exception as e:
        print(e)

    send_order_mail(context['user'].email, file_path)

    if pdf.err:
        return " ", False
    
    return file_name, True