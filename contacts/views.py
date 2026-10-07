from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Contact

# render halaman utama kontak
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/index.html", {"contacts": contacts})

# tambah kontak baru via htmx post, balikin fragment rows
def contact_add(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        if name and email:
            Contact.objects.create(name=name, email=email, phone=phone)
            
    contacts = Contact.objects.all()
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})

# live search kontak via htmx get
def contact_search(request):
    query = request.GET.get("q", "").strip()
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query)
        )
    else:
        contacts = Contact.objects.all()
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})

# hapus kontak via htmx delete, balikin http response kosong biar row di-swap hilang
@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return HttpResponse("")

# ganti baris data jadi form edit inline
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_edit_row.html", {"contact": contact})

# batal edit dan balikin lagi jadi baris data biasa
def contact_row(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_row.html", {"contact": contact})

# update data kontak via htmx put
@require_http_methods(["PUT"])
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = QueryDict(request.body)
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    if "phone" in data:
        contact.phone = data.get("phone", contact.phone)
    contact.save()
    return render(request, "contacts/_contact_row.html", {"contact": contact})
