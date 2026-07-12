# Site Map — 9_project-management

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Login** — `pages/01_Login.png` · `pages/01_Login.json`
- **02_User_Dashboard** — `pages/02_User_Dashboard.png` · `pages/02_User_Dashboard.json`
- **03_User_Task** — `pages/03_User_Task.png` · `pages/03_User_Task.json`
- **04_User_Projects** — `pages/04_User_Projects.png` · `pages/04_User_Projects.json`
- **05_User_Project_Details** — `pages/05_User_Project_Details.png` · `pages/05_User_Project_Details.json`
- **06_User_Profile** — `pages/06_User_Profile.png` · `pages/06_User_Profile.json`
- **07_User_Task_Kanban_board** — `pages/07_User_Task_Kanban_board.png` · `pages/07_User_Task_Kanban_board.json`
- **08_User_WorkLog** — `pages/08_User_WorkLog.png` · `pages/08_User_WorkLog.json`
- **09_User_Performance_Report** — `pages/09_User_Performance_Report.png` · `pages/09_User_Performance_Report.json`
- **10_User_Task_PopUp** — `pages/10_User_Task_PopUp.png` · `pages/10_User_Task_PopUp.json`

## Navigation graph

```
01_Login
  └─→ 02_User_Dashboard

02_User_Dashboard
  ├─→ 03_User_Task
  ├─→ 06_User_Profile
  ├─→ 08_User_WorkLog
  └─→ 09_User_Performance_Report

03_User_Task
  ├─→ 04_User_Projects
  └─→ 07_User_Task_Kanban_board

04_User_Projects
  ├─→ 03_User_Task
  ├─→ 05_User_Project_Details (x6)
  ├─→ 06_User_Profile
  ├─→ 08_User_WorkLog
  └─→ 09_User_Performance_Report

05_User_Project_Details
  ├─→ 03_User_Task
  ├─→ 04_User_Projects
  ├─→ 06_User_Profile
  ├─→ 08_User_WorkLog
  ├─→ 09_User_Performance_Report
  └─→ 10_User_Task_PopUp (x6)

06_User_Profile
  ├─→ 03_User_Task
  ├─→ 04_User_Projects
  ├─→ 05_User_Project_Details (x9)
  ├─→ 08_User_WorkLog
  └─→ 09_User_Performance_Report

07_User_Task_Kanban_board
  ├─→ 04_User_Projects
  ├─→ 06_User_Profile
  ├─→ 08_User_WorkLog
  └─→ 09_User_Performance_Report

08_User_WorkLog
  ├─→ 03_User_Task
  ├─→ 04_User_Projects
  ├─→ 06_User_Profile
  └─→ 09_User_Performance_Report

09_User_Performance_Report
  ├─→ 03_User_Task
  ├─→ 04_User_Projects
  ├─→ 06_User_Profile
  └─→ 08_User_WorkLog

# pages with no outgoing navigate edges:
  · 10_User_Task_PopUp
```

## Per-page navigation

### 01_Login
_6 annotations · 1 navigate_

Goes to:
- **02_User_Dashboard**

### 02_User_Dashboard
_10 annotations · 4 navigate_

Goes to:
- **03_User_Task**
- **06_User_Profile**
- **08_User_WorkLog**
- **09_User_Performance_Report**

Reached from: 01_Login

### 03_User_Task
_3 annotations · 2 navigate_

Goes to:
- **04_User_Projects**
- **07_User_Task_Kanban_board**

Reached from: 02_User_Dashboard, 04_User_Projects, 05_User_Project_Details, 06_User_Profile, 08_User_WorkLog, 09_User_Performance_Report

### 04_User_Projects
_20 annotations · 10 navigate_

Goes to:
- **03_User_Task**
- **05_User_Project_Details** (x6)
- **06_User_Profile**
- **08_User_WorkLog**
- **09_User_Performance_Report**

Reached from: 03_User_Task, 05_User_Project_Details, 06_User_Profile, 07_User_Task_Kanban_board, 08_User_WorkLog, 09_User_Performance_Report

### 05_User_Project_Details
_13 annotations · 11 navigate_

Goes to:
- **03_User_Task**
- **04_User_Projects**
- **06_User_Profile**
- **08_User_WorkLog**
- **09_User_Performance_Report**
- **10_User_Task_PopUp** (x6)

Reached from: 04_User_Projects, 06_User_Profile

### 06_User_Profile
_34 annotations · 13 navigate_

Goes to:
- **03_User_Task**
- **04_User_Projects**
- **05_User_Project_Details** (x9)
- **08_User_WorkLog**
- **09_User_Performance_Report**

Reached from: 02_User_Dashboard, 04_User_Projects, 05_User_Project_Details, 07_User_Task_Kanban_board, 08_User_WorkLog, 09_User_Performance_Report

### 07_User_Task_Kanban_board
_17 annotations · 4 navigate_

Goes to:
- **04_User_Projects**
- **06_User_Profile**
- **08_User_WorkLog**
- **09_User_Performance_Report**

Reached from: 03_User_Task

### 08_User_WorkLog
_8 annotations · 4 navigate_

Goes to:
- **03_User_Task**
- **04_User_Projects**
- **06_User_Profile**
- **09_User_Performance_Report**

Reached from: 02_User_Dashboard, 04_User_Projects, 05_User_Project_Details, 06_User_Profile, 07_User_Task_Kanban_board, 09_User_Performance_Report

### 09_User_Performance_Report
_10 annotations · 4 navigate_

Goes to:
- **03_User_Task**
- **04_User_Projects**
- **06_User_Profile**
- **08_User_WorkLog**

Reached from: 02_User_Dashboard, 04_User_Projects, 05_User_Project_Details, 06_User_Profile, 07_User_Task_Kanban_board, 08_User_WorkLog

### 10_User_Task_PopUp
_6 annotations_

Goes to: _(none)_

Reached from: 05_User_Project_Details
