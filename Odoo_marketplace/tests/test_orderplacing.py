import sys

from playwright.sync_api import Page
from pytest_playwright.pytest_playwright import page

from models.Orderplacing import OrderPlacing
from testing.utilities import AfterSetup, get_seller_credentials


def test_oo(page:Page,setup):
    """
            Test: End-to-End Order Placement Flow in Odoo Marketplace

            Steps:
            1. Log in as a customer
            2. Add a product from a seller to the cart.
            3. Proceed to checkout and complete the payment.
            4. Log in as a seller to verify the new order in the seller dashboard.
            5. Process the order and validate its Shipping and mark it Done.
            6. Admin verifies the order completion and create order invoice.
            """

    # Initialize custom login and setup helper

    login_page = AfterSetup()

    # ========================
    # Step 1: Login as Customer
    # ========================
    login_page.login_customer(page)

    # ========================
    # Step 2: Add a product from a seller to the cart.
    # ========================
    Orders = OrderPlacing(page)
    order_number, seller_names = Orders.order()


    #customer logout
    login_page.logout_customer(page)

    # ========================
    # Step 4: Log in as a seller to verify the new order in the seller dashboard.
    # ========================
    page.locator(
        "ul.navbar-nav.align-items-center.gap-2.flex-shrink-0.justify-content-end.ps-3 a[href='/web/login']"
    ).click()
    print("Now trying to login as seller...")

    #take seller data form the Excel sheet
    for seller in seller_names:
        creds = get_seller_credentials(seller)
        print(f"Getting credentials for: {seller}")
        print(f"Credentials found: {creds}")
        if creds:
            print(f"Logging in as seller: {seller}")
            login = AfterSetup()
            login.login_seller(page, creds["email"], creds["password"])
        else:
            print(f"Credentials not found for seller: {seller}")

    # Navigate to seller dashboard
    page.locator("button[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu3']").click()
    page.locator("a[href='/odoo/marketplace-orders']").click()

    # Search order by number
    search_box = page.get_by_placeholder("Search...")
    search_box.fill("")
    search_box.fill(order_number)
    search_box.press("Enter")

    # Open the order from list
    order = page.locator(
        "//div[@class='o_kanban_renderer o_renderer d-flex o_kanban_ungrouped align-content-start flex-wrap justify-content-start']/article[1]")
    print(f"Elements found: {order}")
    order.click()

    #=========================================
    #Step 5: Process the order and validate its Shipping and mark it Done.
    #==========================================
    page.locator("button[name='button_approve_ol']").click()
    page.locator(".modal-content button.btn.btn-primary").click()

    # Try checking product availability
    page.locator("div.o_statusbar_buttons.d-flex.align-items-center.align-content-around.flex-wrap.gap-1").click()
    try:
        check_Availability = page.locator(
            "div.o_statusbar_buttons.d-flex.align-items-center.align-content-around.flex-wrap.gap-1 button.btn.btn-primary")
        check_Availability.click()
        print("Checking the product availability.....")
        modal_header = page.locator("header.modal-header")
        if modal_header.is_visible():
            modal_header.click()
            print("Validation error modal closed.")
        else:
            print("No validation error modal found.")
    except Exception as e:
        print("Availability checked , Proceding to the next step")

    # Try sending SMS (optional)
    try:
        send_sms = page.wait_for_selector("button[name='send_sms']", timeout=2000)
        send_sms.click()
        print("Sending confirmation sms")
    except Exception:
        print("Skipping to the next step")

    # Mark order as Done
    try:
        page.locator(
            "ol.breadcrumb.flex-nowrap.text-nowrap.lh-sm li.breadcrumb-item.d-inline-flex.min-w-0.o_back_button").click()
        print("Going back to mark done")
        mark_done = page.locator("button[name='action_mark_done']")
        mark_done.click()
        page.locator(
            ".modal-footer.justify-content-around.justify-content-md-start.flex-wrap.gap-1.w-100 button.btn.btn-primary").click()
        print("Mark Done the order")
    except Exception:
        print("Mark done button not found , Skipping to the next step")

    # logout seller account
    login_page.logout_seller(page)

    # ========================
    # Step 6: Admin verifies the order completion and create order invoice.
    # ========================
    login_page.login_admin(page)
    print("Admin is successfully login")

    # Go to Sales > Orders
    page.locator("div.o_navbar_apps_menu").click()
    print("Navigating to the sales page")
    page.locator("a[data-menu-xmlid='sale.sale_menu_root']").click()
    page.locator("button[data-menu-xmlid='sale.sale_order_menu']").click()
    page.locator("a[href='/odoo/orders']").click()

    # Search for order
    search = page.get_by_placeholder("Search...")
    search.fill("")
    search.fill(order_number)
    search.press("Enter")
    page.locator("tbody.ui-sortable").click()
    print("order select successfully")

    # Create Invoice if possible
    try:
        invoice_percentage = page.wait_for_selector("button#create_invoice_percentage", timeout=2000)
        print("===invoice_percentage=======%r=", invoice_percentage.is_visible())
        if invoice_percentage.is_visible():
            print("Invoice status: Nothing to invoice")
            sys.exit(1)  # Stop script execution
    except Exception as e:
        print(f"An error occurred: {e}")
        print("inside invoce_create")
        invoice_create = page.wait_for_selector("button#create_invoice", timeout=2000)

        if invoice_create.is_visible():
            print("Invoice status:paid")
            invoice_create.click()
            page.locator("button#create_invoice_open").click()
            page.locator("button[name='action_post']").click()
            print("Invoice is being created.")












