# Site Map — 2_real-estate

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_sign_in** — `pages/01_sign_in.png` · `pages/01_sign_in.json`
- **02_sign_up** — `pages/02_sign_up.png` · `pages/02_sign_up.json`
- **03_Home_page** — `pages/03_Home_page.png` · `pages/03_Home_page.json`
- **04_Buy** — `pages/04_Buy.png` · `pages/04_Buy.json`
- **05_Buy** — `pages/05_Buy.png` · `pages/05_Buy.json`
- **06_Buy_Grid_With_Map** — `pages/06_Buy_Grid_With_Map.png` · `pages/06_Buy_Grid_With_Map.json`
- **07_Buy_Details_-_Request_Info** — `pages/07_Buy_Details_-_Request_Info.png` · `pages/07_Buy_Details_-_Request_Info.json`
- **08_Rent_Grid** — `pages/08_Rent_Grid.png` · `pages/08_Rent_Grid.json`
- **09_Rent_List** — `pages/09_Rent_List.png` · `pages/09_Rent_List.json`
- **10_Rent_Grid_with_Map** — `pages/10_Rent_Grid_with_Map.png` · `pages/10_Rent_Grid_with_Map.json`
- **11_Detail_Page_For_Rent** — `pages/11_Detail_Page_For_Rent.png` · `pages/11_Detail_Page_For_Rent.json`
- **12_Agent_Grid** — `pages/12_Agent_Grid.png` · `pages/12_Agent_Grid.json`
- **13_Agent_List** — `pages/13_Agent_List.png` · `pages/13_Agent_List.json`
- **14_Agent_Details** — `pages/14_Agent_Details.png` · `pages/14_Agent_Details.json`

## Navigation graph

```
01_sign_in
  ├─→ 02_sign_up
  └─→ 03_Home_page

02_sign_up
  ├─→ 01_sign_in
  └─→ 03_Home_page

03_Home_page
  ├─→ 01_sign_in
  ├─→ 02_sign_up
  ├─→ 04_Buy (x9)
  ├─→ 07_Buy_Details_-_Request_Info (x6)
  ├─→ 08_Rent_Grid (x3)
  ├─→ 11_Detail_Page_For_Rent (x7)
  └─→ 13_Agent_List

04_Buy
  ├─→ 03_Home_page (x2)
  ├─→ 05_Buy
  ├─→ 06_Buy_Grid_With_Map
  ├─→ 07_Buy_Details_-_Request_Info (x9)
  └─→ 12_Agent_Grid

05_Buy
  ├─→ 03_Home_page
  ├─→ 04_Buy
  ├─→ 06_Buy_Grid_With_Map
  ├─→ 07_Buy_Details_-_Request_Info (x6)
  └─→ 12_Agent_Grid

06_Buy_Grid_With_Map
  ├─→ 03_Home_page
  ├─→ 04_Buy
  ├─→ 05_Buy
  ├─→ 07_Buy_Details_-_Request_Info (x5)
  └─→ 12_Agent_Grid

07_Buy_Details_-_Request_Info
  ├─→ 03_Home_page
  ├─→ 11_Detail_Page_For_Rent
  ├─→ 12_Agent_Grid
  └─→ 14_Agent_Details

08_Rent_Grid
  ├─→ 03_Home_page
  ├─→ 09_Rent_List
  ├─→ 10_Rent_Grid_with_Map
  ├─→ 11_Detail_Page_For_Rent (x9)
  └─→ 12_Agent_Grid

09_Rent_List
  ├─→ 03_Home_page
  ├─→ 08_Rent_Grid
  ├─→ 10_Rent_Grid_with_Map
  ├─→ 11_Detail_Page_For_Rent (x6)
  └─→ 12_Agent_Grid

10_Rent_Grid_with_Map
  ├─→ 03_Home_page
  ├─→ 08_Rent_Grid
  ├─→ 09_Rent_List
  ├─→ 11_Detail_Page_For_Rent (x5)
  └─→ 12_Agent_Grid

11_Detail_Page_For_Rent
  ├─→ 03_Home_page
  ├─→ 12_Agent_Grid
  └─→ 14_Agent_Details

12_Agent_Grid
  ├─→ 03_Home_page
  └─→ 14_Agent_Details (x8)

13_Agent_List
  ├─→ 01_sign_in
  ├─→ 02_sign_up
  ├─→ 03_Home_page
  └─→ 14_Agent_Details (x7)

14_Agent_Details
  ├─→ 01_sign_in
  ├─→ 02_sign_up
  ├─→ 03_Home_page
  ├─→ 11_Detail_Page_For_Rent (x2)
  └─→ 12_Agent_Grid

```

## Per-page navigation

### 01_sign_in
_7 annotations · 2 navigate_

Goes to:
- **02_sign_up**
- **03_Home_page**

