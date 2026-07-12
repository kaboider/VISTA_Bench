# Site Map — 3_job-board

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Landing_page** — `pages/01_Landing_page.png` · `pages/01_Landing_page.json`
- **02_Find_jobs** — `pages/02_Find_jobs.png` · `pages/02_Find_jobs.json`
- **03_Browse_Companies** — `pages/03_Browse_Companies.png` · `pages/03_Browse_Companies.json`
- **04_Search_Companies_Results** — `pages/04_Search_Companies_Results.png` · `pages/04_Search_Companies_Results.json`
- **05_Job_Descriptions** — `pages/05_Job_Descriptions.png` · `pages/05_Job_Descriptions.json`
- **06_Company_Profile** — `pages/06_Company_Profile.png` · `pages/06_Company_Profile.json`
- **07_Sign_Up** — `pages/07_Sign_Up.png` · `pages/07_Sign_Up.json`
- **08_Log_in** — `pages/08_Log_in.png` · `pages/08_Log_in.json`
- **09_Dashboard_Applicant** — `pages/09_Dashboard_Applicant.png` · `pages/09_Dashboard_Applicant.json`
- **10_Dashboard_-_Message** — `pages/10_Dashboard_-_Message.png` · `pages/10_Dashboard_-_Message.json`
- **11_Dashboard_-_Applications_History** — `pages/11_Dashboard_-_Applications_History.png` · `pages/11_Dashboard_-_Applications_History.json`
- **12_Dashboard_-_Find_Jobs** — `pages/12_Dashboard_-_Find_Jobs.png` · `pages/12_Dashboard_-_Find_Jobs.json`
- **13_Dashboard_-_Job_Descriptions** — `pages/13_Dashboard_-_Job_Descriptions.png` · `pages/13_Dashboard_-_Job_Descriptions.json`
- **14_Dashboard_-_Browse_Companies** — `pages/14_Dashboard_-_Browse_Companies.png` · `pages/14_Dashboard_-_Browse_Companies.json`
- **15_Dashboard_-_Profile** — `pages/15_Dashboard_-_Profile.png` · `pages/15_Dashboard_-_Profile.json`
- **16_Dashboard_-_Settings** — `pages/16_Dashboard_-_Settings.png` · `pages/16_Dashboard_-_Settings.json`
- **17_Dashboard_-_Settings** — `pages/17_Dashboard_-_Settings.png` · `pages/17_Dashboard_-_Settings.json`
- **18_Dashboard_-_Settings** — `pages/18_Dashboard_-_Settings.png` · `pages/18_Dashboard_-_Settings.json`
- **19_Dashboard_-_Help** — `pages/19_Dashboard_-_Help.png` · `pages/19_Dashboard_-_Help.json`

## Navigation graph

```
01_Landing_page
  ├─→ 02_Find_jobs (x4)
  ├─→ 03_Browse_Companies (x10)
  ├─→ 05_Job_Descriptions (x16)
  ├─→ 07_Sign_Up (x2)
  └─→ 08_Log_in

02_Find_jobs
  ├─→ 03_Browse_Companies
  ├─→ 05_Job_Descriptions (x7)
  ├─→ 07_Sign_Up
  └─→ 08_Log_in

03_Browse_Companies
  ├─→ 02_Find_jobs
  ├─→ 06_Company_Profile (x14)
  ├─→ 07_Sign_Up
  └─→ 08_Log_in

04_Search_Companies_Results
  ├─→ 02_Find_jobs
  ├─→ 06_Company_Profile (x8)
  ├─→ 07_Sign_Up
  └─→ 08_Log_in

05_Job_Descriptions
  ├─→ 02_Find_jobs (x2)
  ├─→ 03_Browse_Companies (x2)
  ├─→ 07_Sign_Up
  └─→ 08_Log_in

06_Company_Profile
  ├─→ 02_Find_jobs
  ├─→ 05_Job_Descriptions (x8)
  ├─→ 07_Sign_Up
  └─→ 08_Log_in

07_Sign_Up
  └─→ 08_Log_in

08_Log_in
  └─→ 07_Sign_Up

09_Dashboard_Applicant
  ├─→ 01_Landing_page
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

10_Dashboard_-_Message
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 17_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

11_Dashboard_-_Applications_History
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 13_Dashboard_-_Job_Descriptions
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

12_Dashboard_-_Find_Jobs
  ├─→ 01_Landing_page
  ├─→ 05_Job_Descriptions (x7)
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

13_Dashboard_-_Job_Descriptions
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

14_Dashboard_-_Browse_Companies
  ├─→ 06_Company_Profile (x6)
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings
  └─→ 18_Dashboard_-_Settings

15_Dashboard_-_Profile
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 16_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

16_Dashboard_-_Settings
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 17_Dashboard_-_Settings
  ├─→ 18_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

17_Dashboard_-_Settings
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings (x2)
  ├─→ 18_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

18_Dashboard_-_Settings
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  ├─→ 16_Dashboard_-_Settings (x2)
  ├─→ 17_Dashboard_-_Settings
  └─→ 19_Dashboard_-_Help

19_Dashboard_-_Help
  ├─→ 01_Landing_page
  ├─→ 09_Dashboard_Applicant
  ├─→ 10_Dashboard_-_Message
  ├─→ 11_Dashboard_-_Applications_History
  ├─→ 12_Dashboard_-_Find_Jobs
  ├─→ 14_Dashboard_-_Browse_Companies
  ├─→ 15_Dashboard_-_Profile (x2)
  └─→ 16_Dashboard_-_Settings

```

