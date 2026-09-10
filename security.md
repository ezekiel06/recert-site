---
title: Recert security policy
---

# Recert security policy

Effective 10 September 2026.

This page describes how Recert ("the app") is built, hosted and operated to keep customer
data safe, and how to report a security problem. It is the security policy referenced on
the app's Atlassian Marketplace listing. What the app reads and stores is described in the
[privacy policy](privacy.html).

## 1. Summary

- The app runs entirely inside Atlassian's Forge platform ("Runs on Atlassian"). It has no
  servers, databases or accounts of its own outside Atlassian.
- The app makes no network calls to any destination other than the customer's own
  Atlassian site. It declares no external egress and passes Atlassian's eligibility check
  for every release.
- The developer cannot read customer data. There is no developer-side database, dashboard,
  log export or support tool that exposes it.
- The app reads Jira and Confluence with the minimum scopes needed and never changes group
  membership, project roles, space permissions or permission schemes.

## 2. Hosting and architecture

The app is an Atlassian Forge application. All of its code executes in Forge's sandboxed
runtime and all of its data is stored in Forge SQL storage that Atlassian provisions per
installation, in the same region as the customer's Atlassian site.

Atlassian operates, patches and monitors this infrastructure. Its controls are described in
the [Atlassian Trust Center](https://www.atlassian.com/trust) and the
[Forge security documentation](https://developer.atlassian.com/platform/forge/security/).
The app inherits those controls; it adds no infrastructure of its own.

Availability of the app follows the availability of the customer's Atlassian site and the
Forge platform. Atlassian publishes platform status at
[status.atlassian.com](https://status.atlassian.com). See the
[support and service statement](sla.html) for support hours and response targets.

## 3. Data handling

The app stores only what a reviewer needs to reproduce and evidence an access review:
point-in-time access snapshots, campaign definitions, assignments, decisions and an audit
log. The only personal data it stores are Atlassian account ids and display names. It stores
no email addresses, passwords, tokens or credentials of any kind.

- **Encryption in transit:** every call the app makes is to Atlassian's own REST APIs over
  HTTPS, from inside Atlassian's network. There is no traffic to third parties.
- **Encryption at rest:** Forge storage is encrypted at rest by Atlassian. The developer
  holds no encryption keys and cannot access the underlying storage.
- **Data residency:** data stays in the region of the customer's Atlassian site and is never
  copied elsewhere.
- **Tenant isolation:** each installation has its own isolated storage. No installation can
  read another's data.
- **Retention and deletion:** described in the [privacy policy](privacy.html). Unreferenced
  snapshots are deleted after 90 days. On uninstall, Atlassian soft-deletes the app's storage
  and permanently deletes it after the Forge retention period.
- **Personal-data reporting:** the app polls Atlassian's personal-data reporting API daily
  and updates or erases stored display names when Atlassian reports that an account has
  changed or been closed, as the Forge user-privacy guide requires.

## 4. Access control inside the app

- **Administrator actions:** only Jira administrators can run snapshots, create campaigns,
  configure reminders, or reopen a signed-off review. The app checks this with Jira's own
  permission service on every request, as the acting user, and never caches the result.
- **Reviewer actions:** a review can be decided only by its assigned owner or a Jira
  administrator. Every decision records the deciding account and a UTC timestamp.
- **Immutable evidence:** once a review is signed off its decisions cannot be edited. A
  reopen creates a new version and keeps the earlier decisions visible as superseded, so
  evidence can never be silently changed.
- **Read as the app, not as the user:** access data is read using the app's own identity so
  that a review shows the same result regardless of who opens it.
- **Writes:** the only write the app performs in the customer's products is creating and
  resolving optional reminder issues in a Jira project the administrator chooses, and only
  when an administrator has turned that feature on.

## 5. Scopes and least privilege

The app requests only the read scopes required to compute effective access, plus the write
scope needed to create reminder issues. The full list is shown on the Marketplace listing
and must be approved by a site administrator at install time. Any change to the app's scopes
is released as a new major version, which administrators must explicitly approve before it
takes effect on their site.

The app cannot change group membership, project roles or permission schemes. Revocations
decided in a review are recorded as evidence and carried out by the customer's own
administrators using Atlassian's tools.

## 6. Developer access to customer data

The developer has no access to any customer installation's data. Forge does not expose
installation storage to the app vendor, and the app provides no export, telemetry or
analytics channel back to the developer. Application logs available to the developer contain
operational information (timings, counts, error codes) and no customer data.

## 7. Secure development

- The access-resolution logic is pure, isolated from all I/O, and covered by unit,
  property-based and end-to-end tests that run on every change.
- Resolver output is verified against Jira's own permission-check API on a test site before
  each release.
- Every release runs Atlassian's Forge lint and "Runs on Atlassian" eligibility checks
  before deployment.
- Dependencies are pinned and reviewed for known vulnerabilities before each release.
- Development, staging and production environments are separate Forge environments;
  customers only ever receive production builds.
- The app source is maintained in a private repository with access limited to the developer.

## 8. Reporting a vulnerability

Please report security issues privately. Do not open a public issue.

- **Email:** the security contact address published on the Marketplace listing.
- **GitHub:** private vulnerability reporting on
  [github.com/ezekiel06/recert-site](https://github.com/ezekiel06/recert-site/security)
  ("Security" tab, "Report a vulnerability").

We acknowledge reports within two business days and keep the reporter informed until the
issue is resolved. Good-faith research that avoids accessing other customers' data and
avoids service disruption will not be met with legal action.

## 9. Vulnerability handling

Confirmed vulnerabilities are triaged by severity using the CVSS scale and fixed on the
following targets:

| Severity | Target |
|---|---|
| Critical | Fix released within 14 days |
| High | Fix released within 30 days |
| Medium and low | Fix in the next regular release |

Fixes ship as a new app version on the Marketplace. Because the app is Forge-hosted, fixes
reach every installation automatically for minor versions, and on administrator approval for
major versions.

## 10. Incident response

If the developer becomes aware of a security incident affecting customer data, we will:

1. Contain the issue, including withdrawing the affected version from the Marketplace if
   needed.
2. Notify affected customers through their Atlassian site administrators without undue
   delay and no later than 72 hours after confirmation, describing what happened, what data
   was involved and what we have done.
3. Notify Atlassian through the Marketplace partner channels.
4. Publish a post-incident summary on this site.

## 11. Compliance

The app holds no certifications of its own. It relies on Atlassian's certifications for the
Forge platform (see the [Atlassian Trust Center](https://www.atlassian.com/trust)). The app's
answers to Atlassian's Privacy & Security questionnaire are published on its Marketplace
listing.

## 12. Changes to this policy

Material changes are dated at the top of this page. Questions about this policy go to the
security contact on the Marketplace listing or the [support page](support.html).
