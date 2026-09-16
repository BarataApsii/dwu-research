# DWU Research App

Standalone Django app for Divine Word University's postgraduate research programs.

## Pages

- `/` — redirects to Doctor of Philosophy (PhD)
- `/doctor-of-philosophy/` — PhD program
- `/master-of-philosophy/` — Master of Philosophy (MPhil) program
- `/master-of-research-methodology/` — Master in Research Methodology (MRM) program
- `/doctor-of-education/` — Doctor of Education (EdD) program

## File structure

```
research/
├── templates/research/
│   ├── doctor-of-philosophy.html
│   ├── master-of-philosophy.html
│   ├── master-of-research-methodology.html
│   └── doctor-of-education.html
├── static/research/
│   ├── css/
│   ├── images/
│   └── docs/
├── urls.py
├── views.py
└── models.py (empty placeholder)
```

## Local setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver
```

## Integration notes

- This app is intended to be integrated into the existing DWU Django website.
- The existing site has a custom CMS; backend developers can clone this app and wire it into the main project.
- The 4 program templates use `{% static %}` for local CSS/images; other navigation links are placeholders for the main site.
