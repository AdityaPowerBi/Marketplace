from dbm.dumb import error

from playwright.sync_api import Page, Error


print("Welcome! To become seller on the marketplace , Please enter required data....")
email = str(input("enter email : "))
name = str(input("enter your name: "))
password = str(input("enter your password: "))
confirm_password = str(input("enter your confirm_password: "))
profile_url = str(input("enter shop_name(profile url): "))


def test_directseller(page:Page,setup):

    """
    Test:Verify Seller Registration and Approval Process.
    Steps:
        1. Navigate to the seller registration page.
        2. Fill in the required details (e.g., name, email, profile URL).
        3. Submit the registration form.
        4. Verify email confirmation (if applicable).
        5. Seller will Request for Approval.
        6. Admin logs in and reviews the seller request.
        7. Admin approves/rejects the request."""

    #Step 1: Navigate to the seller registration page
    page.locator("#top_menu [href='/seller']").click()
    page.locator("[href='/seller/signup']").click()
    print(page.title())

    #Step 2. Fill in the required details (e.g., name, email, profile URL).
    page.locator("//input[@name='login']").fill(email)
    page.locator("//input[@name='name']").fill(name)
    page.locator("//input[@name='password']").fill(password)
    page.locator("//input[@name='confirm_password']").fill(confirm_password)
    page.locator("//select[@name='country_id']").select_option("2")
    page.locator("//input[@name='url_handler']").fill(profile_url)
    if page.wait_for_selector("#profile_url_error", state="attached", timeout=2000):
        if page.locator("#profile_url_error").is_visible():
            error_profile = page.locator("#profile_url_error").inner_text()
            print(f"Error: {error_profile}")
            page.close()
            return
        else:
            print("No profile URL error found.")
    else:
        print("No profile URL error appeared within timeout.")

    # Accept terms and submit form
    page.locator("input[name='mp_terms_conditions']").click()

    #============================================
    #Step 3:Submit the registration form.
    # ============================================
    page.locator(".clearfix.oe_login_buttons button[type='submit']").click()
    print("Waiting for account creation...")
    # Wait for any potential error message
    if page.locator(".alert.alert-danger").is_visible():
        error_message = page.locator(".alert.alert-danger").inner_text()
        print(f"Error: {error_message}")
        page.close()
        return
    else:
        print("No error found: Seller account created successfully.")

    #=====================================
    #Step 5:Seller will Request for Approval.
    #=======================================
    page.locator("button[name='set_to_pending']").click()
    print("Seller profile sent for request successfully.")
    page.wait_for_timeout(3000)  # Wait for 3 seconds before proceeding

    #signout the selleraccount and login the Admin
    page.locator("div.o_user_menu.d-none.d-md-block.pe-0").click()
    page.locator("//a[@data-menu='logout']").click()

    #============================================
    #Step 6:Admin logs in and reviews the seller request.
    #==========================================
    page.get_by_placeholder("Email").fill("admin")
    page.get_by_placeholder("Password").fill("webkul")
    page.locator("button.btn.btn-primary").click()

     # Navigate to Marketplace
    page.locator("div.o_navbar_apps_menu").click()
    page.locator("//a[@href='/odoo/marketplace-dashboard']").click()
     # Wait for page load
    page.wait_for_load_state("networkidle")

     #navigating to the sellers
    Sellers = page.locator("[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu1']")
    Sellers.click()

    seller_list = page.locator("a[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu1_sub_menu1']")
    seller_list.click()
    page.wait_for_timeout(3000)


    sellers = page.locator("article.o_kanban_record")
    print(f"Found {sellers.count()} sellers in the Admin list.")

    #=================================================
    # Step 7. Admin approves/rejects the request.
    #=================================================
    search_box = page.locator("input[role='searchbox']")
    search_box.fill("")
    search_box.fill(email)
    search_box.press("Enter")
    page.locator("(//article[@class='o_kanban_record d-flex cursor-pointer o_kanban_color_0 flex-grow-1 flex-md-shrink-1 flex-shrink-0'])[1]").click()
    page.locator("//button[@name='approve']").click()
    page.locator("div.modal-content button.btn.btn-primary").click()

     #publish the seller
    page.locator("//button[@name='website_publish_button']").click()
    print("Seller is successfully published")










































