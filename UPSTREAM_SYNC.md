# Updating the MetaCarat HR fork

This fork follows Frappe HR's `version-16` releases. `origin/version-16` contains
our branding, privacy, PWA, and translation changes. `upstream` points to
`frappe/hrms`. Keep Frappe Framework and ERPNext on compatible version 16
releases when upgrading HRMS.

## For each upstream release

1. Finish or set aside local work and confirm `git status` is clean. Preserve
   untracked files too; a normal `git stash` does not include them.
2. Run `git fetch upstream version-16 --tags` and check the newest `v16.x.y`
   release on the upstream releases page. Merge a release tag, not an
   unreleased branch tip.
3. Create a branch from the fork's current `version-16` branch:

   ```sh
   git switch version-16
   git pull --ff-only origin version-16
   git switch -c sync/v16.x.y
   git merge --no-ff v16.x.y
   ```

4. Resolve conflicts while retaining intentional fork behavior. Review the
   branding, privacy, PWA, and translation changes even when Git reports no
   conflict. Check `git diff --check` and run the relevant tests and builds.
5. Push the update branch and open a pull request into **this fork's**
   `version-16` branch. Record the release tag, local changes, test results,
   and any deployment steps in the pull request.
6. On a staging site with a production-like backup, update the compatible
   Frappe/ERPNext/HRMS versions, build assets, and run `bench --site <site>
   migrate`. Exercise payroll, leave, attendance, PWA, and the custom branding
   and privacy behavior. Back up production before deploying the approved
   release and repeat the migration there.

Do not rebase or force-push the shared `version-16` branch. Use merge commits so
the fork's changes and each upstream update remain visible.

## New company-specific features

Put custom fields, form scripts, document event hooks, and reports in a separate
Frappe app when possible. Export its fixtures and customizations into that app's
own repository. Keep changes in this HRMS fork only for behavior that cannot be
implemented through a supported extension point. Review each direct HRMS patch
after an upstream release changes the same area.
