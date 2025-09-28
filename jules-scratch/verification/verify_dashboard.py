from playwright.sync_api import sync_playwright, expect, Page

def verify_dashboard(page: Page):
    """
    Navigates to the Streamlit dashboard, waits for it to load,
    and takes a screenshot.
    """
    # 1. Navigate to the app
    # Streamlit's default port is 8501
    url = "http://localhost:8501"
    print(f"Navigating to {url}...")
    page.goto(url, timeout=60000) # Increased timeout for app to start

    # 2. Wait for a key element to be visible
    # We'll wait for the main H1 title of the dashboard
    print("Waiting for dashboard title to be visible...")
    title_locator = page.get_by_role("heading", name="Análisis de Series Temporales para Lima (2024-2025)")

    # Use expect to wait for the element to be visible
    expect(title_locator).to_be_visible(timeout=30000)
    print("Dashboard title is visible.")

    # 3. Take a screenshot for verification
    screenshot_path = "jules-scratch/verification/dashboard_verification.png"
    print(f"Taking screenshot and saving to {screenshot_path}...")
    page.screenshot(path=screenshot_path)
    print("Screenshot taken successfully.")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_dashboard(page)
        except Exception as e:
            print(f"An error occurred during verification: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()