## Per-page navigation

### 01_Landing_page
_37 annotations · 33 navigate_

Goes to:
- **02_Find_jobs** (x4)
- **03_Browse_Companies** (x10)
- **05_Job_Descriptions** (x16)
- **07_Sign_Up** (x2)
- **08_Log_in**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 02_Find_jobs
_46 annotations · 10 navigate_

Goes to:
- **03_Browse_Companies**
- **05_Job_Descriptions** (x7)
- **07_Sign_Up**
- **08_Log_in**

Reached from: 01_Landing_page, 03_Browse_Companies, 04_Search_Companies_Results, 05_Job_Descriptions, 06_Company_Profile

### 03_Browse_Companies
_30 annotations · 17 navigate_

Goes to:
- **02_Find_jobs**
- **06_Company_Profile** (x14)
- **07_Sign_Up**
- **08_Log_in**

Reached from: 01_Landing_page, 02_Find_jobs, 05_Job_Descriptions

### 04_Search_Companies_Results
_42 annotations · 11 navigate_

Goes to:
- **02_Find_jobs**
- **06_Company_Profile** (x8)
- **07_Sign_Up**
- **08_Log_in**

### 05_Job_Descriptions
_20 annotations · 6 navigate_

Goes to:
- **02_Find_jobs** (x2)
- **03_Browse_Companies** (x2)
- **07_Sign_Up**
- **08_Log_in**

Reached from: 01_Landing_page, 02_Find_jobs, 06_Company_Profile, 12_Dashboard_-_Find_Jobs

### 06_Company_Profile
_27 annotations · 11 navigate_

Goes to:
- **02_Find_jobs**
- **05_Job_Descriptions** (x8)
- **07_Sign_Up**
- **08_Log_in**

Reached from: 03_Browse_Companies, 04_Search_Companies_Results, 14_Dashboard_-_Browse_Companies

### 07_Sign_Up
_8 annotations · 1 navigate_

Goes to:
- **08_Log_in**

Reached from: 01_Landing_page, 02_Find_jobs, 03_Browse_Companies, 04_Search_Companies_Results, 05_Job_Descriptions, 06_Company_Profile, 08_Log_in

### 08_Log_in
_8 annotations · 1 navigate_

Goes to:
- **07_Sign_Up**

Reached from: 01_Landing_page, 02_Find_jobs, 03_Browse_Companies, 04_Search_Companies_Results, 05_Job_Descriptions, 06_Company_Profile, 07_Sign_Up

### 09_Dashboard_Applicant
_23 annotations · 9 navigate_

Goes to:
- **01_Landing_page**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 10_Dashboard_-_Message, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 10_Dashboard_-_Message
_26 annotations · 9 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **17_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 09_Dashboard_Applicant, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 11_Dashboard_-_Applications_History
_31 annotations · 9 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **12_Dashboard_-_Find_Jobs**
- **13_Dashboard_-_Job_Descriptions**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 12_Dashboard_-_Find_Jobs
_55 annotations · 16 navigate_

Goes to:
- **01_Landing_page**
- **05_Job_Descriptions** (x7)
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 11_Dashboard_-_Applications_History, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 13_Dashboard_-_Job_Descriptions
_14 annotations · 10 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 11_Dashboard_-_Applications_History

### 14_Dashboard_-_Browse_Companies
_48 annotations · 14 navigate_

Goes to:
- **06_Company_Profile** (x6)
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**
- **18_Dashboard_-_Settings**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 15_Dashboard_-_Profile
_35 annotations · 8 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **16_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 16_Dashboard_-_Settings
_23 annotations · 11 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **17_Dashboard_-_Settings**
- **18_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 09_Dashboard_Applicant, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 14_Dashboard_-_Browse_Companies, 15_Dashboard_-_Profile, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings, 19_Dashboard_-_Help

### 17_Dashboard_-_Settings
_20 annotations · 12 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings** (x2)
- **18_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 10_Dashboard_-_Message, 16_Dashboard_-_Settings, 18_Dashboard_-_Settings

### 18_Dashboard_-_Settings
_18 annotations · 12 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings** (x2)
- **17_Dashboard_-_Settings**
- **19_Dashboard_-_Help**

Reached from: 14_Dashboard_-_Browse_Companies, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings

### 19_Dashboard_-_Help
_26 annotations · 9 navigate_

Goes to:
- **01_Landing_page**
- **09_Dashboard_Applicant**
- **10_Dashboard_-_Message**
- **11_Dashboard_-_Applications_History**
- **12_Dashboard_-_Find_Jobs**
- **14_Dashboard_-_Browse_Companies**
- **15_Dashboard_-_Profile** (x2)
- **16_Dashboard_-_Settings**

Reached from: 09_Dashboard_Applicant, 10_Dashboard_-_Message, 11_Dashboard_-_Applications_History, 12_Dashboard_-_Find_Jobs, 13_Dashboard_-_Job_Descriptions, 15_Dashboard_-_Profile, 16_Dashboard_-_Settings, 17_Dashboard_-_Settings, 18_Dashboard_-_Settings
