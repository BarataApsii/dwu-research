from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Application, ApplicationDocument

TEXT_FIELDS = [
    'title', 'first_name', 'middle_name', 'surname', 'full_name',
    'previous_surname', 'gender', 'nationality', 'place_of_birth',
    'home_province', 'residence_during_study', 'previously_enrolled',
    'previous_student_id', 'disabilities', 'email', 'work_email',
    'mobile_phone', 'work_phone', 'emergency_name', 'emergency_relationship',
    'emergency_mobile', 'emergency_email', 'award', 'specialization',
    'institution', 'other_qualifications', 'work_experience', 'study_mode',
    'fee_payment_method', 'research_topic', 'research_outline',
    'statement_of_purpose', 'previous_work', 'equipment_travel',
    'supervisor_arrangement',
]

FILE_CATEGORIES = {
    'fee_receipt': 'fee_receipt',
    'fee_payment': 'fee_receipt',
    'qualification_documents': 'qualification',
    'cv': 'cv',
    'professional_references': 'reference',
}


def _save_application(request, program):
    post = request.POST
    data = {field: post.get(field, '') for field in TEXT_FIELDS}
    data['address'] = post.get('postal_address') or post.get('mailing_address') or post.get('address', '')
    data['mobile_phone'] = post.get('mobile_phone') or post.get('phone', '')
    data['work_experience'] = post.get('work_experience') or post.get('employment_history', '')
    data['award'] = post.get('award') or post.get('highest_qualification', '')
    data['nationality'] = post.get('nationality') or post.get('country_of_citizenship', '')
    data['date_of_birth'] = post.get('date_of_birth') or None
    data['year_started'] = post.get('year_started') or None
    data['year_completed'] = post.get('year_completed') or None
    data['declaration'] = post.get('declaration') == 'on'

    submitted_program = post.get('program', '').lower()
    if submitted_program in ('phd', 'edd'):
        program = submitted_program

    application = Application.objects.create(program=program, **data)
    for field_name, category in FILE_CATEGORIES.items():
        for upload in request.FILES.getlist(field_name):
            ApplicationDocument.objects.create(application=application, category=category, file=upload)
    return application


def _handle_application_post(request, program, template):
    if request.method == 'POST':
        _save_application(request, program)
        messages.success(request, 'Your application has been submitted successfully. The Postgraduate & Research Centre will contact you by email.')
        return redirect(request.path)
    return render(request, template)


def research(request):
    return render(request, 'research/research.html')


def doctor_of_philosophy(request):
    return render(request, 'research/doctor-of-philosophy.html')


def master_of_philosophy(request):
    return render(request, 'research/master-of-philosophy.html')


def master_of_research_methodology(request):
    return render(request, 'research/master-of-research-methodology.html')


def mrm_application_form(request):
    return _handle_application_post(request, 'mrm', 'research/mrm-application-form.html')


def mphil_application_form(request):
    return _handle_application_post(request, 'mphil', 'research/mphil-application-form.html')


def phd_application_form(request):
    return _handle_application_post(request, 'phd', 'research/phd-application-form.html')


def doctor_of_education(request):
    return render(request, 'research/doctor-of-education.html')


@staff_member_required
def coordinator_dashboard(request):
    applications = Application.objects.all()

    query = request.GET.get('q', '').strip()
    program = request.GET.get('program', '')
    status = request.GET.get('status', '')

    if query:
        applications = applications.filter(
            Q(first_name__icontains=query) | Q(middle_name__icontains=query)
            | Q(surname__icontains=query) | Q(full_name__icontains=query)
            | Q(email__icontains=query) | Q(research_topic__icontains=query)
        )
    if program in dict(Application.PROGRAM_CHOICES):
        applications = applications.filter(program=program)
    if status in dict(Application.STATUS_CHOICES):
        applications = applications.filter(status=status)

    paginator = Paginator(applications, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    all_applications = Application.objects.all()
    status_counts = {row['status']: row['total'] for row in all_applications.values('status').annotate(total=Count('id'))}
    program_counts = {row['program']: row['total'] for row in all_applications.values('program').annotate(total=Count('id'))}

    return render(request, 'research/coordinator-dashboard.html', {
        'page_obj': page_obj,
        'applications': page_obj.object_list,
        'total_count': all_applications.count(),
        'status_counts': status_counts,
        'program_counts': program_counts,
        'program_choices': Application.PROGRAM_CHOICES,
        'status_choices': Application.STATUS_CHOICES,
        'query': query,
        'selected_program': program,
        'selected_status': status,
    })


@staff_member_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
        application.coordinator_notes = request.POST.get('coordinator_notes', '')
        application.save()
        messages.success(request, 'Application updated.')
        return redirect('research:application-detail', pk=application.pk)

    return render(request, 'research/application-detail.html', {
        'application': application,
        'documents': application.documents.all(),
        'status_choices': Application.STATUS_CHOICES,
    })
