---
title: Attest security
---

# Attest security

- **Runs on Atlassian**: all compute and storage is Atlassian-hosted; the app declares no
  external egress. Verified with Atlassian's eligibility check for every release.
- **Least privilege**: the app reads Jira and Confluence as its own app identity with the
  scopes listed on its Marketplace listing. It never changes group membership, project
  roles or permission schemes. The only write it performs is creating and resolving the
  optional review-reminder Jira issues, and only when an administrator turns that on.
- **Who can do what**: only Jira administrators can create campaigns or reopen a signed
  review; the app checks this with Jira's own permission service on every request, as the
  acting user. Reviews can be decided only by the assigned owner or a Jira administrator,
  and every decision records who made it.
- **Immutable evidence**: once a review is signed off, its decisions cannot be edited. A
  reopen creates a new version and keeps the earlier decisions visible as superseded.
- **Reporting a security issue**: see the [support page](support.html). Please do not file
  security reports as public issues.
