import unittest

from ip_checker import analyze_input, find_ip_addresses


class IpCheckerTests(unittest.TestCase):
    def test_valid_ipv4_public_address(self):
        result = analyze_input("8.8.8.8")
        self.assertEqual(result["kind"], "ipv4")
        self.assertTrue(result["is_public"])
        self.assertEqual(result["category"], "global")

    def test_private_ipv4_address(self):
        result = analyze_input("192.168.1.1")
        self.assertEqual(result["kind"], "ipv4")
        self.assertFalse(result["is_public"])
        self.assertEqual(result["category"], "private")

    def test_loopback_address(self):
        result = analyze_input("127.0.0.1")
        self.assertEqual(result["category"], "loopback")

    def test_valid_ipv6_address(self):
        result = analyze_input("2001:db8::1")
        self.assertEqual(result["kind"], "ipv6")
        self.assertEqual(result["category"], "documentation")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            analyze_input("not-an-ip")

    def test_find_ip_addresses_in_text(self):
        result = find_ip_addresses("The server is 8.8.8.8 and backup is 192.168.1.10")
        self.assertEqual(result, ["8.8.8.8", "192.168.1.10"])


if __name__ == "__main__":
    unittest.main()
