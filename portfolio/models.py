from django.db import models


class Project(models.Model):
    """A portfolio project shown on the Projects (about) page."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField('Repository / Live URL', blank=True)
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        help_text='Upload a project screenshot or cover image.',
    )
    image_url = models.URLField(
        'External Image URL',
        blank=True,
        help_text='Alternative: paste an external image URL instead of uploading.',
    )
    category = models.CharField(max_length=100, default='Software')
    category_slug = models.SlugField(
        max_length=50,
        default='all',
        help_text='Used for filtering (e.g. web, api, automation, ai-data, analytics, desktop).',
    )
    badge = models.CharField(max_length=100, blank=True)
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated tags (e.g. Django, Python, Full-Stack).',
    )
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(
        default=0,
        help_text='Lower numbers appear first.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        """Return the uploaded image URL or the external URL fallback."""
        if self.image:
            return self.image.url
        return self.image_url or ''

    @property
    def tags_list(self):
        """Return tags as a list for template iteration."""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class Service(models.Model):
    """A service offering shown on the Services (offerings) page."""

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    deliverables = models.TextField(
        blank=True,
        help_text='One deliverable per line.',
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated tags (e.g. Django, Flask, Redis Caching).',
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        help_text='Upload a service cover image.',
    )
    image_url = models.URLField(
        'External Image URL',
        blank=True,
        help_text='Alternative: paste an external image URL instead of uploading.',
    )
    badge = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text='Lower numbers appear first.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        """Return the uploaded image URL or the external URL fallback."""
        if self.image:
            return self.image.url
        return self.image_url or ''

    @property
    def tags_list(self):
        """Return tags as a list for template iteration."""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def deliverables_list(self):
        """Return deliverables as a list for template iteration."""
        if not self.deliverables:
            return []
        return [d.strip() for d in self.deliverables.strip().splitlines() if d.strip()]


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} ({self.email})"
