from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8501")
        page.screenshot(path="jules-scratch/verification/dashboard_main.png")

        # Click on the expander
        page.click('text="Análisis Demográfico por Etnia y Seguro de Salud"')
        page.screenshot(path="jules-scratch/verification/dashboard_expanded_demographic.png")

        page.click('text="Análisis Laboral Detallado"')
        page.screenshot(path="jules-scratch/verification/dashboard_expanded_labor.png")

        # Click on the "Acerca de" tab
        page.click('text="Acerca de"')
        page.screenshot(path="jules-scratch/verification/dashboard_about.png")

        browser.close()

run()
