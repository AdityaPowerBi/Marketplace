import random

from playwright.sync_api import Page, sync_playwright

from models.Orderplacing import OrderPlacing
from testing.utilities import AfterSetup


def test_verify_rating_reviews(page: Page, setup, context):
    """
    Test:-Verify Rating & Reviews Submission and Approval Process
    Precondition: Order should be confirmed.
Steps:
    1. Log in as a customer.
    2. Navigate to the Sellers List and select a Seller.
    3. Click on Rating & Reviews tab and Write a Review.
    4. Admin logs in and reviews the submitted feedback.
   5. Admin publish the review on website.
"""
    # Initialize custom login and setup helper

    login = AfterSetup()

    # ========================
    # Step 1: Login as Customer
    # ========================
    login.login_customer(page)

    # Precondition: Order should be confirmed.
    Orders = OrderPlacing(page)
    order_number, seller_names = Orders.order()
    # clicking on the seller list , new window is opening

    #=======================================================
    #Step 2: Navigate to the Sellers List and select a Seller.
    #========================================================

    with context.expect_page() as new_tab_info:
        page.locator("a[href='/sellers/list']").click()
        new_tab = new_tab_info.value
        new_tab.wait_for_load_state()
        search = new_tab.wait_for_selector("div.js_sale input[name='search']", timeout=5000)
        print("✅ Clicked search input in new tab")

        # search.fill(seller_names[0])
        search.fill(seller_names[0])
        search.press("Enter")

        # Select seller
        seller = new_tab.locator(
            "div.o_wsale_product_grid_wrapper.o_wsale_product_grid_wrapper_1_1.p-3 a.view-profile").first
        seller.wait_for(state="visible", timeout=10000)

        seller.click()
        new_tab.wait_for_load_state("networkidle")

        # =========================================
        # Step 3. Click on Rating & Reviews tab and Write a Review
        # =========================================

        # Go to the review tab
        new_tab.locator("ul#shop-nav-tabs a[href='#rating_review_tab']").click()
        print("------------------------")
        new_tab.locator("//button[@data-bs-toggle='modal']").click()

        # Give Rating
        print("Clicking on the star rating...")
        # new_tab.wait_for_selector("div.star-rating.rating-sm.rating-active", timeout=5000)
        print("🟡 Setting rating value to 4...")
        rating_input = new_tab.locator("#rating-star")
        rating_input.wait_for(state="attached", timeout=5000)
        new_tab.evaluate("""
            const ratingInput = document.querySelector('#rating-star');
            if (ratingInput) {
                ratingInput.value = '4';
                ratingInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)
        print("✅ Rating set successfully.")

        new_tab.get_by_placeholder("Write review title").fill("Good")
        new_tab.locator("//textarea[@id='summary']").fill("I feel product is good")

        # submit the review
        new_tab.locator("button#btn-create-review").click()
        print("Review submit")
        reply_message = new_tab.locator("span#submit-msg").text_content()
        print(reply_message)

        # close the new window
        new_tab.locator("div.modal-header.py-0.mt-4 button.btn-close").click()
        new_tab.close()

        # went back to the previous page
        page.bring_to_front()
        page.evaluate("window.scrollTo(0, 0)")

        login.logout_customer(page)
        # visible_logout.scroll_into_view_if_needed()
        # visible_logout.click()

        page.locator("a.o_nav_link_btn.nav-link.border.px-3").click()

    #=======================================================
    # Step 4. Admin logs in and reviews the submitted feedback.
    #=======================================================
    login.login_admin(page)
    print("Successfully login Admin account")
    page.locator("div.o_navbar_apps_menu").click()
    page.locator("a[href='/odoo/marketplace-dashboard']").click()
    print("Navigating to the seller dashboard page")
    page.locator("button[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu1']").click()
    page.locator("a[href='/odoo/marketplace-seller-reviews']").click()
    page.locator(
        "button.o_searchview_dropdown_toggler.d-print-none.btn.btn-outline-secondary.o-dropdown-caret.rounded-start-0.o-dropdown.dropdown-toggle.dropdown").click()
    page.locator(
        "div.o_dropdown_container.o_filter_menu.w-100.w-lg-auto.h-100.px-3.mb-4.mb-lg-0.border-end span[role='menuitemcheckbox']:nth-child(3)").click()
    page.locator(
        "button.o_searchview_dropdown_toggler.d-print-none.btn.btn-outline-secondary.o-dropdown-caret.rounded-start-0.o-dropdown.dropdown-toggle.dropdown").click()
    page.locator(
        "div.o_kanban_renderer.o_renderer.d-flex.o_kanban_ungrouped.align-content-start.flex-wrap.justify-content-start article:first-child").click()
    # publishing the reviews

    #=============================================
    # Step 5. Admin publish the review on website.
    #=============================================
    page.locator(
        ".o-form-buttonbox.d-print-none.position-relative.d-flex.w-md-auto.o_not_full button[name='toggle_website_published']").click()
    print("Review published successfully")




















