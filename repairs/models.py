from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Instrument(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='instruments')
    instrument_type = models.CharField(max_length=100)
    make = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.instrument_type}) — {self.owner}"


class JobType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    default_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('picked_up', 'Picked Up'),
    ]

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Ticket #{self.pk} — {self.instrument} [{self.get_status_display()}]"

    def total(self):
        return sum(j.price for j in self.jobs.all() if j.price is not None)


class Job(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='jobs')
    job_type = models.ForeignKey(JobType, on_delete=models.PROTECT, related_name='jobs')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_type} on Ticket #{self.ticket_id}"

    def save(self, *args, **kwargs):
        if self.price is None and self.job_type.default_price is not None:
            self.price = self.job_type.default_price
        super().save(*args, **kwargs)
