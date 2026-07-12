# Interaction summary

This is a human-friendly digest of `interaction_index.json` you can consume while writing each page. The JSON is the source of truth; this Markdown only re-organizes it.

- Total annotations: **214**
- Total logical elements: **193**
- Vision-verified groups: SAME=8, DIFFERENT=0, UNCLEAR=0

**Tiers:** critical=65 (must implement + must work), bonus=65 (must have testid; behavior unconstrained), skip=63 (decorative — `click_dead`).

## Cross-page elements
These appear on multiple pages. Use ONE shared testid for each. Pick a name once and reuse it across every page in `pages` below.

| logical_id | tier | type/subtype | grouping | pages | description |
|---|---|---|---|---|---|
| `le_001` | critical | navigate | vision✓ | 4: 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out | All four crops show the same 'Home' navigation link text in identical styling, representing the same nav element across different pages of the site. |
| `le_002` | bonus | click/click_unknown_nav | vision✓ | 4: 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out | All four crops show the same 'Products' navigation link text in the same style, representing the same nav item across the Shop, Product, Cart, and Checkout pages — the second crop has an underline ind |
| `le_003` | critical | click/click_popout | vision✓ | 4: 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out | All four crops show the same search icon (magnifying glass) in the same header position, consistently representing the 'm-search-popup' trigger element across all four pages. |
| `le_004` | bonus | click/click_unknown_nav | vision✓ | 4: 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out | All four crops show the same user/account icon and adjacent navigation icon in the same header position across all pages, indicating a consistent navigation element. |
| `le_005` | bonus | click/click_unknown_nav | vision✓ | 4: 04_Shop_page, 05_Product_Page, 06_Cart_Page, 07_Check_out | All four crops show the same pair of navigation icons (a bookmark/cart icon and a star/wishlist icon) repeated consistently across each page, indicating the same persistent nav element. |
| `le_006` | critical | navigate | vision✓ | 3: 04_Shop_page, 05_Product_Page, 07_Check_out | All three crops show the same shopping cart icon in the navigation bar, with the third instance showing a badge indicating 1 item in cart — same logical UI element across pages. |
| `le_007` | critical | navigate | vision✓ | 3: 05_Product_Page, 06_Cart_Page, 07_Check_out | All three crops show an identical 'Shop' navigation link in the same style and role across the product, cart, and checkout pages. |
| `le_008` | bonus | click/click_unknown_nav | vision✓ | 2: 05_Product_Page, 07_Check_out | Both crops show the identical 'Pages ∨' dropdown navigation element with the same text, style, and chevron icon, consistent across both pages. |

## Per-page checklists
For each page, every logical_element that has an occurrence on it. When you implement that page's component, every `logical_id` row below MUST have its testid present in the rendered HTML.

### 01_Sign_in — 5 critical, 2 bonus, 0 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #1 | `le_009` | critical | click/click_social_oauth |  | "Sign up with Google" rectangle — OAuth authentication button. |
| #3 | `le_011` | critical | input |  | (no description; check bbox in PNG) |
| #4 | `le_012` | critical | input |  | (no description; check bbox in PNG) |
| #5 | `le_013` | critical | navigate |  | (no description; check bbox in PNG) |
| #6 | `le_014` | critical | navigate |  | (no description; check bbox in PNG) |
| #2 | `le_010` | bonus | click/click_unknown_nav |  | "Rectangle 4" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #7 | `le_015` | bonus | click/click_unknown_nav |  | "Forget Password?" navigates to the password-reset flow. |

### 02_Sign_up — 8 critical, 2 bonus, 0 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #3 | `le_018` | critical | input |  | (no description; check bbox in PNG) |
| #4 | `le_019` | critical | input |  | (no description; check bbox in PNG) |
| #5 | `le_020` | critical | input |  | (no description; check bbox in PNG) |
| #6 | `le_021` | critical | input |  | (no description; check bbox in PNG) |
| #7 | `le_022` | critical | input |  | (no description; check bbox in PNG) |
| #8 | `le_023` | critical | input |  | (no description; check bbox in PNG) |
| #9 | `le_024` | critical | navigate |  | (no description; check bbox in PNG) |
| #10 | `le_025` | critical | navigate |  | (no description; check bbox in PNG) |
| #1 | `le_016` | bonus | click/click_unknown_nav |  | "Rectangle 3" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #2 | `le_017` | bonus | click/click_unknown_nav |  | "Rectangle 4" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |

