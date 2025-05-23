from playwright.sync_api import sync_playwright, Page
from pytest_playwright.pytest_playwright import browser, page

from testing.utilities import AfterSetup

# seller_email = input("Enter seller email : ")
# password = input("Enter password : ")
# requested_amount = input("Enter request amount : ")


def test_Seller_Payment(page:Page,setup):
        login_page = AfterSetup()
        login_page.login_specific_seller(page)

        page.locator("//button[@data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu3']").click()
        page.locator("//a[@data-menu-xmlid='odoo_marketplace.wk_seller_payment_request']").click()
        cashable_amount = page.locator("//div[@name='cashable_amount']")
        print(cashable_amount.text_content())
        page.locator("input#amount_0").fill("10")
        page.get_by_placeholder("Payment description").fill("text")
        page.locator("button[name='do_request']").click()
        try:
            shows_warning = page.locator("div.o_form_renderer.o_form_nosheet.o_form_editable.d-block.o_form_saved")
            print(shows_warning.text_content())
            page.locator("footer.modal-footer.justify-content-around.justify-content-md-start.flex-wrap.gap-1.w-100 button.btn.btn-primary:nth-child(1)").click()
            print("Requested amount should be less than or equal to Cashable amount :{cashable_amount}")
            page.close()
        except Exception as e:
            print("No warning shown")


        try:
            show_invalid = page.locator("div.modal-content.o_error_dialog main div p")
            print(show_invalid.text_content())
            page.locator("div.modal-content.o_error_dialog button.btn.btn-primary.o-default-button").click()
        except Exception as e:
            print("No error modal found")

        # logout seller account
        login_page.logout_seller(page)

        #login Admin
        login_page.login_admin(page)
        print("Admin is successfully login")
        page.locator("div.o_navbar_apps_menu").click()
        print("Navigating to the seller-dashboard page")
        page.locator("//a[@href='/odoo/marketplace-dashboard']").click()
        page.locator("button[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu3']").click()
        page.locator("a[href='/odoo/marketplace-seller-payments']").click()
        page.locator("button.o_searchview_dropdown_toggler.d-print-none.btn.btn-outline-secondary.o-dropdown-caret.rounded-start-0.o-dropdown.dropdown-toggle.dropdown").click()
        #Apply filter for new request
        page.locator("div.o_dropdown_container.o_filter_menu span.o-dropdown-item").nth(0).click()
        page.locator("button.o_searchview_dropdown_toggler.d-print-none.btn.btn-outline-secondary.o-dropdown-caret.rounded-start-0.o-dropdown.dropdown-toggle.dropdown").click()
        page.locator("tr.o_data_row:nth-child(1)").click()
        page.locator("button[name='do_validate']").click()
        print("Validate the invoice")
        page.locator("button[name='do_Confirm_and_view_invoice']").click()
        print("Confirm and view invoice")
        page.locator("button[name='action_post']").click()
        page.locator("button#account_invoice_payment_btn").click()
        page.locator("button[name='action_create_payments']").click()






























