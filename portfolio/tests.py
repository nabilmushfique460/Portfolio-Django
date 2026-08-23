from django.core import mail
from django.test import TestCase
from django.urls import reverse
from .models import ContactMessage
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
        """Valid POST request saves message to db, sends emails, and sets success to True."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, I want to discuss a project.',
        }
        response = self.client.post(reverse('contact'), data)
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
        self.assertEqual(admin_mail.to, ['nabil29089@gmail.com'])
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

    def test_contact_form_submission_duplicate_debounced(self):
        """Rapid duplicate submissions are debounced so only 1 email per recipient is sent and 1 DB record saved."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, duplicate test message.',
        }
        # First submission
        response1 = self.client.post(reverse('contact'), data)
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(response1.context['success'])
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)  # 1 to user + 1 to admin

        # Immediate duplicate submission (simulating double-click / rapid resubmit)
        response2 = self.client.post(reverse('contact'), data)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.context['success'])
        # DB count must remain 1 and no additional emails sent
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_contact_form_submission_admin_as_sender(self):
        """When sender is admin_email, only 1 email is sent (admin notification) to avoid duplicate emails in admin inbox."""
        data = {
            'name': 'Admin User',
            'email': 'nabil29089@gmail.com',
            'message': 'Testing with admin email.',
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(ContactMessage.objects.count(), 1)
        # Exactly 1 email to admin (no separate user confirmation to same address)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['nabil29089@gmail.com'])
        self.assertIn('New Contact Message from Admin User', mail.outbox[0].subject)


class ProjectPagesTests(TestCase):
    def test_about_page_loads_projects_from_csv(self):
        """GET /about/ renders about.html with projects parsed from data.csv and no obsolete sections."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertIn('projects', response.context)
        projects = response.context['projects']
        self.assertGreater(len(projects), 0)

        # Verify first project details match data.csv
        todo_project = next((p for p in projects if p['title'] == 'Todo App'), None)
        self.assertIsNotNone(todo_project)
        self.assertIn('A distraction-free web app', todo_project['description'])
        self.assertTrue(todo_project['image'].startswith('https://images.unsplash.com/'))

        # Verify old "About Me" and "My Mission" sections are deleted
        content = response.content.decode('utf-8')
        self.assertNotIn('<h2>About Me</h2>', content)
        self.assertNotIn('<h2>My Mission</h2>', content)
        self.assertIn('SELECTED.', content)
        self.assertIn('SYSTEMS.', content)

    def test_services_page_renders_rich_services(self):
        """GET /services/ renders services.html with 6 enriched service cards and images."""
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services.html')
        self.assertIn('services', response.context)
        services = response.context['services']
        self.assertEqual(len(services), 6)

        # Verify first service details
        svc = services[0]
        self.assertEqual(svc['title'], 'Custom Full Stack Web Applications')
        self.assertTrue(svc['image'].startswith('https://images.unsplash.com/'))
        self.assertGreater(len(svc['deliverables']), 0)
        self.assertGreater(len(svc['tags']), 0)

        # Verify page content contains heading
        content = response.content.decode('utf-8')
        self.assertIn('ARCHITECTED.', content)
        self.assertIn('SCALABLE.', content)




