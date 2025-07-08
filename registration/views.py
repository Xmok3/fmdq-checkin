import qrcode
import csv
from io import BytesIO
from django.core.files import File
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Registration

# ---------- Registration & QR Code ----------
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        registration = Registration(name=name, phone=phone, email=email)
        registration.save()

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

def success(request):
    return render(request, 'registration/success.html')

# ---------- Dashboard ----------
def dashboard(request):
    registrations = Registration.objects.all()
    total = registrations.count()
    checked_in = registrations.filter(checked_in=True).count()

    context = {
        'registrations': registrations,
        'total': total,
        'checked_in': checked_in
    }
    return render(request, 'registration/dashboard.html', context)

# ---------- QR Code Check-In ----------
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

# ---------- QR Scanner Page ----------
def qr_scanner(request):
    return render(request, 'registration/scanner.html')

def qr_checkin(request, code):
    try:
        guest = Registration.objects.get(code=code)
        if guest.checked_in:
            return JsonResponse({'status': 'info', 'message': 'Already checked in'})
        guest.checked_in = True
        guest.save()
        return JsonResponse({'status': 'success', 'message': '✅ Check-in successful!'})
    except Registration.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '❌ Invalid code'})

# ---------- Export to CSV ----------
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Checked In'])

    for guest in Registration.objects.all():
        writer.writerow([guest.name, guest.phone, guest.email, guest.checked_in])

    return response
