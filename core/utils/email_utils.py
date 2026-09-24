import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.utils import timezone
from core.models import SiteSettings, EmailLog

def get_email_settings():
    """Get email settings from SiteSettings"""
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        return {
            'host': '',
            'port': 587,
            'username': '',
            'password': '',
            'use_tls': True,
            'from_email': '',
        }
    return {
        'host': settings_obj.smtp_host,
        'port': settings_obj.smtp_port,
        'username': settings_obj.smtp_username,
        'password': settings_obj.smtp_password,
        'use_tls': settings_obj.smtp_use_tls,
        'from_email': settings_obj.from_email,
    }

def send_email(recipient_email, subject, html_message, text_message=None, email_type='custom', nominee=None):
    """
    Send an email using SMTP settings from SiteSettings
    """
    email_settings = get_email_settings()
    
    if not email_settings['host'] or not email_settings['username']:
        log = EmailLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            message=html_message[:1000],
            email_type=email_type,
            nominee=nominee,
            sent_successfully=False,
            error_message='SMTP settings not configured'
        )
        return False, 'SMTP settings not configured'
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_settings['from_email'] or email_settings['username']
        msg['To'] = recipient_email
        
        # Add text part if provided
        if text_message:
            text_part = MIMEText(text_message, 'plain')
            msg.attach(text_part)
        
        # Add HTML part
        html_part = MIMEText(html_message, 'html')
        msg.attach(html_part)
        
        # Connect and send
        context = ssl.create_default_context() if email_settings['use_tls'] else None
        
        with smtplib.SMTP(email_settings['host'], email_settings['port']) as server:
            if email_settings['use_tls']:
                server.starttls(context=context)
            server.login(email_settings['username'], email_settings['password'])
            server.sendmail(msg['From'], [recipient_email], msg.as_string())
        
        # Log success
        EmailLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            message=html_message[:1000],
            email_type=email_type,
            nominee=nominee,
            sent_successfully=True
        )
        
        return True, 'Email sent successfully'
        
    except Exception as e:
        # Log error
        EmailLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            message=html_message[:1000],
            email_type=email_type,
            nominee=nominee,
            sent_successfully=False,
            error_message=str(e)
        )
        return False, str(e)


