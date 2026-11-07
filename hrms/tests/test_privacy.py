from unittest.mock import patch

import frappe
from frappe.tests import IntegrationTestCase

from hrms.privacy import SYSTEM_SETTINGS, apply_privacy


class TestPrivacy(IntegrationTestCase):
	def test_legacy_system_settings_do_not_block_privacy_migration(self):
		original = {
			field: frappe.db.get_single_value("System Settings", field)
			for field in ("frequency", *SYSTEM_SETTINGS)
		}
		try:
			frappe.db.set_single_value("System Settings", "frequency", "Weekly")
			frappe.db.set_single_value("System Settings", "enable_telemetry", 1)
			frappe.db.set_single_value("System Settings", "disable_system_update_notification", 0)
			frappe.clear_cache()

			with patch("hrms.privacy.OUTBOUND_JOBS", ()):
				apply_privacy()

			for field, value in SYSTEM_SETTINGS.items():
				self.assertEqual(int(frappe.db.get_single_value("System Settings", field)), value)
			self.assertEqual(frappe.db.get_single_value("System Settings", "frequency"), "Weekly")
		finally:
			for field, value in original.items():
				frappe.db.set_single_value("System Settings", field, value)
			# apply_privacy commits; persist the restoration for subsequent tests.
			frappe.db.commit()  # nosemgrep
			frappe.clear_cache()
