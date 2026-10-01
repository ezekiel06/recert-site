---
title: Who has access to a Jira project? A checklist for Jira Cloud
description: The Jira People screen can say a project has no one in it while everyone on the site can open it. Here is every way access reaches a Jira Cloud project, and how to check each one.
---

# Who has access to a Jira project?

*A checklist for Jira Cloud admins. Jira now calls projects "spaces"; this page uses both words.*

Open a company-managed project, go to **Space settings → People**, and Jira may tell you:

> There is no one in this space.

On a fresh site we set up to test this, that was exactly what it said. Then we opened
**Space settings → Permissions**: the **Browse Projects** permission was granted to
**Application access (Any logged in user)**. In other words, *everyone with Jira on the site*
could open the project the People screen said was empty.

That gap is the reason a Jira access review done from the People screen looks complete and is
not. Below is every route access takes into a Jira Cloud project, and where to look for each.

## Company-managed projects: five routes in

Access to a company-managed project is decided by its **permission scheme**
(**Space settings → Permissions**). The permission that matters for "can this person see the
project" is **Browse Projects**. Each grant on it can be one of these:

| Grant type | Who it actually means | Where you see the people |
|---|---|---|
| Project role (a user in the role) | That person | Space settings → People |
| Project role (a group in the role) | Everyone in the group | People shows the group as one line; members are in admin.atlassian.com → Groups |
| Group | Everyone in that group | Not on the People screen at all; admin.atlassian.com → Groups |
| Application access | Everyone licensed for the product, e.g. *Any logged in user* | Not on the People screen; the product's access groups in admin.atlassian.com |
| Single user | That person | Only in the permission scheme |
| Reporter, assignee, user or group picker field | People named on a particular work item, for that item only | Nowhere as a list; it changes as work items change |

The last row is **conditional** access: it only covers the work items where the person is named.
Treat it separately in a review; it is not membership.

Permission schemes are usually **shared between many projects**. Removing a group from a scheme,
or a person from a group, changes access to every project that uses it, so those decisions belong
to whoever owns the scheme or the group, not to one project lead.

## Team-managed projects: the access level first

Team-managed projects have no permission scheme. Look at **Space settings → Access**. The access
level shown at the top decides most of the answer
([Atlassian's definitions](https://support.atlassian.com/jira-software-cloud/docs/manage-how-people-access-your-team-managed-project/)):

- **Open**: anyone on the Jira site can view, create and edit work items.
- **Limited**: anyone on the site can view and comment, but not create or edit.
- **Private**: only Jira admins and the people added to the space can see it.

So an **Open** team-managed project with one person listed on its Access screen is, in practice,
open to everyone on the site. Our test project showed exactly that.

## Three things that skew the count

1. **App accounts.** Marketplace apps and integrations get their own accounts, and they often
   hold Browse Projects through the `atlassian-addons-project-access` role. On our test site, 11
   of the 12 accounts that could browse a project were apps, not people. Leave them out of a
   human access review, or reviewers will be asked to approve robots.
2. **Customers.** Jira Service Management portal customers are a separate account type; they are
   not agents and should be reviewed differently.
3. **Deactivated accounts** still appear in groups. They cannot log in, so a review should show
   them but not ask anyone to decide on them.

## Doing this by hand

For one project: read the Browse Projects row of the permission scheme, expand every group and
role in it into people, drop app and deactivated accounts, and note *why* each remaining person
has access. That last part is what makes the list useful: it tells the reviewer what to change
if the answer is "remove".

For one project it is an afternoon. For every project, every quarter, it is the job auditors
expect you to have done and few teams finish.

## What Recert does

[Recert](https://marketplace.atlassian.com/apps/2953269953) is a Jira Cloud app that does
the expansion above for every Jira project and Confluence space: it lists each person who
can browse or administer, with the route (scheme grant, role, group, licence class) that gives
them access. It then sends one review per project to its lead, records keep / revoke /
exception decisions with a reason, and exports the evidence. It runs entirely on Atlassian's
infrastructure.

See the [getting-started guide](getting-started.html), or the companion page on
[what auditors ask for in a Jira and Confluence access review](access-review-evidence.html).
