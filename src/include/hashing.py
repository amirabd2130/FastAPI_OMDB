import bcrypt


class Hashing:
    def hash(self, string: str):
        string_bytes = string.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=string_bytes, salt=salt).decode('utf8')

    def verify(self, plain_string: str, hashed_string: str):
        plain_string_byte = plain_string.encode("utf-8")
        if isinstance(hashed_string, str):
            hashed_string_byte = hashed_string.encode("utf-8")
        else:
            hashed_string_byte = hashed_string

        return bcrypt.checkpw(password=plain_string_byte, hashed_password=hashed_string_byte)