### 03_Home_page — 18 critical, 4 bonus, 5 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #5 | `le_030` | critical | navigate |  | (no description; check bbox in PNG) |
| #6 | `le_031` | critical | navigate |  | (no description; check bbox in PNG) |
| #7 | `le_032` | critical | navigate |  | (no description; check bbox in PNG) |
| #8 | `le_033` | critical | navigate |  | (no description; check bbox in PNG) |
| #12 | `le_036` | critical | navigate |  | (no description; check bbox in PNG) |
| #13 | `le_037` | critical | navigate |  | (no description; check bbox in PNG) |
| #14 | `le_038` | critical | navigate |  | (no description; check bbox in PNG) |
| #15 | `le_039` | critical | navigate |  | (no description; check bbox in PNG) |
| #16 | `le_040` | critical | navigate |  | (no description; check bbox in PNG) |
| #17 | `le_041` | critical | navigate |  | (no description; check bbox in PNG) |
| #18 | `le_042` | critical | navigate |  | (no description; check bbox in PNG) |
| #19 | `le_043` | critical | navigate |  | (no description; check bbox in PNG) |
| #20 | `le_044` | critical | navigate |  | (no description; check bbox in PNG) |
| #21 | `le_045` | critical | navigate |  | (no description; check bbox in PNG) |
| #22 | `le_046` | critical | navigate |  | (no description; check bbox in PNG) |
| #23 | `le_047` | critical | navigate |  | (no description; check bbox in PNG) |
| #24 | `le_048` | critical | navigate |  | (no description; check bbox in PNG) |
| #28 | `le_052` | critical | click/click_popout |  | Subscribe Now button — triggers newsletter confirmation modal. |
| #2 | `le_027` | bonus | click/click_unknown_nav |  | "Deals" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #3 | `le_028` | bonus | click/click_unknown_nav |  | "New Arrivals" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #4 | `le_029` | bonus | click/click_unknown_nav |  | "Packages" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #25 | `le_049` | bonus | click/click_unknown_nav |  | "DESCRIPTION" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #1 | `le_026` | skip | click/click_dead |  | Nav link "Home" matches the current page (03_Home_page); clicking it produces no navigation. |
| #9 | `le_034` | skip | click/click_dead |  | Carousel arrow — advances carousel in-place, no page navigation. |
| #10 | `le_035` | skip | click/click_dead |  | Carousel arrow — advances carousel in-place, no page navigation. |
| #26 | `le_050` | skip | click/click_dead |  | Carousel arrow — advances carousel in-place, no page navigation. |
| #27 | `le_051` | skip | click/click_dead |  | Carousel arrow — advances carousel in-place, no page navigation. |

