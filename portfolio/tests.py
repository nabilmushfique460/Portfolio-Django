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



