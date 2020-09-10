from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import HtmlTestRunner
import time


class Testsnapmart(unittest.TestCase):
    ############################################### login ##########################################
    username = "caisamgab@test.com"
    password = "Password123!"
    ############################################### select item ####################################
    First = "Apple Juice (1000ml)"
    Second = "Banana Juice (1000ml)"
    Third = "Carrot Juice (1000ml)"
    add_cart = (By.XPATH, '//div[contains(text(),"{}")]/ancestor::mat-card/child::div['
                          '@class="product"]/following-sibling::div/child::Button[@aria-label="Add to Basket"]')
    checkout_cart = (By.XPATH, '//mat-cell[contains(text(), "{}")]')
    ############################################# delivery option ###################################
    """ mat-radio-41-input = One day delivery, 
    mat-radio-42-input = fast delivery, 
    mat-radio-43-input  = standard delivery """
    delivery_option = "mat-radio-42-input"
    delivery_choice = (By.XPATH, '//label[@for ="{}"]/child::div')
    ############################################# delivery option ###################################
    payment_option = "credit card"
    ############################################# Confirmation ###################################
    order_summary = (By.XPATH, '//mat-cell[contains(text(), "{}")]')
    price = (By.XPATH, '//mat-cell[contains(text(), "{}")]/following-sibling::mat-cell')
    quantity = (By.XPATH, '//mat-cell[contains(text(), "{}")]/following-sibling::mat-cell')
    price_check1 = "1.99¤"
    #############################################################################
    driver = webdriver.Chrome(executable_path="../webdriver/chromedriver.exe")
    driver.get("https://test.cuongnguyen.online")
    driver.maximize_window()

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.option_selected = None

    def test_step1_login_credentials(self):
        self.driver.find_element(By.XPATH, '//a[contains(text(),"Me want it!")]').click()
        self.driver.find_element(By.XPATH, '//Button[@aria-label="Close Welcome Banner"]').click()
        self.driver.find_element(By.XPATH, '//Button[@id="navbarAccount"]').click()
        # Element for account_login will be available after account is click
        self.driver.find_element(By.XPATH, '//Button[@id="navbarLoginButton"]').click()
        self.driver.get_screenshot_as_file('./screenshot/login_screen.png')

        # login_fields will be available/displayed after account_login is click
        self.driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(self.username)
        self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(self.password)

    def test_step2_login_success(self):
        # Login_button will be enable after populating Username and Password
        self.driver.find_element(By.XPATH, '//Button[@aria-label="Login"]').click()
        time.sleep(2)
        self.driver.get_screenshot_as_file('./screenshot/Successful_login.png')

    # class TestMenu(unittest.TestCase):
    def test_step3_menu_selection(self):
        self.driver.find_element(By.XPATH, '//div[contains(text(),"All Products")]').is_displayed()

        add_cart_selecta = (self.add_cart[0], self.add_cart[1].format(self.First))
        add_cart_select1 = self.driver.find_element(*add_cart_selecta)
        add_cart_selectb = (self.add_cart[0], self.add_cart[1].format(self.Second))
        add_cart_select2 = self.driver.find_element(*add_cart_selectb)
        add_cart_selectc = (self.add_cart[0], self.add_cart[1].format(self.Third))
        add_cart_select3 = self.driver.find_element(*add_cart_selectc)

        add_cart_select1.click()
        time.sleep(1)
        basket_count1 = self.driver.find_element_by_xpath(
            '//span[contains(@class, "fa-layers-counter fa-layers-top-right fa-3x warn-notification")]').text
        self.assertEqual(basket_count1, '1', "not the correct count")  # validate the basket counter
        add_cart_select2.click()
        time.sleep(1)
        basket_count2 = self.driver.find_element_by_xpath(
            '//span[contains(@class, "fa-layers-counter fa-layers-top-right fa-3x warn-notification")]').text
        self.assertEqual(basket_count2, '2', "not the correct count")  # validate the basket counter
        add_cart_select3.click()
        time.sleep(1)
        basket_count3 = self.driver.find_element_by_xpath(
            '//span[contains(@class, "fa-layers-counter fa-layers-top-right fa-3x warn-notification")]').text
        self.assertEqual(basket_count3, '3', "not the correct count")  # validate the basket counter
        self.driver.get_screenshot_as_file('./screenshot/add_to_cart.png')
        time.sleep(1)

    def test_step4_menu_basket(self):
        self.driver.find_element(By.XPATH, '//Button[@class = "mat-focus-indicator buttons mat-button mat-button-base '
                                           'ng-star-inserted"]').click()
        self.driver.get_screenshot_as_file('./screenshot/view_cart.png')
        self.driver.find_element(By.XPATH, '// h1[contains(text(), " Your Basket ")]').is_displayed()

        checkout_cart_a = (self.checkout_cart[0], self.checkout_cart[1].format(self.First))
        checkout_cart_1 = self.driver.find_element(*checkout_cart_a)
        checkout_cart_1.is_displayed()  # verify 1st selected in menu is displayed in cart
        checkout_cart_b = (self.checkout_cart[0], self.checkout_cart[1].format(self.Second))
        checkout_cart_2 = self.driver.find_element(*checkout_cart_b)
        checkout_cart_2.is_displayed()  # verify 2nd selected in menu is displayed in cart
        checkout_cart_c = (self.checkout_cart[0], self.checkout_cart[1].format(self.Third))
        checkout_cart_3 = self.driver.find_element(*checkout_cart_c)
        checkout_cart_3.is_displayed()  # verify 3rd selected in menu is displayed in cart
        time.sleep(1)

        """ checkout """

        self.driver.find_element(By.XPATH, '//button[@class="mat-focus-indicator checkout-button mat-raised-button '
                                           'mat-button-base mat-primary"]').click()

    def test_step5_Select_address(self):
        """ Select an address """
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//h1[contains(text(), "Select an address")]').is_displayed()
        self.driver.find_element(By.XPATH, '//mat-radio-button[@class= "mat-radio-button mat-accent"]').click()
        self.driver.get_screenshot_as_file('./screenshot/Select_address.png')
        self.driver.find_element(By.XPATH, '//Button[@aria-label="Proceed to payment selection"]').click()

    def test_step6_delivery_speed(self):
        """choose a delivery speed"""
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//h1[contains(text(), "Delivery Address")]').is_displayed()
        self.driver.find_element(By.XPATH, '//h1[contains(text(), "Choose a delivery speed")]').is_displayed()

        radio_button = self.delivery_choice[0], self.delivery_choice[1].format(self.delivery_option)
        self.driver.find_element(*radio_button).click()  # select delivery speed
        self.driver.get_screenshot_as_file('./screenshot/delivery_option.png')
        self.driver.find_element(By.XPATH, '//Button[@aria-label="Proceed to delivery method selection"]').click()

    def test_step7_payment_option(self):
        """Payment Option"""
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//h1[contains(text(), "My Payment Options")]').is_displayed()

        if self.payment_option == "wallet":
            self.driver.get_screenshot_as_file('./screenshot/payment_option.png')
            self.driver.find_element(By.XPATH, '//Button[@class="mat-focus-indicator btn mat-raised-button '
                                               'mat-button-base mat-primary"]').click()
        else:
            self.driver.find_element(By.XPATH, '//label[@for ="mat-radio-44-input"]/child::div').click()
            self.driver.get_screenshot_as_file('./screenshot/payment_option.png')
            self.driver.find_element(By.XPATH, '//Button[@aria-label="Proceed to review"]').click()

    def test_step7_plase_order(self):
        """Place Order and Pay"""
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Place your order and pay")]').is_displayed()
        self.driver.get_screenshot_as_file('./screenshot/Place_order.png')
        self.driver.find_element(By.XPATH, '//Button[@aria-label="Complete your purchase"]').click()

    def test_step8_confirmation_page(self):
        """Confirmation Page"""
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//h1[contains(text(), "Thank you for your purchase!")]').is_displayed()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Track Orders")]').is_displayed()
        self.driver.find_element(By.XPATH, '//mat-cell[contains(text(), "Apple Juice (1000ml) ")]').is_displayed()
        """Validate Order"""
        order_a = (self.order_summary[0], self.order_summary[1].format(self.First))
        order1 = self.driver.find_element(*order_a)
        order1.is_displayed()
        order_b = (self.order_summary[0], self.order_summary[1].format(self.First))
        order2 = self.driver.find_element(*order_b)
        order2.is_displayed()
        order_c = (self.order_summary[0], self.order_summary[1].format(self.First))
        order3 = self.driver.find_element(*order_c)
        order3.is_displayed()
        """Price"""

        price1 = (self.price[0], self.price[1].format(self.First))
        price_a = self.driver.find_element(*price1)
        price_check1 = price_a.text

        self.assertEqual(price_check1, '1.99¤', "not the correct price")  # validate price

        """Quantity"""
        quantity1 = (self.quantity[0], self.quantity[1].format(self.price_check1))
        quantity_a = self.driver.find_element(*quantity1)
        quantity_check1 = quantity_a.text
        self.assertEqual(quantity_check1, '1', "not the correct quantity")  # validate quantity


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='Test_Evidence'))
