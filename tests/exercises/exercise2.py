import json
import unittest

from requests import Session


class TestCaseDemoWebShop(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'http://demowebshop.tricentis.com/'

        self.sess = Session()
        self.sess.headers.update = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 95.0.4638.54 Safari / 537.36',
            'Content - Type': 'application / x - www - form - urlencoded; charset = UTF - 8'

        }

    def test_add_to_cart(self):
        add_to_cart = 'addproducttocart/details/72/1'
        body = {'product_attribute_72_5_18': 53,
                'product_attribute_72_6_19': 54,
                'product_attribute_72_3_20': 57,
                'product_attribute_72_8_30': 94,
                'addtocart_72.EnteredQuantity': 1
                }

        response = self.sess.post(self.base_url + add_to_cart, body)
        self.assertEqual(200, response.status_code)
        json_parsed = json.loads(response.text)
        self.assertIn('The product has been added to your', json_parsed['message'])
        self.assertIn('1', json_parsed['updatetopcartsectionhtml'])

    # TODO
    def test_add_to_cart_with_cookies(self):
        add_to_cart = 'addproducttocart/details/72/1'

        response = self.sess.post(self.base_url + add_to_cart, json={"product_attribute_72_5_18": "53",
                                                                     "product_attribute_72_6_19": "54",
                                                                     "product_attribute_72_3_20": "57",
                                                                     "product_attribute_72_8_30": "94",
                                                                     "addtocart_72.EnteredQuantity": "1"
                                                                     }, cookies={
            "_mkto_trk=id:470-GZN-442&token:_mch-tricentis.com-1636046052027-77390; _ga=GA1.2.316657831.1636046052; _gid=GA1.2.1163688894.1636046052; Nop.customer=b7f0a293-9125-427c-a1ea-9c2793474e45; ARRAffinity=7f10010dd6b12d83d6aefe199065b2e8fe0d0850a7df2983b482815225e42439; __utmc=78382081; __utmz=78382081.1636046194.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NopCommerce.RecentlyViewedProducts=RecentlyViewedProductIds=72; __utma=78382081.316657831.1636046052.1636072596.1636078619.7; __utmt=1; __atuvc=18%7C44; __atuvs=6184941b9f967ef2002; __utmb=78382081.3.10.1636078619"})
        self.assertEqual(200, response.status_code)
        json_parsed = json.loads(response.text)
        self.assertIn('The product has been added to your', json_parsed['message'])
        self.assertIn('1', json_parsed['updatetopcartsectionhtml'])


# <RequestsCookieJar[<Cookie ARRAffinity=7f10010dd6b12d83d6aefe199065b2e8fe0d0850a7df2983b482815225e42439 for .demowebshop.tricentis.com/>, <Cookie Nop.customer=33a36312-52e8-40be-967f-3a5b83c1253f for demowebshop.tricentis.com/>]>


if __name__ == '__main__':
    unittest.main()
