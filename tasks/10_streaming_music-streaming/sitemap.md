# Site Map — 10_streaming_music-streaming

Auto-generated from `interaction/*.json`. Each navigation arrow below comes from an annotation whose `type` is `navigate` and whose `navigateTo.name` points to another page.

## Pages

- **01_Onboarding** — `pages/01_Onboarding.png` · `pages/01_Onboarding.json`
- **02_Log_in_Page** — `pages/02_Log_in_Page.png` · `pages/02_Log_in_Page.json`
- **03_Sign_in_Page** — `pages/03_Sign_in_Page.png` · `pages/03_Sign_in_Page.json`
- **04_Login_successfully** — `pages/04_Login_successfully.png` · `pages/04_Login_successfully.json`
- **05_Home** — `pages/05_Home.png` · `pages/05_Home.json`
- **06_Playlist** — `pages/06_Playlist.png` · `pages/06_Playlist.json`
- **07_Browser** — `pages/07_Browser.png` · `pages/07_Browser.json`
- **08_Music_Player_Page** — `pages/08_Music_Player_Page.png` · `pages/08_Music_Player_Page.json`
- **09_Permium_Subscriptions** — `pages/09_Permium_Subscriptions.png` · `pages/09_Permium_Subscriptions.json`
- **10_Settings_-_Profile** — `pages/10_Settings_-_Profile.png` · `pages/10_Settings_-_Profile.json`
- **11_Settings_-_Detailes** — `pages/11_Settings_-_Detailes.png` · `pages/11_Settings_-_Detailes.json`
- **12_Settings_-_Contact_Us** — `pages/12_Settings_-_Contact_Us.png` · `pages/12_Settings_-_Contact_Us.json`
- **13_Settings_-_FAQ** — `pages/13_Settings_-_FAQ.png` · `pages/13_Settings_-_FAQ.json`

## Navigation graph

```
02_Log_in_Page
  ├─→ 03_Sign_in_Page
  └─→ 04_Login_successfully

03_Sign_in_Page
  └─→ 05_Home

05_Home
  ├─→ 06_Playlist (x31)
  ├─→ 07_Browser
  ├─→ 08_Music_Player_Page (x15)
  ├─→ 09_Permium_Subscriptions (x2)
  └─→ 10_Settings_-_Profile (x2)

06_Playlist
  ├─→ 05_Home
  ├─→ 07_Browser
  ├─→ 08_Music_Player_Page (x18)
  ├─→ 09_Permium_Subscriptions
  └─→ 10_Settings_-_Profile (x2)

07_Browser
  ├─→ 05_Home
  ├─→ 06_Playlist (x45)
  ├─→ 08_Music_Player_Page (x19)
  └─→ 09_Permium_Subscriptions (x3)

08_Music_Player_Page
  └─→ 10_Settings_-_Profile (x2)

09_Permium_Subscriptions
  ├─→ 05_Home
  ├─→ 06_Playlist
  └─→ 07_Browser

10_Settings_-_Profile
  ├─→ 05_Home
  ├─→ 06_Playlist
  ├─→ 07_Browser
  ├─→ 09_Permium_Subscriptions
  ├─→ 11_Settings_-_Detailes
  ├─→ 12_Settings_-_Contact_Us
  └─→ 13_Settings_-_FAQ

11_Settings_-_Detailes
  ├─→ 05_Home
  ├─→ 06_Playlist
  ├─→ 07_Browser
  ├─→ 08_Music_Player_Page (x6)
  ├─→ 09_Permium_Subscriptions
  ├─→ 10_Settings_-_Profile (x3)
  ├─→ 12_Settings_-_Contact_Us
  └─→ 13_Settings_-_FAQ

12_Settings_-_Contact_Us
  ├─→ 05_Home
  ├─→ 06_Playlist
  ├─→ 07_Browser
  ├─→ 09_Permium_Subscriptions
  ├─→ 10_Settings_-_Profile (x3)
  ├─→ 11_Settings_-_Detailes
  └─→ 13_Settings_-_FAQ

13_Settings_-_FAQ
  ├─→ 05_Home
  ├─→ 06_Playlist
  ├─→ 07_Browser
  ├─→ 10_Settings_-_Profile (x3)
  ├─→ 11_Settings_-_Detailes
  └─→ 12_Settings_-_Contact_Us

# pages with no outgoing navigate edges:
  · 01_Onboarding
  · 04_Login_successfully
```

