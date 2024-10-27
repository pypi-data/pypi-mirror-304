import unittest
from maskify.masker import Masker

class TestMaskFunction(unittest.TestCase):

    def test_mask_middle_section(self):
        result = Masker.mask("1234567890", start_position=2, length=4)
        self.assertEqual(result, "12****7890")

    def test_mask_start_section(self):
        result = Masker.mask("abcdefghij", start_position=0, length=3)
        self.assertEqual(result, "***defghij")

    def test_mask_end_section(self):
        result = Masker.mask("abcdefghij", start_position=7, length=3)
        self.assertEqual(result, "abcdefg***")

    def test_invalid_start_position(self):
        with self.assertRaises(ValueError):
            Masker.mask("abcdefghij", start_position=-1, length=3)

        with self.assertRaises(ValueError):
            Masker.mask("abcdefghij", start_position=10, length=1)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Masker.mask("abcdefghij", start_position=2, length=0)

        with self.assertRaises(ValueError):
            Masker.mask("abcdefghij", start_position=8, length=5)

    def test_empty_or_none_input(self):
        with self.assertRaises(ValueError):
            Masker.mask("", start_position=0, length=1)

        with self.assertRaises(ValueError):
            Masker.mask(None, start_position=0, length=1)

    def test_mask_cpf(self):
        cpf = "123.456.789-01"
        masked_cpf = Masker.mask_cpf(cpf, "X")
        self.assertEqual(masked_cpf, "123.XXX.XX9-01")

    def test_mask_cnpj(self):
        cnpj = "12.345.678/0001-99"
        masked_cnpj = Masker.mask_cnpj(cnpj, "X")
        self.assertEqual(masked_cnpj, "12.XXX.XXX/XX01-99")

    def test_mask_email(self):
        email = "usuario@exemplo.com"
        masked_email = Masker.mask_email(email, "*")
        self.assertEqual(masked_email, "u*****o@exemplo.com")

    def test_mask_credit_card(self):
        credit_card = "1234 1234 1234 1234"
        masked_credit_card = Masker.mask_credit_card(credit_card, "*")
        self.assertEqual(masked_credit_card, "**** **** **** 1234")

    def test_mask_mobile_phone(self):
        mobile_phone = "(11) 91234-5678"
        masked_mobile_phone = Masker.mask_mobile_phone(mobile_phone)
        self.assertEqual(masked_mobile_phone, "(11) *****-5678")

        with self.assertRaises(ValueError):
            Masker.mask_mobile_phone("(11) 1234-567")  # Telefone com menos de 11 dígitos

    def test_mask_residential_phone(self):
        residential_phone = "(11) 1234-5678"
        masked_residential_phone = Masker.mask_residential_phone(residential_phone)
        self.assertEqual(masked_residential_phone, "(11) ****-5678")

        with self.assertRaises(ValueError):
            Masker.mask_residential_phone("(11) 123-5678")  # Telefone com menos de 10 dígitos


if __name__ == "__main__":
    unittest.main()
