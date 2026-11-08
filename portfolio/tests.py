from unittest.mock import patch
from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from .models import ContactMessage, Project, Service
from .forms import ContactForm


class ContactMessageTests(TestCase):
    def test_contact_page_get(self):
        """GET request should render contact page with empty form."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertFalse(response.context['success'])

    def test_contact_form_submission_success(self):
        """Valid POST request saves message to db, sends emails, and redirects via PRG."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, I want to discuss a project.',
        }
        # follow=True verifies the full Post/Redirect/Get cycle
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])

        # Verify record in SQLite database
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved_msg = ContactMessage.objects.first()
        self.assertEqual(saved_msg.name, 'John Doe')
        self.assertEqual(saved_msg.email, 'john@example.com')
        self.assertEqual(saved_msg.message, 'Hello, I want to discuss a project.')
        self.assertEqual(str(saved_msg), 'John Doe (john@example.com)')

        # Verify emails sent: 1 confirmation to sender + 1 notification to admin
        self.assertEqual(len(mail.outbox), 2)

        # Email 1: Confirmation to user
        user_mail = mail.outbox[0]
        self.assertIn('Thank you for getting in touch!', user_mail.subject)
        self.assertEqual(user_mail.to, ['john@example.com'])
        self.assertIn('Hello, I want to discuss a project.', user_mail.body)

        # Email 2: Notification to admin
        admin_mail = mail.outbox[1]
        self.assertIn('New Contact Message from John Doe', admin_mail.subject)
        expected_admin = getattr(settings, 'ADMIN_EMAIL', 'nabil29089@gmail.com')
        self.assertEqual(admin_mail.to, [expected_admin])
        self.assertIn('Name: John Doe', admin_mail.body)
        self.assertIn('Email: john@example.com', admin_mail.body)
        self.assertIn('Message:\nHello, I want to discuss a project.', admin_mail.body)

    def test_contact_form_submission_invalid_email(self):
        """Invalid email does not save to db, does not send email, and displays form error."""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'message': 'Hello',
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_contact_form_honeypot_rejects_bot(self):
        """Bot populating the hidden honeypot website field is rejected."""
        data = {
            'name': 'Bot Spammer',
            'email': 'spammer@example.com',
            'message': 'Buy cheap crypto now!',
            'website': 'https://spam-domain.com',
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(response.context['success'])

    @patch('portfolio.views.send_mail')
    def test_contact_form_email_failure_handles_gracefully(self, mock_send_mail):
        """When SMTP fails, message is still saved and status reflects delayed delivery."""
        mock_send_mail.side_effect = Exception("SMTP Connection Timeout")
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Testing SMTP failure path.',
        }
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertFalse(response.context['success'])
        self.assertTrue(response.context['saved_delivery_failed'])


class ProjectPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_data')

    def test_about_page_loads_projects(self):
        """GET /about/ renders about.html with projects from DB and dynamic categories."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertIn('projects', response.context)
        projects = response.context['projects']
        self.assertGreater(projects.count(), 0)

        # Verify first project details
        todo_project = next((p for p in projects if p.title == 'Todo App'), None)
        self.assertIsNotNone(todo_project)
        self.assertIn('A distraction-free web app', todo_project.description)
        self.assertTrue(todo_project.display_image.startswith('https://images.unsplash.com/'))
        self.assertIn('Django', todo_project.tags_list)
        self.assertEqual(todo_project.display_id, '01')

        # Verify page content structure
        content = response.content.decode('utf-8')
        self.assertIn('SELECTED.', content)
        self.assertIn('SYSTEMS.', content)

    def test_services_page_renders_rich_services(self):
        """GET /services/ renders services.html with 6 enriched service cards and images."""
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')
        self.assertIn('services', response.context)
        services = response.context['services']
        self.assertEqual(services.count(), 6)

        # Verify first service details
        svc = services.first()
        self.assertEqual(svc.title, 'Custom Full Stack Web Applications')
        self.assertTrue(svc.display_image.startswith('https://images.unsplash.com/'))
        self.assertGreater(len(svc.deliverables_list), 0)
        self.assertGreater(len(svc.tags_list), 0)
        self.assertEqual(svc.display_id, '01')

        # Verify page content contains heading
        content = response.content.decode('utf-8')
        self.assertIn('ARCHITECTED.', content)
        self.assertIn('SCALABLE.', content)

    def test_home_page_renders_cleanly(self):
        """GET / renders home.html with live terminal and navigation links."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        content = response.content.decode('utf-8')
        self.assertIn('SHIP.', content)
        self.assertIn('BREAK.', content)
        self.assertIn('REBUILD.', content)
        self.assertIn('manage.py check', content)


class ModelPropertiesTests(TestCase):
    def test_project_model_helpers(self):
        """Test Project model helper properties and string representations."""
        project = Project.objects.create(
            title="Telemetry Dashboard",
            order=5,
            image_url="https://example.com/telemetry.png",
            tags="Django, InfluxDB, Celery",
        )
        self.assertEqual(str(project), "Telemetry Dashboard")
        self.assertEqual(project.display_image, "https://example.com/telemetry.png")
        self.assertEqual(project.display_id, "05")
        self.assertEqual(project.tags_list, ["Django", "InfluxDB", "Celery"])

    def test_service_model_helpers(self):
        """Test Service model helper properties and string representations."""
        service = Service.objects.create(
            title="Database Tuning",
            order=2,
            deliverables="Schema Review\nIndex Optimization\nSlow Query Profiling",
            tags="PostgreSQL, MySQL, Redis",
        )
        self.assertEqual(str(service), "Database Tuning")
        self.assertEqual(service.display_id, "02")
        self.assertEqual(len(service.deliverables_list), 3)
        self.assertEqual(service.deliverables_list[0], "Schema Review")
        self.assertEqual(service.tags_list, ["PostgreSQL", "MySQL", "Redis"])
