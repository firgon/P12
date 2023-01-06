from django.contrib.admin import AdminSite


class EpicEventAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = "Managers' website"

    # Text to put in each page's <h1> (and above login form).
    site_header = 'Epic Events'

    # Text to put at the top of the admin index page.
    index_title = 'Users Management'


admin_site = EpicEventAdminSite("administration")