def send_voting_link_email(nominee, request=None):
    """
    Send voting link email to a nominee with tips on how to win
    """
    if not nominee.email:
        return False, 'No email address for nominee'
    
    voting_url = nominee.get_full_voting_url(request)
    site_settings = SiteSettings.objects.first()
    site_name = site_settings.site_name if site_settings else 'Pinnacle Excellence Awards Africa'
    
    subject = f'Your Voting Link - {site_name}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Voting Link</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 0;
                color: #0F1A14;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                overflow: hidden;
            }}
            .header {{
                background: #0F1A14;
                padding: 32px 40px;
                text-align: center;
                border-bottom: 3px solid #F5C842;
            }}
            .header h1 {{
                color: #F5C842;
                margin: 0;
                font-size: 26px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header .subtitle {{
                color: #9FB1A8;
                margin: 4px 0 0;
                font-size: 12px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .body {{
                padding: 40px;
            }}
            .body h2 {{
                color: #0F1A14;
                margin-top: 0;
                font-size: 22px;
                font-weight: 600;
            }}
            .body p {{
                color: #5C6A62;
                font-size: 15px;
                line-height: 1.7;
                margin: 0 0 16px 0;
            }}
            .link-box {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin: 24px 0;
                border-left: 4px solid #F5C842;
            }}
            .link-box .label {{
                font-size: 13px;
                font-weight: 600;
                color: #5C6A62;
                margin: 0 0 4px 0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .link-box .link {{
                color: #2B6E4B;
                font-size: 18px;
                font-weight: 600;
                word-break: break-all;
                text-decoration: underline;
            }}
            .tips-section {{
                margin: 28px 0;
            }}
            .tips-section h3 {{
                color: #0F1A14;
                font-size: 17px;
                font-weight: 600;
                margin: 0 0 12px 0;
                padding-bottom: 8px;
                border-bottom: 2px solid #f0f0f0;
            }}
            .tips-section .tip {{
                padding: 10px 0;
                border-bottom: 1px solid #f0f0f0;
                display: flex;
                align-items: flex-start;
                gap: 12px;
                font-size: 14px;
                color: #5C6A62;
            }}
            .tips-section .tip:last-child {{
                border-bottom: none;
            }}
            .tips-section .tip-icon {{
                color: #F5C842;
                font-weight: 700;
                width: 24px;
                flex-shrink: 0;
                text-align: center;
            }}
            .tips-section .tip strong {{
                color: #0F1A14;
            }}
            .highlight-box {{
                background: #FFF8E1;
                border-radius: 8px;
                padding: 16px 20px;
                margin: 20px 0;
                border-left: 4px solid #F5C842;
            }}
            .highlight-box p {{
                margin: 0;
                color: #5C6A62;
                font-size: 14px;
            }}
            .highlight-box strong {{
                color: #0F1A14;
            }}
            .btn-container {{
                text-align: center;
                margin: 32px 0 16px;
            }}
            .btn-vote {{
                background: #F5C842;
                color: #0F1A14;
                padding: 14px 40px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: 700;
                font-size: 15px;
                display: inline-block;
                transition: background 0.2s ease;
            }}
            .btn-vote:hover {{
                background: #E5B832;
            }}
            .footer {{
                background: #0F1A14;
                padding: 20px 40px;
                text-align: center;
            }}
            .footer p {{
                color: #6C7B72;
                margin: 0;
                font-size: 12px;
            }}
            .footer .tagline {{
                color: #6C7B72;
                margin: 4px 0 0;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f7f6; padding: 20px;">
            <tr>
                <td align="center">
                    <div class="container">
                        <div class="header">
                            <h1>PINNACLE EXCELLENCE</h1>
                            <div class="subtitle">AWARDS AFRICA</div>
                        </div>
                        <div class="body">
                            <h2>Hello {nominee.get_display_name()},</h2>
                            <p>
                                You have been successfully nominated for the <strong>{nominee.category.name}</strong> category at the <strong>Pinnacle Excellence Awards Africa</strong>.
                            </p>
                            <p>
                                Your personalized voting link is ready. Share it with your supporters and start collecting votes.
                            </p>
                            <div class="link-box">
                                <p class="label">Your Voting Link</p>
                                <a href="{voting_url}" class="link">{voting_url}</a>
                            </div>
                            <div class="tips-section">
                                <h3>How to Win</h3>
                                <div class="tip">
                                    <span class="tip-icon">1.</span>
                                    <div><strong>Share Your Link</strong> — Share your voting link with friends, family, and followers</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">2.</span>
                                    <div><strong>Social Media</strong> — Post on WhatsApp, Instagram, Facebook, and Twitter</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">3.</span>
                                    <div><strong>Community Engagement</strong> — Ask your community to vote for you</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">4.</span>
                                    <div><strong>Email Campaign</strong> — Send your link to your email contacts</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">5.</span>
                                    <div><strong>Vote Multiple Times</strong> — Unlimited voting allowed; encourage supporters to vote multiple times</div>
                                </div>
                            </div>
                            <div class="highlight-box">
                                <p><strong>Pro Tip:</strong> Every vote counts. The more you share, the higher your chances of winning.</p>
                            </div>
                            <div class="btn-container">
                                <a href="{voting_url}" class="btn-vote">Start Getting Votes</a>
                            </div>
                        </div>
                        <div class="footer">
                            <p>&copy; {timezone.now().year} Pinnacle Excellence Awards Africa. All rights reserved.</p>
                            <p class="tagline">Celebrating Excellence. Inspiring Impact. Honouring Greatness.</p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    text_message = f"""
    Hello {nominee.get_display_name()}!
    
    You have been successfully nominated for the {nominee.category.name} category at the Pinnacle Excellence Awards Africa.
    
    Your personalized voting link is: {voting_url}
    
    Share this link with your supporters and start collecting votes!
    
    Tips to Win:
    1. Share your link with friends, family, and followers
    2. Post on WhatsApp, Instagram, Facebook, and Twitter
    3. Ask your community to vote for you
    4. Send your link to your email contacts
    5. Unlimited voting allowed - encourage multiple votes!
    
    Best of luck!
    
    Pinnacle Excellence Awards Africa
    """
    
    return send_email(
        recipient_email=nominee.email,
        subject=subject,
        html_message=html_message,
        text_message=text_message,
        email_type='voting_link',
        nominee=nominee
    )


def send_nomination_confirmation_email(nomination, request=None):
    """
    Send confirmation email after successful nomination (self-nomination)
    """
    if not nomination.nominator_email:
        return False, 'No email address'
    
    nominee = nomination.approved_nominee
    if not nominee:
        return False, 'No approved nominee linked to this nomination'
    
    voting_url = nominee.get_full_voting_url(request)
    site_settings = SiteSettings.objects.first()
    site_name = site_settings.site_name if site_settings else 'Pinnacle Excellence Awards Africa'
    
    subject = f'Nomination Confirmed - {site_name}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nomination Confirmed</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 0;
                color: #0F1A14;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                overflow: hidden;
            }}
            .header {{
                background: #0F1A14;
                padding: 32px 40px;
                text-align: center;
                border-bottom: 3px solid #F5C842;
            }}
            .header h1 {{
                color: #F5C842;
                margin: 0;
                font-size: 26px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header .subtitle {{
                color: #9FB1A8;
                margin: 4px 0 0;
                font-size: 12px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .body {{
                padding: 40px;
                text-align: center;
            }}
            .confirmation-icon {{
                width: 64px;
                height: 64px;
                border-radius: 50%;
                background: #E6F4EC;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 16px;
            }}
            .confirmation-icon i {{
                color: #2B6E4B;
                font-size: 28px;
            }}
            .body h2 {{
                color: #0F1A14;
                margin-top: 0;
                font-size: 22px;
                font-weight: 600;
            }}
            .body p {{
                color: #5C6A62;
                font-size: 15px;
                line-height: 1.7;
                margin: 0 0 16px 0;
            }}
            .link-box {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin: 24px 0;
                border-left: 4px solid #2B6E4B;
            }}
            .link-box .label {{
                font-size: 13px;
                font-weight: 600;
                color: #5C6A62;
                margin: 0 0 4px 0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .link-box .link {{
                color: #2B6E4B;
                font-size: 18px;
                font-weight: 600;
                word-break: break-all;
                text-decoration: underline;
            }}
            .tips-section {{
                margin: 28px 0;
                text-align: left;
            }}
            .tips-section h3 {{
                color: #0F1A14;
                font-size: 17px;
                font-weight: 600;
                margin: 0 0 12px 0;
                padding-bottom: 8px;
                border-bottom: 2px solid #f0f0f0;
                text-align: left;
            }}
            .tips-section .tip {{
                padding: 10px 0;
                border-bottom: 1px solid #f0f0f0;
                display: flex;
                align-items: flex-start;
                gap: 12px;
                font-size: 14px;
                color: #5C6A62;
                text-align: left;
            }}
            .tips-section .tip:last-child {{
                border-bottom: none;
            }}
            .tips-section .tip-icon {{
                color: #F5C842;
                font-weight: 700;
                width: 24px;
                flex-shrink: 0;
                text-align: center;
            }}
            .tips-section .tip strong {{
                color: #0F1A14;
            }}
            .btn-container {{
                text-align: center;
                margin: 32px 0 16px;
            }}
            .btn-vote {{
                background: #F5C842;
                color: #0F1A14;
                padding: 14px 40px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: 700;
                font-size: 15px;
                display: inline-block;
                transition: background 0.2s ease;
            }}
            .btn-vote:hover {{
                background: #E5B832;
            }}
            .footer {{
                background: #0F1A14;
                padding: 20px 40px;
                text-align: center;
            }}
            .footer p {{
                color: #6C7B72;
                margin: 0;
                font-size: 12px;
            }}
            .footer .tagline {{
                color: #6C7B72;
                margin: 4px 0 0;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f7f6; padding: 20px;">
            <tr>
                <td align="center">
                    <div class="container">
                        <div class="header">
                            <h1>PINNACLE EXCELLENCE</h1>
                            <div class="subtitle">AWARDS AFRICA</div>
                        </div>
                        <div class="body">
                            <div class="confirmation-icon">
                                <i style="font-family: 'Font Awesome 5 Free'; font-weight: 900;">&#xf058;</i>
                            </div>
                            <h2>Nomination Confirmed</h2>
                            <p>
                                Congratulations <strong>{nomination.nominee_name}</strong>! You have successfully been nominated for the <strong>{nomination.category.name}</strong> category.
                            </p>
                            <div class="link-box">
                                <p class="label">Your Voting Link</p>
                                <a href="{voting_url}" class="link">{voting_url}</a>
                            </div>
                            <div class="tips-section">
                                <h3>How to Win</h3>
                                <div class="tip">
                                    <span class="tip-icon">1.</span>
                                    <div><strong>Share Your Link</strong> — Share your voting link with friends, family, and followers</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">2.</span>
                                    <div><strong>Social Media</strong> — Post on WhatsApp, Instagram, Facebook, and Twitter</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">3.</span>
                                    <div><strong>Community Engagement</strong> — Ask your community to vote for you</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">4.</span>
                                    <div><strong>Email Campaign</strong> — Send your link to your email contacts</div>
                                </div>
                                <div class="tip">
                                    <span class="tip-icon">5.</span>
                                    <div><strong>Vote Multiple Times</strong> — Unlimited voting allowed; encourage supporters to vote multiple times</div>
                                </div>
                            </div>
                            <div class="btn-container">
                                <a href="{voting_url}" class="btn-vote">Start Getting Votes</a>
                            </div>
                        </div>
                        <div class="footer">
                            <p>&copy; {timezone.now().year} Pinnacle Excellence Awards Africa. All rights reserved.</p>
                            <p class="tagline">Celebrating Excellence. Inspiring Impact. Honouring Greatness.</p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return send_email(
        recipient_email=nomination.nominator_email,
        subject=subject,
        html_message=html_message,
        text_message=None,
        email_type='nomination_confirmation',
        nominee=nominee
    )


def send_bulk_voting_links(nominees, request=None):
    """
    Send voting links to multiple nominees at once
    Returns: (success_count, failed_count, failed_list)
    """
    success_count = 0
    failed_count = 0
    failed_list = []
    
    for nominee in nominees:
        if nominee.email and not nominee.voting_email_sent:
            success, message = send_voting_link_email(nominee, request)
            if success:
                nominee.voting_email_sent = True
                nominee.voting_email_sent_at = timezone.now()
                nominee.save()
                success_count += 1
            else:
                failed_count += 1
                failed_list.append({
                    'nominee_id': nominee.id,
                    'name': nominee.name,
                    'email': nominee.email,
                    'error': message
                })
        elif nominee.voting_email_sent:
            # Already sent
            pass
        else:
            failed_count += 1
            failed_list.append({
                'nominee_id': nominee.id,
                'name': nominee.name,
                'email': nominee.email or 'No Email',
                'error': 'No email address'
            })
    
    return success_count, failed_count, failed_list