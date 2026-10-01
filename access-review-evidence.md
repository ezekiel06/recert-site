---
title: SOC 2 and ISO 27001 user access reviews for Jira and Confluence
description: What an auditor expects to see from a periodic user access review of Jira projects and Confluence spaces, and the mistakes that make the evidence fail.
---

# SOC 2 and ISO 27001 user access reviews for Jira and Confluence

If your company is going through SOC 2 or ISO 27001, at some point the auditor asks for
evidence that access to your systems is **reviewed periodically**. ISO 27001:2022 says it
directly in Annex A control 5.18, *Access rights*; SOC 2 auditors test it under the logical
access criteria (CC6). Jira and Confluence usually end up in scope because that is where
product plans, customer tickets and internal documentation live.

This page is about what that evidence has to contain, and where Jira and Confluence make it hard.

## What the evidence needs to show

For each review period, and for each Jira project and Confluence space in scope:

1. **A dated list of who had access.** Taken at a known point in time, and complete: people
   who get in through groups and permission schemes count, not only the ones listed by name.
2. **Why each person had access.** The group, role or scheme grant. Without it, a reviewer
   cannot act on "remove", and the auditor cannot tell whether the list is complete.
3. **Who reviewed it.** Normally the owner of the project or space, not one admin for everything.
4. **A decision per person.** Keep, revoke, or an accepted exception, with a reason for the last two.
5. **Proof that revokes happened.** A ticket, a change record, or a later snapshot showing the
   person gone.
6. **Sign-off.** That the review was completed, by whom, and when.

## Where Jira and Confluence make this hard

- **The People screens are not the access list.** A Jira project's People screen can say "There
  is no one in this space" while everyone on the site can open it. See
  [who has access to a Jira project](jira-who-has-access.html) for every route in.
- **Groups hide people.** Most access arrives through groups that are shared across many
  projects and spaces. Expanding them is the bulk of the work.
- **App accounts inflate the list.** Integrations hold their own accounts with project access;
  mixing them into a human review produces a wrong document.
- **History expires.** The organization audit log keeps 180 days. If you did not record who had
  access last quarter, you cannot reconstruct it reliably afterwards, so the snapshot has to be
  taken at review time and kept.
- **Two products, two permission models.** Confluence spaces use space permissions or space
  roles, with their own groups and licence classes; a review covering only Jira leaves half the
  scope out.

## Common reasons this evidence fails

- A spreadsheet with names but no date, or no source for each name.
- One administrator approving every project, with no sign of the owners' involvement.
- "Revoke" decisions with nothing to show they were carried out.
- A list that only includes directly-named users, so the auditor's own sample finds someone missing.

## What Recert does

[Recert](https://marketplace.atlassian.com/apps/2953269953) produces the evidence above for
Jira projects and Confluence spaces in one review. It snapshots effective access, including
access through groups, roles, permission schemes and licence classes, leaving app accounts out. It
routes one review to each project lead or space administrator, records keep / revoke / exception
decisions with reasons, tracks sign-off, and exports the result as CSV files attached to a Jira
issue. It runs entirely on Atlassian's infrastructure; no data leaves your site.

See the [getting-started guide](getting-started.html).
