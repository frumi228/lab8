from django.db import models


class Locomotive(models.Model):
    registration_number = models.AutoField(primary_key=True)
    depot = models.CharField(max_length=50)
    locomotive_type = models.CharField(
        max_length=50,
        choices=[('вантажний', 'вантажний'), ('пасажирський', 'пасажирський')]
    )
    manufacture_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.locomotive_type} - {self.registration_number}"


class Brigade(models.Model):
    brigade_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Brigade {self.brigade_id}"


class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    brigade = models.ForeignKey(Brigade, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Repair(models.Model):
    repair_id = models.AutoField(primary_key=True)
    locomotive = models.ForeignKey(Locomotive, on_delete=models.CASCADE)
    repair_type = models.CharField(
        max_length=50,
        choices=[
            ('поточний', 'поточний'),
            ('технічне обслуговування', 'технічне обслуговування'),
            ('позаплановий', 'позаплановий')
        ]
    )
    start_date = models.DateField()
    repair_days = models.PositiveIntegerField()
    daily_cost = models.DecimalField(max_digits=10, decimal_places=2)
    brigade = models.ForeignKey(Brigade, on_delete=models.CASCADE)

    def __str__(self):
        return f"Repair {self.repair_id} for Locomotive {self.locomotive.registration_number}"