### 04_Shop_page — 14 critical, 33 bonus, 46 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #1 | `le_001` | critical | navigate | ✓ | All four crops show the same 'Home' navigation link text in identical styling, representing the same nav element across different pages of the site. |
| #5 | `le_003` | critical | click/click_popout | ✓ | All four crops show the same search icon (magnifying glass) in the same header position, consistently representing the 'm-search-popup' trigger element across all four pages. |
| #8 | `le_006` | critical | navigate | ✓ | All three crops show the same shopping cart icon in the navigation bar, with the third instance showing a badge indicating 1 item in cart — same logical UI element across pages. |
| #3 | `le_054` | critical | click/click_popout |  | Pagination dropdown — opens page-number selector panel. |
| #9 | `le_055` | critical | navigate |  | (no description; check bbox in PNG) |
| #10 | `le_056` | critical | navigate |  | (no description; check bbox in PNG) |
| #11 | `le_057` | critical | navigate |  | (no description; check bbox in PNG) |
| #12 | `le_058` | critical | navigate |  | (no description; check bbox in PNG) |
| #13 | `le_059` | critical | navigate |  | (no description; check bbox in PNG) |
| #14 | `le_060` | critical | navigate |  | (no description; check bbox in PNG) |
| #15 | `le_061` | critical | navigate |  | (no description; check bbox in PNG) |
| #16 | `le_062` | critical | navigate |  | (no description; check bbox in PNG) |
| #17 | `le_063` | critical | navigate |  | (no description; check bbox in PNG) |
| #93 | `le_137` | critical | click/click_popout |  | "m-select-component" opens a dropdown selection panel. |
| #4 | `le_002` | bonus | click/click_unknown_nav | ✓ | All four crops show the same 'Products' navigation link text in the same style, representing the same nav item across the Shop, Product, Cart, and Checkout pages — the second crop has an underline ind |
| #6 | `le_004` | bonus | click/click_unknown_nav | ✓ | All four crops show the same user/account icon and adjacent navigation icon in the same header position across all pages, indicating a consistent navigation element. |
| #7 | `le_005` | bonus | click/click_unknown_nav | ✓ | All four crops show the same pair of navigation icons (a bookmark/cart icon and a star/wishlist icon) repeated consistently across each page, indicating the same persistent nav element. |
| #19 | `le_064` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #20 | `le_065` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #21 | `le_066` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #22 | `le_067` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #23 | `le_068` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #24 | `le_069` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #25 | `le_070` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #26 | `le_071` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #27 | `le_072` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #28 | `le_073` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #29 | `le_074` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #30 | `le_075` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #31 | `le_076` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #32 | `le_077` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #33 | `le_078` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #34 | `le_079` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #35 | `le_080` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #36 | `le_081` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #37 | `le_082` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #38 | `le_083` | bonus | click/click_unknown_nav |  | "div.sf__tooltip-item" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #39 | `le_084` | bonus | click/click_unknown_nav |  | "Item ⏵ Link" is a facet/filter navigation link that updates the listing page. |
| #40 | `le_085` | bonus | click/click_unknown_nav |  | "Item ⏵ Link" is a facet/filter navigation link that updates the listing page. |
| #41 | `le_086` | bonus | click/click_unknown_nav |  | "Item ⏵ Link" is a facet/filter navigation link that updates the listing page. |
| #42 | `le_087` | bonus | click/click_unknown_nav |  | "Item ⏵ Link" is a facet/filter navigation link that updates the listing page. |
| #83 | `le_127` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #84 | `le_128` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #85 | `le_129` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #86 | `le_130` | bonus | click/click_unknown_nav |  | "span.page" is a content navigation link to a related page. |
| #87 | `le_131` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #94 | `le_138` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #2 | `le_053` | skip | click/click_dead |  | Nav link "Shop" matches the current page (04_Shop_page); clicking it produces no navigation. |
| #43 | `le_088` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #44 | `le_089` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #45 | `le_090` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #46 | `le_091` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #47 | `le_092` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #48 | `le_093` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #49 | `le_094` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #50 | `le_095` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #51 | `le_096` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #52 | `le_097` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #53 | `le_098` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #54 | `le_099` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #55 | `le_100` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #56 | `le_101` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #57 | `le_102` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #58 | `le_103` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #59 | `le_104` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #60 | `le_105` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #61 | `le_106` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #62 | `le_107` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #63 | `le_108` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #64 | `le_109` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #65 | `le_110` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #66 | `le_111` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #67 | `le_112` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #68 | `le_113` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #69 | `le_114` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #70 | `le_115` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #71 | `le_115` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #72 | `le_116` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #73 | `le_117` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #74 | `le_118` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #75 | `le_119` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #76 | `le_120` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #77 | `le_121` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #78 | `le_122` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #79 | `le_123` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #80 | `le_124` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #81 | `le_125` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #82 | `le_126` | skip | click/click_dead |  | Color selector chip (Item) — in-place color selection. |
| #88 | `le_132` | skip | click/click_dead |  | View toggle (Button) — switches grid/list view in-place. |
| #89 | `le_133` | skip | click/click_dead |  | View toggle (Button) — switches grid/list view in-place. |
| #90 | `le_134` | skip | click/click_dead |  | View toggle (Button) — switches grid/list view in-place. |
| #91 | `le_135` | skip | click/click_dead |  | View toggle (Button) — switches grid/list view in-place. |
| #92 | `le_136` | skip | click/click_dead |  | View toggle (Button) — switches grid/list view in-place. |