## Per-page navigation

### 01_Onboarding
Goes to: _(none)_

### 02_Log_in_Page
_7 annotations · 2 navigate_

Goes to:
- **03_Sign_in_Page**
- **04_Login_successfully**

### 03_Sign_in_Page
_4 annotations · 1 navigate_

Goes to:
- **05_Home**

Reached from: 02_Log_in_Page

### 04_Login_successfully
Goes to: _(none)_

Reached from: 02_Log_in_Page

### 05_Home
_99 annotations · 51 navigate_

Goes to:
- **06_Playlist** (x31)
- **07_Browser**
- **08_Music_Player_Page** (x15)
- **09_Permium_Subscriptions** (x2)
- **10_Settings_-_Profile** (x2)

Reached from: 03_Sign_in_Page, 06_Playlist, 07_Browser, 09_Permium_Subscriptions, 10_Settings_-_Profile, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us, 13_Settings_-_FAQ

### 06_Playlist
_39 annotations · 23 navigate_

Goes to:
- **05_Home**
- **07_Browser**
- **08_Music_Player_Page** (x18)
- **09_Permium_Subscriptions**
- **10_Settings_-_Profile** (x2)

Reached from: 05_Home, 07_Browser, 09_Permium_Subscriptions, 10_Settings_-_Profile, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us, 13_Settings_-_FAQ

### 07_Browser
_98 annotations · 68 navigate_

Goes to:
- **05_Home**
- **06_Playlist** (x45)
- **08_Music_Player_Page** (x19)
- **09_Permium_Subscriptions** (x3)

Reached from: 05_Home, 06_Playlist, 09_Permium_Subscriptions, 10_Settings_-_Profile, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us, 13_Settings_-_FAQ

### 08_Music_Player_Page
_6 annotations · 2 navigate_

Goes to:
- **10_Settings_-_Profile** (x2)

Reached from: 05_Home, 06_Playlist, 07_Browser, 11_Settings_-_Detailes

### 09_Permium_Subscriptions
_7 annotations · 3 navigate_

Goes to:
- **05_Home**
- **06_Playlist**
- **07_Browser**

Reached from: 05_Home, 06_Playlist, 07_Browser, 10_Settings_-_Profile, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us

### 10_Settings_-_Profile
_24 annotations · 7 navigate_

Goes to:
- **05_Home**
- **06_Playlist**
- **07_Browser**
- **09_Permium_Subscriptions**
- **11_Settings_-_Detailes**
- **12_Settings_-_Contact_Us**
- **13_Settings_-_FAQ**

Reached from: 05_Home, 06_Playlist, 08_Music_Player_Page, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us, 13_Settings_-_FAQ

### 11_Settings_-_Detailes
_27 annotations · 15 navigate_

Goes to:
- **05_Home**
- **06_Playlist**
- **07_Browser**
- **08_Music_Player_Page** (x6)
- **09_Permium_Subscriptions**
- **10_Settings_-_Profile** (x3)
- **12_Settings_-_Contact_Us**
- **13_Settings_-_FAQ**

Reached from: 10_Settings_-_Profile, 12_Settings_-_Contact_Us, 13_Settings_-_FAQ

### 12_Settings_-_Contact_Us
_23 annotations · 9 navigate_

Goes to:
- **05_Home**
- **06_Playlist**
- **07_Browser**
- **09_Permium_Subscriptions**
- **10_Settings_-_Profile** (x3)
- **11_Settings_-_Detailes**
- **13_Settings_-_FAQ**

Reached from: 10_Settings_-_Profile, 11_Settings_-_Detailes, 13_Settings_-_FAQ

### 13_Settings_-_FAQ
_23 annotations · 8 navigate_

Goes to:
- **05_Home**
- **06_Playlist**
- **07_Browser**
- **10_Settings_-_Profile** (x3)
- **11_Settings_-_Detailes**
- **12_Settings_-_Contact_Us**

Reached from: 10_Settings_-_Profile, 11_Settings_-_Detailes, 12_Settings_-_Contact_Us
