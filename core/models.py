from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid


# ============================================================
# SITE SETTINGS (with Voting & Nomination toggles)
# ============================================================

class SiteSettings(models.Model):
    # ---- Branding ----
    site_name = models.CharField(max_length=200, default='Pinnacle Excellence Awards Africa')
    tagline = models.CharField(max_length=500, default='Celebrating Excellence. Inspiring Impact. Honouring Greatness.')
    footer_text = models.TextField(blank=True)
    
    # ---- Feature Flags ----
    voting_open = models.BooleanField(default=True, help_text="Legacy flag (kept for compatibility)")
    results_live = models.BooleanField(default=False, help_text="Show live results on the public site")
    
    # ---- Countdown ----
    countdown_label = models.CharField(max_length=100, default='The Night Begins In')
    countdown_date = models.DateTimeField(default=timezone.now)
    
    # ---- Nomination Period Window ----
    nomination_open_date = models.DateTimeField(null=True, blank=True, help_text="Date when nominations open")
    nomination_close_date = models.DateTimeField(null=True, blank=True, help_text="Date when nominations close")
    
    # ---- Voting Period Window ----
    voting_open_date = models.DateTimeField(null=True, blank=True, help_text="Date when voting opens")
    voting_close_date = models.DateTimeField(null=True, blank=True, help_text="Date when voting closes")
    
    # ---- MASTER TOGGLES (controlled from admin panel) ----
    nominations_enabled = models.BooleanField(
        default=True, 
        help_text="Master switch for nominations — when off, all nominations are blocked regardless of date window"
    )
    voting_enabled = models.BooleanField(
        default=True, 
        help_text="Master switch for voting — when off, all voting is blocked regardless of date window"
    )
    
    # ---- Paystack ----
    paystack_secret_key = models.CharField(max_length=255, blank=True, default='')
    paystack_public_key = models.CharField(max_length=255, blank=True, default='')
    paystack_active = models.BooleanField(default=False)
    
    # ---- Email (SMTP) ----
    smtp_host = models.CharField(max_length=255, blank=True, default='')
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=255, blank=True, default='')
    smtp_password = models.CharField(max_length=255, blank=True, default='')
    smtp_use_tls = models.BooleanField(default=True)
    from_email = models.EmailField(blank=True, default='')
    
    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def is_nomination_open(self):
        """
        Returns True only when:
          - master switch is on
          - current time is within the configured window (if set)
        """
        if not self.nominations_enabled:
            return False
        now = timezone.now()
        if self.nomination_open_date and now < self.nomination_open_date:
            return False
        if self.nomination_close_date and now > self.nomination_close_date:
            return False
        return True
    
    def is_voting_open(self):
        """
        Returns True only when:
          - master switch is on
          - current time is within the configured window (if set)
        """
        if not self.voting_enabled:
            return False
        now = timezone.now()
        if self.voting_open_date and now < self.voting_open_date:
            return False
        if self.voting_close_date and now > self.voting_close_date:
            return False
        return True
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name_plural = "Site Settings"


# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):
    # Main category groups (26 total)
    GROUP_CHOICES = [
        ('Music & Entertainment', 'Music & Entertainment'),
        ('Dance & Performance', 'Dance & Performance'),
        ('Film & Television', 'Film & Television'),
        ('Fashion & Design', 'Fashion & Design'),
        ('Visual Arts & Culture', 'Visual Arts & Culture'),
        ('Media & Journalism', 'Media & Journalism'),
        ('Business & Enterprise', 'Business & Enterprise'),
        ('Finance & Banking', 'Finance & Banking'),
        ('Accounting & Audit', 'Accounting & Audit'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Real Estate & Construction', 'Real Estate & Construction'),
        ('Agriculture & Food Security', 'Agriculture & Food Security'),
        ('Transport & Logistics', 'Transport & Logistics'),
        ('Tourism & Hospitality', 'Tourism & Hospitality'),
        ('Technology & Innovation', 'Technology & Innovation'),
        ('Digital & Social Media', 'Digital & Social Media'),
        ('Artificial Intelligence & Tech', 'Artificial Intelligence & Tech'),
        ('Education & Academia', 'Education & Academia'),
        ('Youth & Empowerment', 'Youth & Empowerment'),
        ('Healthcare & Wellness', 'Healthcare & Wellness'),
        ('Community & Humanity', 'Community & Humanity'),
        ('Human Rights & Advocacy', 'Human Rights & Advocacy'),
        ('Faith & Spirituality', 'Faith & Spirituality'),
        ('Leadership & Public Service', 'Leadership & Public Service'),
        ('Sports & Athletics', 'Sports & Athletics'),
        ('Environment & Sustainability', 'Environment & Sustainability'),
    ]
    
    name = models.CharField(max_length=200, help_text="The award name e.g., 'Best New Artist of the Year'")
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, help_text="Main category group")
    description = models.TextField(blank=True, help_text="What this award recognizes")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, default='fas fa-award')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.group})"
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['group', 'order', 'name']


