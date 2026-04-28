from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Instrument, Owner, JobType, Job
from .forms import TicketForm, JobFormSet, InstrumentForm, OwnerForm


def dashboard(request):
    tickets = Ticket.objects.select_related('instrument__owner').order_by('-created_at')
    context = {
        'tickets': tickets,
        'open_count': tickets.filter(status='open').count(),
        'in_progress_count': tickets.filter(status='in_progress').count(),
        'complete_count': tickets.filter(status='complete').count(),
        'picked_up_count': tickets.filter(status='picked_up').count(),
    }
    return render(request, 'repairs/dashboard.html', context)


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related('instrument__owner'), pk=pk)
    jobs = ticket.jobs.select_related('job_type')
    return render(request, 'repairs/ticket_detail.html', {'ticket': ticket, 'jobs': jobs})


def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        formset = JobFormSet(request.POST, queryset=Job.objects.none())
        if form.is_valid() and formset.is_valid():
            ticket = form.save()
            jobs = formset.save(commit=False)
            for job in jobs:
                job.ticket = ticket
                job.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
        formset = JobFormSet(queryset=Job.objects.none())
    return render(request, 'repairs/ticket_form.html', {'form': form, 'formset': formset, 'title': 'New Ticket'})


def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        formset = JobFormSet(request.POST, queryset=ticket.jobs.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            jobs = formset.save(commit=False)
            for job in jobs:
                job.ticket = ticket
                job.save()
            for job in formset.deleted_objects:
                job.delete()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
        formset = JobFormSet(queryset=ticket.jobs.all())
    return render(request, 'repairs/ticket_form.html', {'form': form, 'formset': formset, 'title': 'Edit Ticket'})


def owner_list(request):
    owners = Owner.objects.prefetch_related('instruments')
    return render(request, 'repairs/owner_list.html', {'owners': owners})


def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            owner = form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'repairs/owner_form.html', {'form': form, 'title': 'New Owner'})


def instrument_create(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = InstrumentForm()
    return render(request, 'repairs/instrument_form.html', {'form': form, 'title': 'New Instrument'})