### 05_Product_Page — 5 critical, 20 bonus, 10 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #2 | `le_001` | critical | navigate | ✓ | All four crops show the same 'Home' navigation link text in identical styling, representing the same nav element across different pages of the site. |
| #6 | `le_003` | critical | click/click_popout | ✓ | All four crops show the same search icon (magnifying glass) in the same header position, consistently representing the 'm-search-popup' trigger element across all four pages. |
| #9 | `le_006` | critical | navigate | ✓ | All three crops show the same shopping cart icon in the navigation bar, with the third instance showing a badge indicating 1 item in cart — same logical UI element across pages. |
| #3 | `le_007` | critical | navigate | ✓ | All three crops show an identical 'Shop' navigation link in the same style and role across the product, cart, and checkout pages. |
| #29 | `le_158` | critical | input |  | (no description; check bbox in PNG) |
| #4 | `le_002` | bonus | click/click_unknown_nav | ✓ | All four crops show the same 'Products' navigation link text in the same style, representing the same nav item across the Shop, Product, Cart, and Checkout pages — the second crop has an underline ind |
| #7 | `le_004` | bonus | click/click_unknown_nav | ✓ | All four crops show the same user/account icon and adjacent navigation icon in the same header position across all pages, indicating a consistent navigation element. |
| #8 | `le_005` | bonus | click/click_unknown_nav | ✓ | All four crops show the same pair of navigation icons (a bookmark/cart icon and a star/wishlist icon) repeated consistently across each page, indicating the same persistent nav element. |
| #5 | `le_008` | bonus | click/click_unknown_nav | ✓ | Both crops show the identical 'Pages ∨' dropdown navigation element with the same text, style, and chevron icon, consistent across both pages. |
| #10 | `le_139` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #11 | `le_140` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #12 | `le_141` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #13 | `le_142` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #14 | `le_143` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #15 | `le_144` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #16 | `le_145` | bonus | click/click_unknown_nav |  | "div.swiper-slide" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #17 | `le_146` | bonus | click/click_unknown_nav |  | "Button" is a button that likely triggers navigation to another page or route. |
| #26 | `le_155` | bonus | click/click_unknown_nav |  | "Button" is a button that likely triggers navigation to another page or route. |
| #30 | `le_159` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #31 | `le_160` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #32 | `le_161` | bonus | click/click_unknown_nav |  | "Link" is a navigation link that leads to another page in the app. |
| #33 | `le_162` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #34 | `le_163` | bonus | click/click_unknown_nav |  | "arrow" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #35 | `le_164` | bonus | click/click_unknown_nav |  | "arrow" is an unclassified clickable element; defaulting to unknown navigation as the target page is not in the dataset. |
| #36 | `le_165` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #18 | `le_147` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #19 | `le_148` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #20 | `le_149` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #21 | `le_150` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #22 | `le_151` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #23 | `le_152` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #24 | `le_153` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #25 | `le_154` | skip | click/click_dead |  | Size selector chip (Label) — in-place size selection. |
| #27 | `le_156` | skip | click/click_dead |  | "Button - Increase quantity of Denim Jacket by one" adjusts item quantity in-page; no navigation or overlay occurs. |
| #28 | `le_157` | skip | click/click_dead |  | "Button - Decrease quantity of Denim Jacket by one" adjusts item quantity in-page; no navigation or overlay occurs. |

### 06_Cart_Page — 6 critical, 7 bonus, 3 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #11 | `le_001` | critical | navigate | ✓ | All four crops show the same 'Home' navigation link text in identical styling, representing the same nav element across different pages of the site. |
| #7 | `le_003` | critical | click/click_popout | ✓ | All four crops show the same search icon (magnifying glass) in the same header position, consistently representing the 'm-search-popup' trigger element across all four pages. |
| #10 | `le_007` | critical | navigate | ✓ | All three crops show an identical 'Shop' navigation link in the same style and role across the product, cart, and checkout pages. |
| #3 | `le_168` | critical | input |  | (no description; check bbox in PNG) |
| #12 | `le_171` | critical | navigate |  | (no description; check bbox in PNG) |
| #14 | `le_173` | critical | toggle |  | (no description; check bbox in PNG) |
| #9 | `le_002` | bonus | click/click_unknown_nav | ✓ | All four crops show the same 'Products' navigation link text in the same style, representing the same nav item across the Shop, Product, Cart, and Checkout pages — the second crop has an underline ind |
| #6 | `le_004` | bonus | click/click_unknown_nav | ✓ | All four crops show the same user/account icon and adjacent navigation icon in the same header position across all pages, indicating a consistent navigation element. |
| #5 | `le_005` | bonus | click/click_unknown_nav | ✓ | All four crops show the same pair of navigation icons (a bookmark/cart icon and a star/wishlist icon) repeated consistently across each page, indicating the same persistent nav element. |
| #4 | `le_169` | bonus | click/click_unknown_nav |  | "Button" is a button that likely triggers navigation to another page or route. |
| #8 | `le_170` | bonus | click/click_unknown_nav |  | "Pages" is a content navigation link to a related page. |
| #15 | `le_174` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #16 | `le_175` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #1 | `le_166` | skip | click/click_dead |  | "Increase" adjusts item quantity in-page; no navigation or overlay occurs. |
| #2 | `le_167` | skip | click/click_dead |  | "Decrease" adjusts item quantity in-page; no navigation or overlay occurs. |
| #13 | `le_172` | skip | click/click_dead |  | "Remove" removes an item from the cart in-place; no navigation occurs. |

