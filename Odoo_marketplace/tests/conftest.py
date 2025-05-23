import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture
def setup(page: Page):
    page.goto("http://192.168.5.139:8028/?db=Odoo_marketplace", wait_until="load")
    page.wait_for_selector("input#login")

# @pytest.fixture
# def setup2(page:Page):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("http://192.168.5.139:8028/?db=Odoo_marketplace", wait_until="load")
#         page.wait_for_selector("input#login")
#         yield context, page
#         browser.close()


