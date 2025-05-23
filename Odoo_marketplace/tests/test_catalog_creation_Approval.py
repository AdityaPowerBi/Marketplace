from playwright.sync_api import Page

from models.ProductPage import TestProductCreation
from testing.utilities import AfterSetup

print("Welcome to the product creation")
"""
Steps:
    1. Log in as a seller.
    2. Navigate to the Products section and click 'Create New Product'.
    3. Fill in product details (Product Name, Price, Website Product Category, etc.).
    4. Create the inventory request.
    5. Submit the product for admin approval.
    6. Admin logs in and verifies the product details.
    7. Admin approves/rejects the product.
    8. Admin approves the inventory request.
"""



def test_product_by_seller(page:Page,setup):
      login_page = AfterSetup()

      #========================================
      # step 1 : Log in as a seller.
      #========================================
      login_page.login_specific_seller(page)


      #========================================
      # step 2: Navigate to the Products section and click 'Create New Product'.
      #=========================================
      Product = TestProductCreation(page)
      Product.open_product_menu()
      Product.open_product_section()

      #=========================================
      #step 3 : Fill in product details (Product Name, Price, Website Product Category, etc.).
      #=========================================
      Product.create_new_product()
      Product.enter_product_name()
      Product.select_product_category()
      Product.check_track_inventory()
      Product.enter_product_price()
      Product.save_product()
      Product.send_product_for_approval()
      print("Product of name Test_Product is successfully created")

      #==============================================
      # step 4. Create the inventory request.
      #==============================================
      print("Create Request for Inventory updation")
      Product.inventory_request()
      Product.new_inventory_created()
      Product.fill_product_quantity()
      Product.save()

      # ===================================
      # step 5. Submit the product for admin approval.
      # ==================================
      Product.send_request()
      print("Inventory request for quantity : 10 is successfully send")

      try:
          error_messages = page.wait_for_selector(".modal-body .text-prewrap", timeout=2000)
          if error_messages.is_visible():
              print(f"Validation error: {error_messages.text_content()}")
          else:
              print("No Validation error found")
          return
      except Exception:
          print(f"No Validation error found")

      try:
          warning = page.wait_for_selector("div.o_notification_body.mt-2 li", timeout=2000)
          if warning.is_visible():
              print(f"invalid field : {warning.text_content()} , Quantity should be a whole number")
          else:
              print("No warning message")
          return
      except Exception:
          print("No Warning message")

          # signout the selleraccount and login the Admin
      page.locator("div.o_user_menu.d-none.d-md-block.pe-0").click()
      page.locator("//a[@data-menu='logout']").click()
      print("Successfully Logout the seller account")


      #========================================
      # step 6. Admin logs in and verifies the product details.
      #========================================
      login_page.login_admin(page)
      print("Login via Admin credentials")

      product = TestProductCreation(page)
      product.open_home_menu()
      product.navigate_to_dashboard()
      product.open_product_menu()
      product.open_product_section()
      search_box = page.locator("input[role='searchbox']")
      search_box.fill("")
      search_box.fill("Test_Product")
      search_box.press("Enter")
      page.locator(
          "//div[@class='o_kanban_renderer o_renderer d-flex o_kanban_ungrouped align-content-start flex-wrap justify-content-start']/article[1]").click()

      #===========================================
      # step 7. Admin approves/rejects the product.
      #===========================================
      page.locator("//button[@name='approved']").click()
      page.locator("div.modal-content button.btn.btn-primary").click()
      print("Test_Product is successfully approved by Admin")

      # published the product
      page.locator("//button[@name='toggle_website_published']").click()
      print("Product is successfully published By Admin")

      #===========================================
      # step 8. Admin approves the inventory request.
      #==================================================
      page.locator("//button[@type='action']").click()
      page.locator("//td[@name='product_temp_id']").click()
      page.locator("//button[@name='approve']").click()
      page.locator(".modal-content button.btn.btn-primary").click()
      print("inventory request is approved By Admin")






