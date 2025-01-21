# Apollo_Automation

This Python script automates data enrichment tasks on Apollo.io, such as selecting contacts, enriching email data, and navigating through multiple pages of lists. It is designed to save time by automating repetitive tasks within the Apollo.io platform.

## Features
- **Automated Login:** Logs in to Apollo.io using provided credentials.
- **Contact Processing:** Automatically selects contacts on a given list and applies enrichment actions.
- **Email Enrichment:** Executes the "Enrich emails" action for selected contacts.
- **Pagination Handling:** Navigates through multiple pages of a list and processes each page sequentially.
- **Error Handling:** Handles common issues like stale elements, timeouts, and intercepted clicks with retries.

---

## Prerequisites
1. **Python:** Ensure Python 3.7 or higher is installed on your system.
2. **Selenium:** Install Selenium using the following command:
   ```bash
   pip install selenium
   ```
3. **ChromeDriver:** Download the appropriate version of ChromeDriver for your Chrome browser from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/). Add the `chromedriver` executable to your system's PATH.
4. **Apollo.io Account:** You need valid Apollo.io credentials to log in.

---

## Script Usage

### 1. Clone or Download the Repository
Save the script file on your local machine.

### 2. Update the Configuration
Replace the placeholders in the script with your details:
- `EMAIL`: Your Apollo.io login email.
- `PASSWORD`: Your Apollo.io password.
- `list_urls`: Replace `"xyz url"` with the list of Apollo.io URLs you want to process.

### 3. Run the Script
Run the script using Python:
```bash
python script_name.py
```

---

## Script Functions

### 1. `login_to_apollo(driver, wait)`
- Navigates to the Apollo.io login page and logs in with the provided credentials.
- Waits until the dashboard loads before proceeding.

### 2. `process_list(driver, wait, list_url)`
- Processes a specific list URL by:
  - Selecting all contacts on the page.
  - Clicking the "Enrich" button and choosing the "Enrich emails" option.
  - Navigating to the next page and repeating the process.

### 3. `main()`
- Handles overall script execution:
  - Calls the login function.
  - Iterates over a list of URLs to process.

---

## Error Handling
- **Retries:** The script retries failed interactions due to stale elements or timeouts.
- **Logs:** Provides detailed console logs for each step, including errors and their resolutions.

---

## Limitations
- **Dynamic Website Changes:** If Apollo.io changes its interface or element structure, the script might require updates.
- **Credential Security:** Avoid hardcoding sensitive information in the script; use environment variables or a secure credential manager if possible.

---

## Disclaimer
This script is intended for educational purposes only. Ensure compliance with Apollo.io's terms of service before using it for automation. Use at your own risk.

