from django.db import models
from django.urls import reverse


# Create your models here.
class Сounterparty(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    inn = models.CharField(max_length=200, null=True, blank=True)
    Contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        return self.name or ''

    def get_absolute_url(self):
        return reverse('counterparty', kwargs={'counterparty_id': self.pk})


class Contract(models.Model):
    choices = (
        (1, 'Договор купли-продажи'),
        (2, 'Договор энергоснабжения')
    )
    type = models.IntegerField(choices=choices, null=True)
    date = models.DateField(auto_now=True, null=True)
    number = models.IntegerField(unique=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    acpoint = models.CharField(max_length=255, null=True)
    rate = models.ForeignKey('Rate', on_delete=models.PROTECT, blank=True, default=1)
    mrate = models.CharField(max_length=255, null=True)
    main_voltage = models.CharField(max_length=255, null=True)
    calc_scheme = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.pk) or str(0)


class Tu(models.Model):
    name = models.CharField(max_length=255)
    CHOISES = (
        (1, 'По показаниям'),
        (2, 'Процент от головы'),
        (3, 'С вычетом из головы'),
        (4, 'Процент от головы')
    )
    Сounterparty = models.OneToOneField('Сounterparty', on_delete=models.PROTECT, blank=True, default=None, null=True)
    Contract = models.OneToOneField('Contract', on_delete=models.SET_NULL, blank=True, default=None, null=True)
    code = models.IntegerField(blank=True, default=None, null=True)
    calc_type = models.IntegerField(choices=CHOISES, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, default=True, null=True)
    ats_code = models.IntegerField(max_length=16, null=True)
    Area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True)

    # head_tu головная точка учета
    # тариф = rate, прибор учета = meter_device

    def __str__(self):
        return self.ats_code

    def get_absolute_url(self):
        return reverse('tu', kwargs={'tu_id': self.pk})


class Rate(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rate', kwargs={'rate_id': self.pk})


class mChannel(models.Model):
    code = models.IntegerField(blank=True, default=None)
    desc = models.CharField(max_length=250, blank=True, default=True)


class mResults(models.Model):
    mChannel = models.IntegerField(blank=True, default=None)
    srart = models.IntegerField(blank=True, default=None)
    end = models.IntegerField(blank=True, default=None)
    valeu = models.IntegerField(blank=True, default=None)


class UploadedFile(models.Model):
    name = models.CharField(max_length=512, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Area(models.Model):
    name = models.CharField(max_length=512, null=True)
    ats_code = models.IntegerField(null=True)

    def __str__(self):
        return self.ats_code


class Measuring_point(models.Model):
    ats_code = models.IntegerField(max_length=16, null=True)
    name = models.CharField(max_length=255, null=True)
    power_object_name = models.CharField(max_length=255, null=True)
    connection_name = models.CharField(max_length=255, null=True)
    location_description = models.CharField(max_length=255, null=True)
    tu = models.ForeignKey('Tu', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ats_code


class Measuring_channel(models.Model):
    per = ((30, '30'), (60, '60'),)
    ats_code = models.IntegerField(max_length=2, null=True)
    Measuring_point_code = models.IntegerField(max_length=16, null=True)
    full_code = models.CharField(max_length=25, null=True)
    Measuring_point = models.ForeignKey('Measuring_point', on_delete=models.SET_NULL, null=True)
    period = models.IntegerField(choices=per, default=30)

    def __str__(self):
        return str(self.pk)


class Measuring_data(models.Model):
    Measuring_point = models.ForeignKey('Measuring_point', on_delete=models.SET_NULL, null=True)
    Measuring_channel = models.ForeignKey('Measuring_channel', on_delete=models.SET_NULL, null=True)
    Measuring_point_code = models.IntegerField(max_length=16, null=True)
    channel_ats_code = models.IntegerField(max_length=2, null=True)
    period_start = models.IntegerField(max_length=4, null=True)
    period_end = models.IntegerField(max_length=4, null=True)
    value = models.IntegerField(max_length=10, null=True)
    date=models.DateField(null=True)
    CHOISES = (
        (1, 'Активный прием'),
        (2, 'Активная отдача'),
        (3, 'Реактивный прием'),
        (4, 'Реактивная отдача')
    )
    type = models.IntegerField(choices=CHOISES, null=True)

    # def __str__(self):
    #     return str(self.Measuring_point_code) + '/' + (self.ats_code) + ' по периоду:' + str(
    #         self.period_start) + ':' + str(self.period_end)+'-'+str(self.value)+' КвТ/Ч'
