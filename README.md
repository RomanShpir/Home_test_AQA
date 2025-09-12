# 🎮 Twitch & IPstack Automation – Tests (Selenium + Requests + Pytest)

A small testing project that combines:
- **UI tests** for Twitch (mobile emulation via Chrome + Selenium).
- **API tests** for **IPstack** using pure Python `requests`.
- Clean **Page Object** design for both UI and API.
- Centralized **validation** utilities (no asserts/ifs in the test layer for API).

## ⚙️ Dependency Installation

```bash
# From the project root
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r automation-home-work/requirements.txt
```

**Requirements (from `requirements.txt`):**
- `selenium`
- `pytest`
- `pytest-env`
- `webdriver-manager`
- `requests`

> Chrome/Chromedriver is handled by **webdriver-manager** automatically.

## 🔧 Environment Variables

### Create a pytest.ini file in the automation-home-work/test_scripts folder.
```
[pytest]

env =
    ; UI General
    UI_URL = https://m.twitch.tv/

    ; API General
    API_URL = http://api.ipstack.com
    API_ACCESS_KEY = API_ACCESS_KEY
```

### To get API_ACCESS_KEY, sign up for a free API key at [ipstack.com](https://ipstack.com/signup/free).

## ▶ How to Run Tests

From the **`twitch-automation-home-work/test_scripts`** folder:

```bash
# Run all tests
pytest -v

# Run only UI tests
pytest -v regression/ui_tests

# Run only API tests
pytest -v regression/api_tests
```

## 🎥 Demo – UI Test Execution

Below is a GIF showing how the UI test runs in mobile emulation:

![UI Test Execution](ui_test.gif)

## 🧪 Page Object Structure & Main Classes

```
twitch-automation-home-work/
├─ Library/
│  ├─ api/
│  │  ├─ IpStackPage.py        # API Page Object + ResponseWrapper
│  │  └─ Validators.py         # Validator classes for API responses
│  └─ ui/
│     ├─ BasePage.py           # Core Selenium helpers, waits & validations
│     ├─ BrowsePage.py         # Twitch “Browse” page interactions
│     └─ Navigation.py         # Navigation helpers (open URL, menu, scroll, popups)
├─ test_scripts/
│  ├─ conftest.py              # Fixtures (Api, Ui, Chrome setup w/ mobile emulation)
│  ├─ main_api_constructor.py  # Api wrapper exposing ip_stack: IpStackPage
│  ├─ main_ui_constructor.py   # Ui wrapper exposing Navigation & BrowsePage
│  └─ regression/
│     ├─ api_tests/
│     │  └─ test_api_ip_stack_endpoint.py   # Parametrized API tests (validators)
│     └─ ui_tests/
│        └─ test_ui_navigate_base_page.py   # UI end-to-end Twitch flow
└─ requirements.txt
```

### UI Page Objects
- **BasePage.py** – DOM waits, clickables, screenshots, video readiness check.
- **BrowsePage.py** – Search input, category selection, stream opening.
- **Navigation.py** – Base page opening, menu navigation, scrolling, popup handling.

### API Page Object
- **IpStackPage.py** – `standard_lookup`, `bulk_lookup`, wraps responses.
- **Validators.py** – `StatusCodeIs`, `IsJSON`, `JsonFieldEquals`, `JsonHasKeys`, `JsonExactKeys`, `IsXML`, `HeaderStartsWith`, `ContentContains`.

## 📊 Written Test Cases (Table)

### UI – Twitch Flow
| ID   | Action / Step             | Validation / Outcome                                                                 |
|------|--------------------------|-------------------------------------------------------------------------------------|
| UI-1 | Open base page            | Page loads successfully                                                             |
| UI-2 | Click Browse              | Element clickable, DOM loaded                                                       |
| UI-3 | Close popup if present    | ESC key sent, popup dismissed                                                       |
| UI-4 | Search category           | Input accepts text                                                                  |
| UI-5 | Verify category in list   | Element present                                                                     |
| UI-6 | Select category           | Correct category clicked                                                             |
| UI-7 | Scroll bottom             | Content loads via lazy loading                                                       |
| UI-8 | Open random stream        | Random stream opened                                                                 |
| UI-9 | Wait for stream to load   | `<video>` present, readyState=4                                                      |
| UI-10| Clear popups              | ESC key ensures no obstruction                                                       |
| UI-11| Take screenshot           | Screenshot saved on teardown                                                         |

### API – IPstack
| ID    | Endpoint                 | Params          | Validators                                                                              |
|-------|-------------------------|-----------------|-----------------------------------------------------------------------------------------|
| API-1 | /134.201.250.155         | None            | StatusCodeIs(200), IsJSON, JsonFieldEquals(ip), JsonHasKeys(country_name)               |
| API-2 | /160.39.144.19           | hostname=1      | StatusCodeIs(200), IsJSON, JsonFieldEquals(ip), JsonHasKeys(hostname)                   |
| API-3 | /134.201.250.155         | language=ru     | StatusCodeIs(200), IsJSON, JsonFieldEquals(ip), JsonHasKeys(country_name)               |
| API-4 | /134.201.250.155         | fields=zip      | StatusCodeIs(200), IsJSON, JsonExactKeys(zip)                                          |
| API-5 | /160.39.144.19           | output=xml      | StatusCodeIs(200), IsXML, HeaderStartsWith(Content-Type, application/xml), ContentContains(<ip>) |
| API-6 | Bulk lookup              | hostname=0      | StatusCodeIs(200), IsJSON, JsonIsList, JsonListLenIs(2), JsonListAllHaveKeys(ip, country_name) |
| API-7 | Bulk lookup              | hostname=1      | StatusCodeIs(200), IsJSON, JsonIsList, JsonListLenIs(2), JsonListAllHaveKeys(ip, hostname)     |

## 🧰 Validation Used & Why
- **StatusCodeIs** – ensures HTTP request succeeded.
- **IsJSON/IsXML** – ensures correct content format.
- **JsonFieldEquals** – ensures correct IP returned.
- **JsonHasKeys/JsonExactKeys** – ensures required fields present or filtered.
- **HeaderStartsWith** – ensures MIME type correctness.
- **ContentContains** – ensures expected XML structure.
- **JsonIsList/JsonListLenIs/JsonListAllHaveKeys** – ensures bulk response correctness.
- **UI waits & video readiness** – stabilize UI flows and confirm playback readiness.
