from playwright.sync_api import Page

class TestProductCreation:
    def __init__(self, page: Page):
        self.page = page
        # self.name_of_product = name_of_product
        # self.product_price = product_price
        # self.product_quantity = product_quantity

        # Locators
        self.home_menu = page.locator("div.o_navbar_apps_menu")
        self.marketplace_dashboard = page.locator("//a[@href='/odoo/marketplace-dashboard']")
        self.product = page.locator("//a[@href='/odoo/marketplace-products']")
        self.new_product = page.locator(".d-inline-flex.gap-1 button[type='button']")
        self.product_name = page.locator("//input[@id='name_0']")
        self.category = page.get_by_placeholder("Category...")
        self.select_category = page.locator("#public_categ_ids_0_0_0")
        self.product_type = page.locator(f"div[name='type'] div[role='radiogroup'][value='0']")
        self.track_inventory = page.locator("div[name='is_storable']")
        self.select_seller = page.locator("#marketplace_seller_id_0")
        self.product_price_field = page.locator("input#list_price_0")
        self.save_button = page.locator("//button[@data-tooltip='Save manually']")
        self.send_for_approval = page.locator("[name='set_pending']")
        self.inventory = page.locator("//button[@type='action']")
        self.new_inventory = page.locator(".btn.btn-primary.o_list_button_add")
        self.Product_quantity = page.locator("#new_quantity_0")
        self.save_manually = page.locator("//button[@data-tooltip='Save manually']")
        self.request = page.locator("button[name='request']")



    # Methods
    def open_home_menu(self):
        self.home_menu.click()

    def navigate_to_dashboard(self):
        self.marketplace_dashboard.click()

    def open_product_menu(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector("[data-menu-xmlid='odoo_marketplace.wk_seller_dashboard_menu2']", timeout=2000).click()

    def open_product_section(self):
        self.product.click()

    def create_new_product(self):
        self.new_product.click()

    def enter_product_name(self):
        self.product_name.fill("Test_Product")

    def select_product_category(self):
        self.category.click()
        self.select_category.click()

    def select_product_type(self):
        self.product_type.click()

    def check_track_inventory(self):
        self.track_inventory.click()

    def choose_seller(self):
        self.select_seller.click()

    def enter_product_price(self):
        self.product_price_field.clear()
        self.product_price_field.fill("200")

    def save_product(self):
        self.save_button.click()

    def send_product_for_approval(self):
        self.send_for_approval.click()

    def inventory_request(self):
        self.inventory.click()

    def new_inventory_created(self):
        self.new_inventory.click()

    def fill_product_quantity(self):
        self.Product_quantity.fill("10")

    def save(self):
        self.save_manually.click()

    def send_request(self):
        self.request.click()
















