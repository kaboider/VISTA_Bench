# Site Map — 4_forum

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Register** — `pages/01_Register.png` · `pages/01_Register.json`
- **02_Login** — `pages/02_Login.png` · `pages/02_Login.json`
- **03_Main** — `pages/03_Main.png` · `pages/03_Main.json`
- **04_Post_View** — `pages/04_Post_View.png` · `pages/04_Post_View.json`
- **05_Post_Edit** — `pages/05_Post_Edit.png` · `pages/05_Post_Edit.json`

## Navigation graph

```
01_Register
  └─→ 02_Login

02_Login
  └─→ 01_Register

03_Main
  ├─→ 04_Post_View (x5)
  └─→ 05_Post_Edit

04_Post_View
  └─→ 05_Post_Edit

# pages with no outgoing navigate edges:
  · 05_Post_Edit
```

## Per-page navigation

### 01_Register
_7 annotations · 1 navigate_

Goes to:
- **02_Login**

Reached from: 02_Login

### 02_Login
_4 annotations · 1 navigate_

Goes to:
- **01_Register**

Reached from: 01_Register

### 03_Main
_27 annotations · 6 navigate_

Goes to:
- **04_Post_View** (x5)
- **05_Post_Edit**

### 04_Post_View
_32 annotations · 1 navigate_

Goes to:
- **05_Post_Edit**

Reached from: 03_Main

### 05_Post_Edit
_20 annotations_

Goes to: _(none)_

Reached from: 03_Main, 04_Post_View