### 07_Check_out — 19 critical, 7 bonus, 0 skip

| ann_id | logical_id | tier | type/subtype | shared? | description |
|---|---|---|---|---|---|
| #1 | `le_001` | critical | navigate | ✓ | All four crops show the same 'Home' navigation link text in identical styling, representing the same nav element across different pages of the site. |
| #8 | `le_003` | critical | click/click_popout | ✓ | All four crops show the same search icon (magnifying glass) in the same header position, consistently representing the 'm-search-popup' trigger element across all four pages. |
| #5 | `le_006` | critical | navigate | ✓ | All three crops show the same shopping cart icon in the navigation bar, with the third instance showing a badge indicating 1 item in cart — same logical UI element across pages. |
| #2 | `le_007` | critical | navigate | ✓ | All three crops show an identical 'Shop' navigation link in the same style and role across the product, cart, and checkout pages. |
| #10 | `le_177` | critical | input |  | (no description; check bbox in PNG) |
| #11 | `le_178` | critical | input |  | (no description; check bbox in PNG) |
| #12 | `le_179` | critical | click/click_popout |  | "Country" opens a form-field selector dropdown. |
| #13 | `le_180` | critical | input |  | (no description; check bbox in PNG) |
| #14 | `le_181` | critical | input |  | (no description; check bbox in PNG) |
| #15 | `le_182` | critical | input |  | (no description; check bbox in PNG) |
| #16 | `le_183` | critical | input |  | (no description; check bbox in PNG) |
| #17 | `le_184` | critical | input |  | (no description; check bbox in PNG) |
| #18 | `le_185` | critical | toggle |  | (no description; check bbox in PNG) |
| #19 | `le_186` | critical | click/click_popout |  | "Payment Type" opens a form-field selector dropdown. |
| #20 | `le_187` | critical | input |  | (no description; check bbox in PNG) |
| #22 | `le_188` | critical | input |  | (no description; check bbox in PNG) |
| #23 | `le_189` | critical | input |  | (no description; check bbox in PNG) |
| #24 | `le_190` | critical | input |  | (no description; check bbox in PNG) |
| #25 | `le_191` | critical | toggle |  | (no description; check bbox in PNG) |
| #3 | `le_002` | bonus | click/click_unknown_nav | ✓ | All four crops show the same 'Products' navigation link text in the same style, representing the same nav item across the Shop, Product, Cart, and Checkout pages — the second crop has an underline ind |
| #7 | `le_004` | bonus | click/click_unknown_nav | ✓ | All four crops show the same user/account icon and adjacent navigation icon in the same header position across all pages, indicating a consistent navigation element. |
| #6 | `le_005` | bonus | click/click_unknown_nav | ✓ | All four crops show the same pair of navigation icons (a bookmark/cart icon and a star/wishlist icon) repeated consistently across each page, indicating the same persistent nav element. |
| #4 | `le_008` | bonus | click/click_unknown_nav | ✓ | Both crops show the identical 'Pages ∨' dropdown navigation element with the same text, style, and chevron icon, consistent across both pages. |
| #9 | `le_176` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #26 | `le_192` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |
| #27 | `le_193` | bonus | click/click_unknown_nav |  | "button" is a button that likely triggers navigation to another page or route. |

