# Lab 2 – Agile Backlog Creation & Sprint Simulation in Jira

**Problem Statement #29 – Municipal Infrastructure Damage Reporting App**  
**Student:** Aditya Shet  
**SRN:** PES2UG24AM015  
**Jira Space:** Damage Reporting App (DRA)  

The backlog is derived from the Lab 1 requirements (FR-001 to FR-005, NFR-001, and NFR-002).

---

## 1. Backlog Summary

| Epic | User Stories (Story Points) | From Lab 1 |
|---|---|---|
| **EPIC1 Damage Reporting** | Auto-detect report location (5), Choose damage type and attach photo (3), Submit report offline (8) | FR-001, FR-002, NFR-001 |
| **EPIC2 Automated Screening** | Flag duplicate reports (8), Reject incomplete or out-of-city reports (3) | FR-003 |
| **EPIC3 Routing and Resolution** | Route valid report to department (5), Assign engineer and update status (3), Audit log of status changes (5) | FR-004, NFR-002 |
| **EPIC4 Status Tracking and Notifications** | Track report status (2), Notify on status change (3) | FR-005 |

**Sprint Plan:**
- **Total:** 45 story points on the Fibonacci scale (1, 2, 3, 5, 8).
- **Sprint 1 (24 pts, 5 stories, all High priority):** Citizen submission flow (locate, categorize, photo), automated screening, and department routing.
- **Sprint 2 (21 pts, 5 stories):** Offline submission and sync, officer workflow with audit trail, citizen status tracking, and automated status notifications.
- **Sprint Duration:** 1 week per sprint (12–19 Nov 2026).

---

## 2. Reflection

### 1. Did your estimations reflect the actual effort?
Not in a way the sprint could measure. The points were set by relative complexity and uncertainty: offline sync and duplicate detection got 8 because of sync conflicts and deciding when two reports describe the same damage, and status tracking got 2. Because the sprint was simulated, every story moved to Done within minutes, so a 2-point and an 8-point story took the same real time. The relative ordering still seems sound, but checking it would need real development time, for example by comparing hours logged per point across sprints.

### 2. Was your backlog well-prioritized?
Mostly. Sprint 1 held the High-priority stories that form the core flow (locate, describe, screen and route a report), so it delivers something usable on its own. Sprint 2 held the stories that depend on that flow, plus the two Medium-priority citizen-feedback stories. One weakness: “Submit report offline” is High priority (NFR-001), but it was deferred to Sprint 2 because it was the largest and riskiest story and builds on the submission flow. In hindsight it could have been split, for example local saving in Sprint 1 and auto-sync in Sprint 2, so that part of a High-priority item shipped earlier.

### 3. How did your simulated sprint align with your plan?
Scope matched the plan exactly. Both sprints completed all committed stories (24/24 and 21/21 points, 100% done), with no carry-over or scope change, and every epic reached 100%. The timing didn’t match: work planned for a week finished on day one, because cards were moved rather than built.

### 4. What insights did the burndown chart give about your team’s capacity?
In both sprints the remaining-work line dropped straight to 0% on the first day, far below the grey guideline, which falls linearly to 19 Nov. Read literally, the chart says the team finished early and under-committed, so it could take on more work. It also shows the “sharp drop” pattern, which signals that stories were not tracked incrementally. In a real sprint, the line should step down as each story is finished, and staying close to the guideline would confirm a velocity of roughly 21–24 points per week for planning future sprints.

---

## 3. Deliverables

| File | Description |
|---|---|
| [Lab2_Submission.pdf](file:///c:/Users/Admin/Desktop/lab2/Lab2_Submission.pdf) | Complete lab report with backlog summary, reflection answers, and embedded Jira screenshots |
| [screenshots/1_backlog_epics_story_points.png](file:///c:/Users/Admin/Desktop/lab2/screenshots/1_backlog_epics_story_points.png) | Backlog view showing Epics panel, 10 user stories, priorities, and 45 story points |
| [screenshots/2_sprint1_active_board.png](file:///c:/Users/Admin/Desktop/lab2/screenshots/2_sprint1_active_board.png) | Sprint 1 active board at start (5 stories in To Do) |
| [screenshots/3_sprint1_burndown.png](file:///c:/Users/Admin/Desktop/lab2/screenshots/3_sprint1_burndown.png) | Sprint 1 completed: board all Done, insights burndown chart (24/24 points done) |
| [screenshots/4_sprint2_burndown.png](file:///c:/Users/Admin/Desktop/lab2/screenshots/4_sprint2_burndown.png) | Sprint 2 completed: board all Done, insights burndown chart (21/21 points done, all epics 100%) |
| [Jira_Backlog_Import.csv](file:///c:/Users/Admin/Desktop/lab2/Jira_Backlog_Import.csv) | Jira CSV backlog import file formatted with issues, descriptions, points, epics, and sprints |
