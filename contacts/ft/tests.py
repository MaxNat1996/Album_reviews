from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase


class AdminTest(LiveServerTestCase):
    # load fixtures
    fixtures = ['admin.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_admin_site(self):
        # user opens web browser, navigates to admin page
        self.browser.get(self.live_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # users types in username and passwords and presses enter
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # login credentials are correct, and the user is redirected to the main admin page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # user clicks on the Users link
        user_link = self.browser.find_elements_by_link_text('Users')
        user_link[0].click()

        # user verifies that user live@forever.com is present
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('live@forever.com', body.text)

    def test_create_contact(self, data_list):
        # user opens web browser, navigates to admin page, and logs in
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # user clicks on the Persons link
        persons_links = self.browser.find_elements_by_link_text('Persons')
        persons_links[0].click()

        # user clicks on the Add person link
        add_person_link = self.browser.find_element_by_link_text('Add person')
        add_person_link.click()

        # user fills out the form
        self.browser.find_element_by_name('first_name').send_keys(data_list[0])
        self.browser.find_element_by_name('last_name').send_keys(data_list[1])
        self.browser.find_element_by_name('email').send_keys(data_list[2])
        self.browser.find_element_by_name('address').send_keys(data_list[3])
        self.browser.find_element_by_name('city').send_keys(data_list[4])
        self.browser.find_element_by_name('state').send_keys(data_list[5])
        self.browser.find_element_by_name('country').send_keys(data_list[6])

        # user clicks the save button
        self.browser.find_element_by_css_selector("input[value='Save']").click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(data_list[7], body.text)

    def test_create_contact_admin(self):
        admin_data_list = ["Max", "Natalchuk", "maksnat25@gmail.com",
                           "22120 Kovalsky Lane", "Kiev", "Ukraine", "Natalchuk, Max"]

        self.test_create_contact(self, admin_data_list)

        # user returns to the main admin screen
        home_link = self.browser.find_element_by_link_text('Home')
        home_link.click()

        # user clicks on the Phones link
        persons_links = self.browser.find_elements_by_link_text('Phones')
        persons_links[0].click()

        # user clicks on the Add phone link
        add_person_link = self.browser.find_element_by_link_text('Add phone')
        add_person_link.click()

        # user finds the person in the dropdown
        el = self.browser.find_element_by_name("person")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Natalchuk, Max':
                option.click()

        # user adds the phone numbers
        self.browser.find_element_by_name('number').send_keys("0960591136")

        # user clicks the save button
        self.browser.find_element_by_css_selector("input[value='Save']").click()

        # the Phone has been added
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0960591136', body.text)

        # user logs out
        self.browser.find_element_by_link_text('Log out').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Thanks for spending some quality time with the Web site today.', body.text)

    def test_create_contact_admin_raise_error(self):
        false_contact_data = ["test@", "tester", "test@tester.com",
                              "2227 Tester Lane", "Tester City", "TCA", "Invalid"]
        self.test_create_contact(self, false_contact_data)


class UserContactTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_create_contact(self, data_list):
        # user opens web browser, navigates to home page
        self.browser.get(self.live_server_url + '/')

        # user clicks on the Persons link
        add_link = self.browser.find_elements_by_link_text('Add Contact')
        add_link[0].click()

        # user fills out the form
        self.browser.find_element_by_name('first_name').send_keys(data_list[0])
        self.browser.find_element_by_name('last_name').send_keys(data_list[1])
        self.browser.find_element_by_name('email').send_keys(data_list[2])
        self.browser.find_element_by_name('address').send_keys(data_list[3])
        self.browser.find_element_by_name('city').send_keys(data_list[4])
        self.browser.find_element_by_name('country').send_keys(data_list[5])
        self.browser.find_element_by_name('number').send_keys(data_list[6])

        # user clicks the save button
        self.browser.find_element_by_css_selector("input[value='Add']").click()

        # the Person has been added
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(data_list[7], body.text)

    def test_without_error(self):
        create_contact_data = ["Max", "Natalchuk", "maksnat25@gmail.com",
                               "22120 Kovalsky Lane", "Kiev", "Ukraine", "0960591136", "maksnat25@gmail.com"]
        self.test_create_contact(self, create_contact_data)

    def test_with_error(self):
        create_contact_data = ["test@", "tester", "test@tester.com",
                               "2227 Tester Lane", "Tester City", "TCA", "415888888888", "Invalid"]
        self.test_create_contact(self, create_contact_data)