# ============================================================
# NOMINEE
# ============================================================

class Nominee(models.Model):
    GENDER_CHOICES = [
        ('man', 'Man'),
        ('woman', 'Woman'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending Approval'),
        ('rejected', 'Rejected'),
        ('draft', 'Draft'),
    ]
    
    # ---- Basic Info ----
    name = models.CharField(max_length=200, help_text="Full name of the nominee")
    stage_name = models.CharField(
        max_length=200, blank=True, 
        help_text="Stage name, artist name, or public name (optional)"
    )
    email = models.EmailField(blank=True, help_text="Email address for voting link")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number for contact")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    
    # ---- Category Relations ----
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='nominees')
    group = models.CharField(max_length=50, choices=Category.GROUP_CHOICES, help_text="Main category group")
    
    # ---- Description & Photo ----
    description = models.TextField(help_text="Brief bio or description of achievements")
    photo = models.ImageField(upload_to='nominees/', blank=True, null=True, help_text="Profile photo")
    
    # ---- Voting ----
    votes = models.IntegerField(default=0, help_text="Total votes received")
    voting_slug = models.SlugField(
        unique=True, blank=True, max_length=100, 
        help_text="Unique voting link slug"
    )
    voting_code = models.CharField(
        max_length=10, blank=True, unique=True, 
        help_text="Short unique code for voting"
    )
    share_count = models.IntegerField(default=0, help_text="Number of times voting link was shared")
    
    # ---- Status & Display ----
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    featured = models.BooleanField(default=False, help_text="Featured on homepage")
    order = models.IntegerField(default=0, help_text="Display order")
    auto_approved = models.BooleanField(default=True, help_text="Auto-approved from user nomination")
    
    # ---- Email Tracking ----
    voting_email_sent = models.BooleanField(
        default=False, 
        help_text="Has the voting link email been sent?"
    )
    voting_email_sent_at = models.DateTimeField(
        null=True, blank=True, 
        help_text="When the voting link email was sent"
    )
    
    # ---- Timestamps ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate voting slug
        if not self.voting_slug:
            base_slug = slugify(self.stage_name or self.name)
            slug = base_slug
            counter = 1
            while Nominee.objects.filter(voting_slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.voting_slug = slug
        
        # Auto-generate voting code
        if not self.voting_code:
            code = str(uuid.uuid4())[:8].upper()
            while Nominee.objects.filter(voting_code=code).exclude(id=self.id).exists():
                code = str(uuid.uuid4())[:8].upper()
            self.voting_code = code
        
        # Keep group synced with category
        if self.category and not self.group:
            self.group = self.category.group
        
        super().save(*args, **kwargs)
    
    # ---- Helpers ----
    def get_voting_url(self):
        return f"/vote/{self.voting_slug}/"
    
    def get_full_voting_url(self, request=None):
        if request:
            return request.build_absolute_uri(self.get_voting_url())
        return self.get_voting_url()
    
    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
    def get_category_name(self):
        return self.category.name if self.category else "Uncategorized"
    
    def get_group_display(self):
        return self.group
    
    def get_display_name(self):
        """Return stage_name if available, otherwise name"""
        return self.stage_name or self.name
    
    def __str__(self):
        display = self.stage_name or self.name
        return f"{display} - {self.category.name if self.category else 'No Category'}"
    
    class Meta:
        ordering = ['-votes', 'order', 'name']


# ============================================================
# USER NOMINATION
# ============================================================

class UserNomination(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # ---- Nominee Details ----
    nominee_name = models.CharField(max_length=200, help_text="Full name of the person being nominated")
    nominee_stage_name = models.CharField(
        max_length=200, blank=True, 
        help_text="Stage name or artist name (optional)"
    )
    nominee_email = models.EmailField(blank=True, help_text="Email address for voting link")
    nominee_phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_nominations')
    description = models.TextField(help_text="Brief bio or description of achievements")
    is_self_nomination = models.BooleanField(
        default=False, 
        help_text="Is the person nominating themselves?"
    )
    
    # ---- Photo ----
    photo = models.ImageField(
        upload_to='nominee_uploads/', blank=True, null=True, 
        help_text="Profile photo uploaded by user"
    )
    
    # ---- Nominator Details ----
    nominator_name = models.CharField(max_length=200, help_text="Name of the person submitting the nomination")
    nominator_email = models.EmailField(help_text="Email of the person submitting")
    nominator_phone = models.CharField(max_length=20, blank=True, help_text="Phone of the person submitting")
    
    # ---- Admin ----
    auto_approve = models.BooleanField(default=True, help_text="Auto-approved if self-nomination")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    # ---- Relation to approved nominee ----
    approved_nominee = models.ForeignKey(
        Nominee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='user_nomination',
        help_text="The nominee record created from this nomination"
    )
    
    # ---- Timestamps ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nominee_name} - {self.nominator_name}"
    
    def get_category_name(self):
        return self.category.name if self.category else "Uncategorized"
    
    def get_display_name(self):
        """Return stage_name if available, otherwise name"""
        return self.nominee_stage_name or self.nominee_name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Nominations"


# ============================================================
# VOTE
# ============================================================

class Vote(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('M-Pesa', 'M-Pesa'),
        ('Paystack', 'Paystack'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
    ]
    
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE, related_name='votes_received')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='votes')
    voter_name = models.CharField(max_length=200, blank=True)
    voter_email = models.EmailField(blank=True)
    voter_phone = models.CharField(max_length=20, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    quantity = models.IntegerField(default=1)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending'
    )
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Paystack'
    )
    payment_response = models.JSONField(blank=True, null=True)
    paystack_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Vote for {self.nominee.name} - KSH {self.amount}"
    
    class Meta:
        ordering = ['-created_at']


