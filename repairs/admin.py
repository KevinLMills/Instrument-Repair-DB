from django.contrib import admin
from .models import Owner, Instrument, JobType, Ticket, Job


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [JobInline]
    list_display = ('pk', 'instrument', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    pass


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    pass
