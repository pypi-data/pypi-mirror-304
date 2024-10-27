from maskify.masker_helper import MaskerHelper


class Masker:
    @staticmethod
    def mask(value: str, start_position: int, length: int, mask_character: str = '*') -> str:
        if value is None or value.strip() == "":
            raise ValueError("No data was provided for masking")
        if start_position < 0 or start_position >= len(value):
            raise ValueError("startPosition is out of range")
        if length <= 0 or start_position + length > len(value):
            raise ValueError("length is out of range")

        result = list(value)

        for i in range(start_position, start_position + length):
            result[i] = mask_character

        return "".join(result)

    @staticmethod
    def mask_cpf(cpf: str, mask_character: str = '*') -> str:
        if cpf is None or cpf.strip() == "":
            raise ValueError("CPF not provided.")

        cpf_digits = [c for c in cpf if c.isdigit()]

        if len(cpf_digits) != 11:
            raise ValueError("CPF must have 11 digits.")

        for i in range(3, 8):
            cpf_digits[i] = mask_character

        return MaskerHelper.convert_to_cpf_format("".join(cpf_digits))

    @staticmethod
    def mask_cnpj(cnpj: str, mask_character: str = '*') -> str:
        if cnpj is None or cnpj.strip() == "":
            raise ValueError("CNPJ not provided.")

        cnpj_digits = [c for c in cnpj if c.isdigit()]

        if len(cnpj_digits) != 14:
            raise ValueError("CNPJ must have 14 digits.")

        for i in range(2, 10):
            cnpj_digits[i] = mask_character

        return MaskerHelper.convert_to_cnpj_format("".join(cnpj_digits))

    @staticmethod
    def mask_email(email: str, mask_character: str = "*"):
        if not email or email.strip() == "":
            raise ValueError("Email not provided.")

        is_valid, email_parsed = MaskerHelper.email_try_parse(email=email)

        if not is_valid:
            raise ValueError("Invalid email.")

        at_position = email_parsed.index("@")
        result = list(email_parsed)
        for i in range(1, at_position - 1):
            result[i] = mask_character
        return "".join(result)

    @staticmethod
    def mask_credit_card(credit_card: str, mask_character: str = '*') -> str:
        if credit_card is None or credit_card.strip() == "":
            raise ValueError("Credit card not provided.")

        digits_only = [c for c in credit_card if c.isdigit()]
        num_digits = len(digits_only)

        is_default = num_digits == 16 and len(credit_card.split(' ')) == 4
        is_amex = num_digits == 15 and len(credit_card.split(' ')) == 3
        is_diners_club = num_digits == 14 and len(credit_card.split(' ')) == 3

        if not is_default and not is_amex and not is_diners_club:
            raise ValueError("Invalid credit card.")

        result = list(credit_card)

        max_length = 15
        if is_amex:
            max_length = 14
        elif is_diners_club:
            max_length = 13

        for i in range(max_length):
            if result[i] != " ":
                result[i] = mask_character

        return "".join(result)

    @staticmethod
    def mask_mobile_phone(phone: str, mask_character: str = '*') -> str:
        if phone is None or phone.strip() == "":
            raise ValueError("Phone number not provided.")

        phone_digits = [c for c in phone if c.isdigit()]

        if len(phone_digits) != 11:
            raise ValueError("The mobile phone number must have 11 digits (9 digits + area code).")

        for i in range(2, 7):
            phone_digits[i] = mask_character

        return MaskerHelper.convert_to_mobile_phone_format("".join(phone_digits))

    @staticmethod
    def mask_residential_phone(phone: str, mask_character: str = '*') -> str:
        if phone is None or phone.strip() == "":
            raise ValueError("Phone number not provided.")

        # Remove qualquer formatação e mantém apenas os dígitos
        phone_digits = [c for c in phone if c.isdigit()]

        # Verifica se o telefone tem exatamente 10 dígitos (DDD + 8 dígitos)
        if len(phone_digits) != 10:
            raise ValueError("The landline phone number must have 10 digits (8 digits + area code).")

        # Aplica a máscara nos dígitos do meio (índices de 2 a 5)
        for i in range(2, 6):
            phone_digits[i] = mask_character

        return MaskerHelper.convert_to_residential_phone_format("".join(phone_digits))
