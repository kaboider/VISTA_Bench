# Site Map — 5_travel-booking

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Homepage** — `pages/01_Homepage.png` · `pages/01_Homepage.json`
- **02_build_your_own_package** — `pages/02_build_your_own_package.png` · `pages/02_build_your_own_package.json`
- **03_ABout_us** — `pages/03_ABout_us.png` · `pages/03_ABout_us.json`
- **04_Package_archive** — `pages/04_Package_archive.png` · `pages/04_Package_archive.json`
- **05_Package_Detail_Page** — `pages/05_Package_Detail_Page.png` · `pages/05_Package_Detail_Page.json`
- **06_Tour_Plan** — `pages/06_Tour_Plan.png` · `pages/06_Tour_Plan.json`
- **07_Location** — `pages/07_Location.png` · `pages/07_Location.json`
- **08_Tour_Gallery** — `pages/08_Tour_Gallery.png` · `pages/08_Tour_Gallery.json`

## Navigation graph

```
01_Homepage
  ├─→ 03_ABout_us
  └─→ 05_Package_Detail_Page (x7)

02_build_your_own_package
  ├─→ 01_Homepage
  └─→ 03_ABout_us

03_ABout_us
  ├─→ 01_Homepage
  └─→ 05_Package_Detail_Page (x12)

04_Package_archive
  ├─→ 01_Homepage
  ├─→ 03_ABout_us
  └─→ 05_Package_Detail_Page (x6)

05_Package_Detail_Page
  ├─→ 01_Homepage
  ├─→ 03_ABout_us
  ├─→ 06_Tour_Plan
  ├─→ 07_Location
  └─→ 08_Tour_Gallery

06_Tour_Plan
  ├─→ 01_Homepage
  ├─→ 03_ABout_us
  ├─→ 05_Package_Detail_Page
  ├─→ 07_Location
  └─→ 08_Tour_Gallery

07_Location
  ├─→ 01_Homepage
  ├─→ 03_ABout_us
  ├─→ 05_Package_Detail_Page
  ├─→ 06_Tour_Plan
  └─→ 08_Tour_Gallery

08_Tour_Gallery
  ├─→ 01_Homepage
  ├─→ 03_ABout_us
  ├─→ 05_Package_Detail_Page
  ├─→ 06_Tour_Plan
  └─→ 07_Location

```

## Per-page navigation

### 01_Homepage
_19 annotations · 8 navigate_

Goes to:
- **03_ABout_us**
- **05_Package_Detail_Page** (x7)

Reached from: 02_build_your_own_package, 03_ABout_us, 04_Package_archive, 05_Package_Detail_Page, 06_Tour_Plan, 07_Location, 08_Tour_Gallery

### 02_build_your_own_package
_30 annotations · 2 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**

### 03_ABout_us
_23 annotations · 13 navigate_

Goes to:
- **01_Homepage**
- **05_Package_Detail_Page** (x12)

Reached from: 01_Homepage, 02_build_your_own_package, 04_Package_archive, 05_Package_Detail_Page, 06_Tour_Plan, 07_Location, 08_Tour_Gallery

### 04_Package_archive
_26 annotations · 8 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**
- **05_Package_Detail_Page** (x6)

### 05_Package_Detail_Page
_20 annotations · 5 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**
- **06_Tour_Plan**
- **07_Location**
- **08_Tour_Gallery**

Reached from: 01_Homepage, 03_ABout_us, 04_Package_archive, 06_Tour_Plan, 07_Location, 08_Tour_Gallery

### 06_Tour_Plan
_20 annotations · 5 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**
- **05_Package_Detail_Page**
- **07_Location**
- **08_Tour_Gallery**

Reached from: 05_Package_Detail_Page, 07_Location, 08_Tour_Gallery

### 07_Location
_20 annotations · 5 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**
- **05_Package_Detail_Page**
- **06_Tour_Plan**
- **08_Tour_Gallery**

Reached from: 05_Package_Detail_Page, 06_Tour_Plan, 08_Tour_Gallery

### 08_Tour_Gallery
_26 annotations · 5 navigate_

Goes to:
- **01_Homepage**
- **03_ABout_us**
- **05_Package_Detail_Page**
- **06_Tour_Plan**
- **07_Location**

Reached from: 05_Package_Detail_Page, 06_Tour_Plan, 07_Location