# ============================================================
# GALLERY IMAGE
# ============================================================

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Gallery Images"
        ordering = ['order', '-created_at']


# ============================================================
# NEWS ARTICLE
# ============================================================

class NewsArticle(models.Model):
    TAG_CHOICES = [
        ('Announcement', 'Announcement'),
        ('Voting', 'Voting'),
        ('Academy', 'Academy'),
        ('Event', 'Event'),
        ('Results', 'Results'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField(blank=True)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "News Articles"
        ordering = ['-published_date', '-created_at']


# ============================================================
# HALL OF FAME
# ============================================================

class HallOfFame(models.Model):
    year = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='hall_of_fame/', blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
    def __str__(self):
        return f"{self.name} ({self.year})"
    
    class Meta:
        verbose_name_plural = "Hall of Fame"
        ordering = ['-year', 'order']


# ============================================================
# PARTNER
# ============================================================

class Partner(models.Model):
    TYPE_CHOICES = [
        ('presenting', 'Presenting Partner'),
        ('category', 'Category Partner'),
        ('media', 'Media Partner'),
        ('technology', 'Technology Partner'),
        ('community', 'Community Partner'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return None
    
    def get_type_display(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']


# ============================================================
# CATEGORY SEED (tracker for seed command)
# ============================================================

class CategorySeed(models.Model):
    """
    Tracks which category groups have been seeded.
    Used by the seed_categories management command.
    """
    group = models.CharField(max_length=50, choices=Category.GROUP_CHOICES)
    seeded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.group
    
    class Meta:
        verbose_name_plural = "Category Seeds"


# ============================================================
# EMAIL LOG (bulk sending tracking)
# ============================================================

class EmailLog(models.Model):
    EMAIL_TYPES = [
        ('voting_link', 'Voting Link'),
        ('nomination_confirmation', 'Nomination Confirmation'),
        ('bulk_voting', 'Bulk Voting Links'),
        ('custom', 'Custom Email'),
    ]
    
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES, default='custom')
    nominee = models.ForeignKey(
        Nominee, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='emails'
    )
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email_type} - {self.recipient} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-sent_at']