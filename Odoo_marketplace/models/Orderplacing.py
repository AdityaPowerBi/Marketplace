import random
from typing import Tuple, List

from playwright.sync_api import Page


class OrderPlacing:
    def __init__(self, page: Page):
        self.page = page

    def order(self) -> Tuple[str, List[str]]:
        # Step 1: Navigate to the shop
        self.page.locator("ul#top_menu a[href='/shop']").click()

        # Step 2: Locate all available products
        elements = self.page.locator(
            "//div[@id='products_grid']/div[@class='o_wsale_products_grid_table_wrapper pt-3 pt-lg-0']/section/div"
        ).all()
        product_found = len(elements)

        if product_found == 0:
            print("No products found!")
            return ""

        print(f"Found {product_found} products.")

        # Randomly select 1 product
        selected_indices = random.sample(range(product_found), min(1, product_found))
        successfully_added = 0
        seller_names = []

        for index in selected_indices:
            product = elements[index]
            product_name = product.locator(".o_wsale_products_item_title.mb-2.text-break").text_content()
            print(f"Selecting product: {product_name}")

            product.locator(".o_wsale_products_item_title.mb-2.text-break").click()

            try:
                add_to_cart_button = self.page.locator("#add_to_cart")

                if add_to_cart_button.is_visible():
                    add_to_cart_button.click()

                    # Capture seller name after adding to cart
                    seller_name = self.page.locator("//a[@itemprop='name']").text_content()
                    seller_names.append(seller_name)

                    self.page.wait_for_timeout(2000)
                    proceed_to_checkout = self.page.locator("button.btn.btn-primary")

                    if proceed_to_checkout.is_visible():
                        print(f"{product_name} requires additional confirmation. Handling it...")
                        proceed_to_checkout.click()
                    else:
                        print(f"{product_name} added to cart successfully!")

                    successfully_added += 1
                else:
                    print(f"Failed to add {product_name} to cart!")

            except Exception as e:
                print(f"Error while adding {product_name}: {e}")

            # Return to the shop
            self.page.locator("ul#top_menu a[href='/shop']").click()

        # ========================
        # Step 3: Proceed to checkout and complete the payment.
        # ========================
        self.page.locator("#o_main_nav li.o_wsale_my_cart a[href='/shop/cart']").click()


        if successfully_added == len(selected_indices):
            print("All selected products added to cart! Proceeding to final checkout...")
            self.page.locator("//a[@name='website_sale_main_button']").click()
            self.page.locator("//button[@name='o_payment_submit_button']").click()
            print("Clicked on 'Pay' button, waiting for order confirmation...")
        else:
            print("Not all products were added to cart. Order will NOT be placed.")
            return ""

        # Step 4: Retrieve order number
        order_number_element = self.page.wait_for_selector(
            "div.oe_cart.col-12.col-lg-7 div.mb-4 em span:nth-child(2)", timeout=10000
        )
        order_number = order_number_element.text_content()
        print(f"✅ Order number: {order_number}")

        # Step 5: Logout and prepare for seller login
        print(f"Order placed for seller(s): {seller_names}")
        # self.page.locator(
        #     "ul.navbar-nav.align-items-center.gap-2.flex-shrink-0.justify-content-end.ps-3 a[href='/web/login']"
        # ).click()
        # print("Now trying to login as seller...")

        return order_number, seller_names
