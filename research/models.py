from django.db import models


class Application(models.Model):
    PROGRAM_CHOICES = [
        ('phd', 'Doctor of Philosophy (PhD)'),
        ('edd', 'Doctor of Education (EdD)'),
        ('mphil', 'Master of Philosophy (MPhil)'),
        ('mrm', 'Master in Research Methodology (MRM)'),
    ]
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coordinator_notes = models.TextField(blank=True)

    # Personal details
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    previous_surname = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    place_of_birth = models.CharField(max_length=150, blank=True)
    home_province = models.CharField(max_length=100, blank=True)
    residence_during_study = models.CharField(max_length=150, blank=True)
    previously_enrolled = models.CharField(max_length=5, blank=True)
    previous_student_id = models.CharField(max_length=50, blank=True)
    disabilities = models.TextField(blank=True)

    # Contact details
    address = models.TextField(blank=True)
    email = models.EmailField()
    work_email = models.EmailField(blank=True)
    mobile_phone = models.CharField(max_length=30, blank=True)
    work_phone = models.CharField(max_length=30, blank=True)

    # Emergency contact
    emergency_name = models.CharField(max_length=150, blank=True)
    emergency_relationship = models.CharField(max_length=100, blank=True)
    emergency_mobile = models.CharField(max_length=30, blank=True)
    emergency_email = models.EmailField(blank=True)

    # Educational qualifications
    award = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    year_started = models.PositiveIntegerField(null=True, blank=True)
    year_completed = models.PositiveIntegerField(null=True, blank=True)
    other_qualifications = models.TextField(blank=True)

    # Work experience
    work_experience = models.TextField(blank=True)

    # Proposed research
    study_mode = models.CharField(max_length=30, blank=True)
    fee_payment_method = models.CharField(max_length=50, blank=True)
    research_topic = models.CharField(max_length=255, blank=True)
    research_outline = models.TextField(blank=True)
    statement_of_purpose = models.TextField(blank=True)
    previous_work = models.TextField(blank=True)
    equipment_travel = models.TextField(blank=True)
    supervisor_arrangement = models.TextField(blank=True)

    declaration = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    @property
    def applicant_name(self):
        if self.full_name:
            return self.full_name
        return ' '.join(part for part in [self.first_name, self.middle_name, self.surname] if part)

    def __str__(self):
        return f'{self.applicant_name} - {self.get_program_display()} ({self.get_status_display()})'


class ApplicationDocument(models.Model):
    CATEGORY_CHOICES = [
        ('fee_receipt', 'Application Fee Receipt'),
        ('qualification', 'Qualification Documents'),
        ('cv', 'Curriculum Vitae'),
        ('reference', 'Professional Reference'),
    ]

    application = models.ForeignKey(Application, related_name='documents', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='applications/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_category_display()} - {self.application}'
