# Site Map — 8_ecommerce

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Sign_in** — `pages/01_Sign_in.png` · `pages/01_Sign_in.json`
- **02_Sign_up** — `pages/02_Sign_up.png` · `pages/02_Sign_up.json`
- **03_Home_page** — `pages/03_Home_page.png` · `pages/03_Home_page.json`
- **04_Shop_page** — `pages/04_Shop_page.png` · `pages/04_Shop_page.json`
- **05_Product_Page** — `pages/05_Product_Page.png` · `pages/05_Product_Page.json`
- **06_Cart_Page** — `pages/06_Cart_Page.png` · `pages/06_Cart_Page.json`
- **07_Check_out** — `pages/07_Check_out.png` · `pages/07_Check_out.json`

## Navigation graph

```
01_Sign_in
  ├─→ 02_Sign_up
  └─→ 03_Home_page

02_Sign_up
  ├─→ 01_Sign_in
  └─→ 03_Home_page

03_Home_page
  ├─→ 01_Sign_in
  ├─→ 02_Sign_up
  ├─→ 04_Shop_page (x8)
  └─→ 05_Product_Page (x7)

04_Shop_page
  ├─→ 03_Home_page
  ├─→ 05_Product_Page (x9)
  └─→ 06_Cart_Page

05_Product_Page
  ├─→ 03_Home_page
  ├─→ 04_Shop_page
  └─→ 06_Cart_Page

06_Cart_Page
  ├─→ 03_Home_page (x2)
  └─→ 04_Shop_page

07_Check_out
  ├─→ 03_Home_page
  ├─→ 04_Shop_page
  └─→ 06_Cart_Page

```

## Per-page navigation

### 01_Sign_in
_7 annotations · 2 navigate_

Goes to:
- **02_Sign_up**
- **03_Home_page**

Reached from: 02_Sign_up, 03_Home_page

### 02_Sign_up
_10 annotations · 2 navigate_

Goes to:
- **01_Sign_in**
- **03_Home_page**

Reached from: 01_Sign_in, 03_Home_page

### 03_Home_page
_27 annotations · 17 navigate_

Goes to:
- **01_Sign_in**
- **02_Sign_up**
- **04_Shop_page** (x8)
- **05_Product_Page** (x7)

Reached from: 01_Sign_in, 02_Sign_up, 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out

### 04_Shop_page
_93 annotations · 11 navigate_

Goes to:
- **03_Home_page**
- **05_Product_Page** (x9)
- **06_Cart_Page**

Reached from: 03_Home_page, 05_Product_Page, 06_Cart_Page, 07_Check_out

### 05_Product_Page
_35 annotations · 3 navigate_

Goes to:
- **03_Home_page**
- **04_Shop_page**
- **06_Cart_Page**

Reached from: 03_Home_page, 04_Shop_page

### 06_Cart_Page
_16 annotations · 3 navigate_

Goes to:
- **03_Home_page** (x2)
- **04_Shop_page**

Reached from: 04_Shop_page, 05_Product_Page, 07_Check_out

### 07_Check_out
_26 annotations · 3 navigate_

Goes to:
- **03_Home_page**
- **04_Shop_page**
- **06_Cart_Page**
