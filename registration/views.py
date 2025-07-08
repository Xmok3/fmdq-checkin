import qrcode
from io import BytesIO
from django.core.files import File
from .models import Registration
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.http import HttpResponse

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Checked In'])

    for guest in Registration.objects.all():
        writer.writerow([guest.name, guest.phone, guest.email, guest.checked_in])

    return response


def checkin(request, code):
    reg_id = code.replace("FMDQ-", "")
    try:
        guest = Registration.objects.get(id=reg_id)
        if not guest.checked_in:
            guest.checked_in = True
            guest.save()
            return HttpResponse(f"✅ {guest.name} successfully checked in!")
        else:
            return HttpResponse(f"⚠️ {guest.name} already checked in.")
    except Registration.DoesNotExist:
        return HttpResponse("❌ Invalid QR code.")



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # 1. Create registration object first (but don’t save QR yet)
        registration = Registration(name=name, phone=phone, email=email)
        registration.save()

        # 2. Generate QR Code (we'll encode the ID or phone for now)
        qr = qrcode.make(f"FMDQ-{registration.id}")
        buffer = BytesIO()
        qr.save(buffer)
        filename = f"qr_{registration.id}.png"
        registration.qr_code.save(filename, File(buffer), save=True)

        return render(request, 'registration/success.html', {
            'name': name,
            'qr_url': registration.qr_code.url
        })

    return render(request, 'registration/register.html')
