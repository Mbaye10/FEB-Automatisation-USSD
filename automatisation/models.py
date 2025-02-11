from django.db import models

class CanalUSSD(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    description = models.TextField()  
    def __str__(self):
        return self.code


class UseCase(models.Model):
    canal = models.ForeignKey(CanalUSSD, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    ) 
    numerousecase = models.IntegerField(default=0)
    entree = models.CharField(max_length=255)
    sortie_attendue = models.TextField()

    def __str__(self):
        return self.nom


class TestResult(models.Model):
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
    date_test = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=[('OK', 'OK'), ('NOK', 'NOK')])
    message_erreur = models.TextField(blank=True, null=True)


class TestStep(models.Model):
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    description = models.TextField()
    input_value = models.CharField(max_length=255)
    expected_output = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.use_case.nom} - Étape {self.step_number}"


class DetailedTestResult(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    step = models.ForeignKey(TestStep, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=20)
    date_heure = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=[('OK', 'OK'), ('NOK', 'NOK')])
    message_erreur = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_heure']

    def __str__(self):
        return f"Test {self.test_result.id} - Étape {self.step.step_number}"


class AlertConfiguration(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'use_case', 'email']

    def __str__(self):
        return f"Alerte pour {self.use_case.nom} - {self.email}"