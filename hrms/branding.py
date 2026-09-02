"""MetaCarat branding for the Desk.

The mobile app, roster and logo files are code and ship with the app. The Desk login
logo, navbar logo, favicon and app name are *settings* (rows in Website Settings and
Navbar Settings) stored per site, so a fresh site would fall back to Frappe defaults.
These hooks write them on install and fill any blanks on migrate.
"""

import frappe

APP_NAME = "MetaCarat HR"
LOGO = "/assets/hrms/images/frappe-hr-logo.svg"
FAVICON = "/assets/hrms/manifest/favicon-196.png"

BRANDING = {
	"Website Settings": {
		"app_name": APP_NAME,
		"app_logo": LOGO,
		"favicon": FAVICON,
		"splash_image": LOGO,
	},
	"Navbar Settings": {
		"app_logo": LOGO,
	},
}


def apply_branding(force: bool = False):
	"""Write the Desk branding settings.

	force=True overwrites every field (install). force=False only fills fields that are
	empty (migrate), so a value an admin changed by hand is left alone.
	"""
	for doctype, values in BRANDING.items():
		doc = frappe.get_single(doctype)
		changed = False
		for fieldname, value in values.items():
			if force or not doc.get(fieldname):
				if doc.get(fieldname) != value:
					doc.set(fieldname, value)
					changed = True
		if changed:
			doc.flags.ignore_permissions = True
			doc.save()

	frappe.db.commit()
	frappe.clear_cache()


def after_install():
	apply_branding(force=True)


def after_migrate():
	apply_branding(force=False)