Reached from: 02_sign_up, 03_Home_page, 13_Agent_List, 14_Agent_Details

### 02_sign_up
_9 annotations · 2 navigate_

Goes to:
- **01_sign_in**
- **03_Home_page**

Reached from: 01_sign_in, 03_Home_page, 13_Agent_List, 14_Agent_Details

### 03_Home_page
_59 annotations · 28 navigate_

Goes to:
- **01_sign_in**
- **02_sign_up**
- **04_Buy** (x9)
- **07_Buy_Details_-_Request_Info** (x6)
- **08_Rent_Grid** (x3)
- **11_Detail_Page_For_Rent** (x7)
- **13_Agent_List**

Reached from: 01_sign_in, 02_sign_up, 04_Buy, 05_Buy, 06_Buy_Grid_With_Map, 07_Buy_Details_-_Request_Info, 08_Rent_Grid, 09_Rent_List, 10_Rent_Grid_with_Map, 11_Detail_Page_For_Rent, 12_Agent_Grid, 13_Agent_List, 14_Agent_Details

### 04_Buy
_28 annotations · 14 navigate_

Goes to:
- **03_Home_page** (x2)
- **05_Buy**
- **06_Buy_Grid_With_Map**
- **07_Buy_Details_-_Request_Info** (x9)
- **12_Agent_Grid**

Reached from: 03_Home_page, 05_Buy, 06_Buy_Grid_With_Map

### 05_Buy
_24 annotations · 10 navigate_

Goes to:
- **03_Home_page**
- **04_Buy**
- **06_Buy_Grid_With_Map**
- **07_Buy_Details_-_Request_Info** (x6)
- **12_Agent_Grid**

Reached from: 04_Buy, 06_Buy_Grid_With_Map

### 06_Buy_Grid_With_Map
_43 annotations · 9 navigate_

Goes to:
- **03_Home_page**
- **04_Buy**
- **05_Buy**
- **07_Buy_Details_-_Request_Info** (x5)
- **12_Agent_Grid**

Reached from: 04_Buy, 05_Buy

### 07_Buy_Details_-_Request_Info
_60 annotations · 4 navigate_

Goes to:
- **03_Home_page**
- **11_Detail_Page_For_Rent**
- **12_Agent_Grid**
- **14_Agent_Details**

Reached from: 03_Home_page, 04_Buy, 05_Buy, 06_Buy_Grid_With_Map

### 08_Rent_Grid
_26 annotations · 13 navigate_

Goes to:
- **03_Home_page**
- **09_Rent_List**
- **10_Rent_Grid_with_Map**
- **11_Detail_Page_For_Rent** (x9)
- **12_Agent_Grid**

Reached from: 03_Home_page, 09_Rent_List, 10_Rent_Grid_with_Map

### 09_Rent_List
_24 annotations · 10 navigate_

Goes to:
- **03_Home_page**
- **08_Rent_Grid**
- **10_Rent_Grid_with_Map**
- **11_Detail_Page_For_Rent** (x6)
- **12_Agent_Grid**

Reached from: 08_Rent_Grid, 10_Rent_Grid_with_Map

### 10_Rent_Grid_with_Map
_43 annotations · 9 navigate_

Goes to:
- **03_Home_page**
- **08_Rent_Grid**
- **09_Rent_List**
- **11_Detail_Page_For_Rent** (x5)
- **12_Agent_Grid**

Reached from: 08_Rent_Grid, 09_Rent_List

### 11_Detail_Page_For_Rent
_48 annotations · 3 navigate_

Goes to:
- **03_Home_page**
- **12_Agent_Grid**
- **14_Agent_Details**

Reached from: 03_Home_page, 07_Buy_Details_-_Request_Info, 08_Rent_Grid, 09_Rent_List, 10_Rent_Grid_with_Map, 14_Agent_Details

### 12_Agent_Grid
_24 annotations · 9 navigate_

Goes to:
- **03_Home_page**
- **14_Agent_Details** (x8)

Reached from: 04_Buy, 05_Buy, 06_Buy_Grid_With_Map, 07_Buy_Details_-_Request_Info, 08_Rent_Grid, 09_Rent_List, 10_Rent_Grid_with_Map, 11_Detail_Page_For_Rent, 14_Agent_Details

### 13_Agent_List
_23 annotations · 10 navigate_

Goes to:
- **01_sign_in**
- **02_sign_up**
- **03_Home_page**
- **14_Agent_Details** (x7)

Reached from: 03_Home_page

### 14_Agent_Details
_31 annotations · 6 navigate_

Goes to:
- **01_sign_in**
- **02_sign_up**
- **03_Home_page**
- **11_Detail_Page_For_Rent** (x2)
- **12_Agent_Grid**

Reached from: 07_Buy_Details_-_Request_Info, 11_Detail_Page_For_Rent, 12_Agent_Grid, 13_Agent_List
