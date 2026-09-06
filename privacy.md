---
title: Attest privacy policy
---

# Attest privacy policy

Effective 6 September 2026.

Attest ("the app") is published on the Atlassian Marketplace by its developer ("we").
This policy explains what the app processes and stores, where, and for how long.

## What the app reads

To compute who has access to a Jira project or Confluence space, the app reads, from your
own Atlassian site and only while it is installed there:

- the list of user accounts on the site (account id, display name, account type, active flag);
- groups and group membership;
- Jira project roles and their members, permission schemes, and application (licence) roles;
- Confluence space permissions, space roles and role assignments, and page restrictions;
- the list of projects and spaces.

The app does not read issue content, page content, comments, attachments, or email
addresses.

## What the app stores

The app stores, in Atlassian-hosted Forge SQL storage attached to your site:

- **Snapshots**: the access data listed above at a point in time, so that a review can be
  reproduced later exactly as the reviewer saw it.
- **Campaigns, assignments and decisions**: which project or space was reviewed, by whom,
  each keep / revoke / exception decision, the reason given, the reviewer's account id and a
  UTC timestamp.
- **An audit log** of campaign events.
- **A record of which site-side data calls were made** to build each snapshot (endpoint,
  status, duration; no payloads).

The app stores personal data only in the form of Atlassian account ids and display names,
which are needed to say who has access and who made a decision. It stores no email
addresses, passwords, or credentials.

## Where data is stored and who can reach it

All storage is Atlassian-hosted Forge storage in the region of your Atlassian site. The
app makes no calls to any server outside Atlassian: it has no external egress and
qualifies for Atlassian's "Runs on Atlassian" programme. We, the developer, cannot read
your data: there is no developer-side database, dashboard, or export.

## Optional Jira issues

If an administrator enables it for a campaign, the app creates one Jira issue per review
in a project they choose, so Jira's own notifications remind the reviewer. These issues
contain the project or space name, the campaign name, the due date and a link, and are
resolved by the app when the review is signed off. They stay in your Jira like any other
issue.

## Retention

- Snapshots not referenced by any campaign are deleted 90 days after they were taken.
- Campaigns, assignments, decisions and the audit log are kept for as long as the app is
  installed, because they are your audit evidence.
- When you uninstall the app, Atlassian soft-deletes all of its storage and permanently
  deletes it after Atlassian's Forge retention period (28 days at the time of writing).
  Data can be relinked to a reinstallation only at your request within that period.

## Sharing

The app shares no data with any third party. It sends no analytics.

## Your rights and contact

Because the app stores nothing outside your own Atlassian site, requests to access, correct
or delete data are fulfilled by your own Atlassian administrators using the app or by
uninstalling it. Questions about this policy: see the [support page](support.html).

## Changes

Material changes to this policy will be dated at the top of this page.
