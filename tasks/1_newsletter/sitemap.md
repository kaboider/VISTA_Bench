# Site Map — 1_newsletter

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Home** — `pages/01_Home.png` · `pages/01_Home.json`
- **02_Single-post** — `pages/02_Single-post.png` · `pages/02_Single-post.json`
- **03_Author** — `pages/03_Author.png` · `pages/03_Author.json`
- **04_Category** — `pages/04_Category.png` · `pages/04_Category.json`
- **05_Tag** — `pages/05_Tag.png` · `pages/05_Tag.json`
- **06_Date** — `pages/06_Date.png` · `pages/06_Date.json`
- **07_Search** — `pages/07_Search.png` · `pages/07_Search.json`
- **08_About_me** — `pages/08_About_me.png` · `pages/08_About_me.json`
- **09_Contact_me** — `pages/09_Contact_me.png` · `pages/09_Contact_me.json`

## Navigation graph

```
01_Home
  ├─→ 02_Single-post (x5)
  ├─→ 03_Author
  ├─→ 04_Category
  └─→ 07_Search

02_Single-post
  ├─→ 01_Home
  ├─→ 03_Author
  ├─→ 04_Category (x3)
  ├─→ 05_Tag (x7)
  └─→ 07_Search

03_Author
  └─→ 02_Single-post (x6)

04_Category
  ├─→ 01_Home
  └─→ 02_Single-post (x10)

05_Tag
  ├─→ 01_Home (x2)
  ├─→ 02_Single-post (x7)
  └─→ 04_Category

06_Date
  ├─→ 01_Home
  └─→ 02_Single-post (x5)

07_Search
  ├─→ 01_Home
  └─→ 02_Single-post (x2)

08_About_me
  └─→ 01_Home

09_Contact_me
  ├─→ 01_Home
  └─→ 07_Search

```

## Per-page navigation

### 01_Home
_18 annotations · 8 navigate_

Goes to:
- **02_Single-post** (x5)
- **03_Author**
- **04_Category**
- **07_Search**

Reached from: 02_Single-post, 04_Category, 05_Tag, 06_Date, 07_Search, 08_About_me, 09_Contact_me

### 02_Single-post
_23 annotations · 13 navigate_

Goes to:
- **01_Home**
- **03_Author**
- **04_Category** (x3)
- **05_Tag** (x7)
- **07_Search**

Reached from: 01_Home, 03_Author, 04_Category, 05_Tag, 06_Date, 07_Search

### 03_Author
_11 annotations · 6 navigate_

Goes to:
- **02_Single-post** (x6)

Reached from: 01_Home, 02_Single-post

### 04_Category
_16 annotations · 11 navigate_

Goes to:
- **01_Home**
- **02_Single-post** (x10)

Reached from: 01_Home, 02_Single-post, 05_Tag

### 05_Tag
_17 annotations · 10 navigate_

Goes to:
- **01_Home** (x2)
- **02_Single-post** (x7)
- **04_Category**

Reached from: 02_Single-post

### 06_Date
_20 annotations · 6 navigate_

Goes to:
- **01_Home**
- **02_Single-post** (x5)

### 07_Search
_10 annotations · 3 navigate_

Goes to:
- **01_Home**
- **02_Single-post** (x2)

Reached from: 01_Home, 02_Single-post, 09_Contact_me

### 08_About_me
_7 annotations · 1 navigate_

Goes to:
- **01_Home**

### 09_Contact_me
_11 annotations · 2 navigate_

Goes to:
- **01_Home**
- **07_Search**
