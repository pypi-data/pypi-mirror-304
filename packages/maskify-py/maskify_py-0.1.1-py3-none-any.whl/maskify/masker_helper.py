import re
from email.utils import parseaddr

class MaskerHelper:
    @staticmethod
    def convert_to_cpf_format(cpf_digits: str) -> str:
        return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"

    @staticmethod
    def convert_to_cnpj_format(cnpj_digits: str) -> str:
        return f"{cnpj_digits[:2]}.{cnpj_digits[2:5]}.{cnpj_digits[5:8]}/{cnpj_digits[8:12]}-{cnpj_digits[12:]}"

    @staticmethod
    def email_try_parse(email: str) -> (bool, str):
        try:
            if "@" not in email or not MaskerHelper.email_format_validate(email):
                raise ValueError("Invalid email")

            name, address = parseaddr(email)
            if address == "":
                raise ValueError("Invalid email")

            return True, address
        except Exception:
            return False, ""

    @staticmethod
    def email_format_validate(email: str) -> bool:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def convert_to_mobile_phone_format(phone_digits: str, mask_character: str = '*') -> str:
        return f"({phone_digits[:2]}) {phone_digits[2:7]}-{phone_digits[7:]}"

    @staticmethod
    def convert_to_residential_phone_format(phone_digits: str) -> str:
        return f"({phone_digits[:2]}) {phone_digits[2:6]}-{phone_digits[6:]}"