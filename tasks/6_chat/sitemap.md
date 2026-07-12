# Site Map — 6_chat

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Sign_Up** — `pages/01_Sign_Up.png` · `pages/01_Sign_Up.json`
- **02_Sign_in** — `pages/02_Sign_in.png` · `pages/02_Sign_in.json`
- **03_Success** — `pages/03_Success.png` · `pages/03_Success.json`
- **04_Chat** — `pages/04_Chat.png` · `pages/04_Chat.json`
- **05_Contacts** — `pages/05_Contacts.png` · `pages/05_Contacts.json`
- **06_Group** — `pages/06_Group.png` · `pages/06_Group.json`
- **07_Status_User** — `pages/07_Status_User.png` · `pages/07_Status_User.json`
- **08_Calls** — `pages/08_Calls.png` · `pages/08_Calls.json`
- **09_video_Call** — `pages/09_video_Call.png` · `pages/09_video_Call.json`
- **10_Voice_call** — `pages/10_Voice_call.png` · `pages/10_Voice_call.json`

## Navigation graph

```
01_Sign_Up
  ├─→ 02_Sign_in
  └─→ 03_Success

02_Sign_in
  ├─→ 01_Sign_Up
  └─→ 04_Chat

03_Success
  └─→ 02_Sign_in

04_Chat
  ├─→ 05_Contacts (x2)
  ├─→ 07_Status_User
  └─→ 08_Calls

05_Contacts
  ├─→ 04_Chat
  ├─→ 06_Group
  ├─→ 07_Status_User
  └─→ 08_Calls

06_Group
  ├─→ 04_Chat
  ├─→ 05_Contacts
  ├─→ 07_Status_User
  └─→ 08_Calls

07_Status_User
  ├─→ 04_Chat
  ├─→ 05_Contacts
  ├─→ 06_Group
  └─→ 08_Calls

08_Calls
  ├─→ 04_Chat
  ├─→ 05_Contacts
  ├─→ 06_Group
  └─→ 07_Status_User

# pages with no outgoing navigate edges:
  · 09_video_Call
  · 10_Voice_call
```

## Per-page navigation

### 01_Sign_Up
_12 annotations · 2 navigate_

Goes to:
- **02_Sign_in**
- **03_Success**

Reached from: 02_Sign_in

### 02_Sign_in
_8 annotations · 2 navigate_

Goes to:
- **01_Sign_Up**
- **04_Chat**

Reached from: 01_Sign_Up, 03_Success

### 03_Success
_1 annotations · 1 navigate_

Goes to:
- **02_Sign_in**

Reached from: 01_Sign_Up

### 04_Chat
_41 annotations · 4 navigate_

Goes to:
- **05_Contacts** (x2)
- **07_Status_User**
- **08_Calls**

Reached from: 02_Sign_in, 05_Contacts, 06_Group, 07_Status_User, 08_Calls

### 05_Contacts
_30 annotations · 4 navigate_

Goes to:
- **04_Chat**
- **06_Group**
- **07_Status_User**
- **08_Calls**

Reached from: 04_Chat, 06_Group, 07_Status_User, 08_Calls

### 06_Group
_35 annotations · 4 navigate_

Goes to:
- **04_Chat**
- **05_Contacts**
- **07_Status_User**
- **08_Calls**

Reached from: 05_Contacts, 07_Status_User, 08_Calls

### 07_Status_User
_21 annotations · 4 navigate_

Goes to:
- **04_Chat**
- **05_Contacts**
- **06_Group**
- **08_Calls**

Reached from: 04_Chat, 05_Contacts, 06_Group, 08_Calls

### 08_Calls
_24 annotations · 4 navigate_

Goes to:
- **04_Chat**
- **05_Contacts**
- **06_Group**
- **07_Status_User**

Reached from: 04_Chat, 05_Contacts, 06_Group, 07_Status_User

### 09_video_Call
_7 annotations_

Goes to: _(none)_

### 10_Voice_call
_5 annotations_

Goes to: _(none)_
