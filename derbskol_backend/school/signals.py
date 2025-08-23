from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment, Invoice, Student
import uuid

# Optionnel: génération PDF
def _try_generate_invoice_pdf(invoice):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from django.conf import settings
        import os

        file_name = f"invoice_{invoice.number}.pdf"
        path = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, file_name)

        c = canvas.Canvas(full_path, pagesize=A4)
        c.setTitle(f"Invoice {invoice.number}")
        c.drawString(100, 800, f"Facture: {invoice.number}")
        c.drawString(100, 780, f"Élève : {invoice.student.first_name} {invoice.student.last_name}")
        c.drawString(100, 760, f"Montant : {invoice.amount} MAD")
        c.drawString(100, 740, f"Date : {invoice.issued_at.strftime('%Y-%m-%d %H:%M')}")
        c.drawString(100, 700, "Merci pour votre paiement.")
        c.showPage()
        c.save()

        from django.core.files import File
        with open(full_path, 'rb') as f:
            invoice.pdf_file.save(file_name, File(f), save=True)
    except Exception:
        # Si reportlab non installé ou autre: on ignore calmement
        pass

@receiver(post_save, sender=Payment)
def create_invoice_on_payment(sender, instance: Payment, created, **kwargs):
    if not created:
        return
    # Générer un numéro unique
    number = f"INV-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
    invoice = Invoice.objects.create(
        number=number,
        student=instance.student,
        amount=instance.amount,
        status='PAID',
        issued_at=timezone.now(),
    )
    _try_generate_invoice_pdf(invoice)
