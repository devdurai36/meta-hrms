"""Keep the site from contacting Frappe's servers.

Usage telemetry ("pulse") is already inert on self-hosted sites because it needs an API
key in site config, but two scheduled jobs still reach out weekly: the update check
(GitHub releases API) and the changelog feed (frappe.io). Neither carries site data,
yet both disclose the server's address. These hooks switch them off on install and keep
them off across migrations, which re-sync scheduled jobs.
"""

import frappe

OUTBOUND_JOBS = (
	"frappe.utils.change_log.check_for_update",
	"frappe.desk.doctype.changelog_feed.changelog_feed.fetch_changelog_feed",
)

SYSTEM_SETTINGS = {
	"enable_telemetry": 0,
	"disable_system_update_notification": 1,
}


def apply_privacy():
	settings = frappe.get_single("System Settings")
	changed = False
	for fieldname, value in SYSTEM_SETTINGS.items():
		if settings.get(fieldname) != value:
			settings.set(fieldname, value)
			changed = True
	if changed:
		settings.flags.ignore_permissions = True
		settings.flags.ignore_mandatory = True
		settings.save()

	for method in OUTBOUND_JOBS:
		for name in frappe.get_all("Scheduled Job Type", filters={"method": method, "stopped": 0}, pluck="name"):
			frappe.db.set_value("Scheduled Job Type", name, "stopped", 1)

	frappe.db.commit()
	frappe.clear_cache()


def after_install():
	apply_privacy()


def after_migrate():
	apply_privacy()
