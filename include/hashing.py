import bcrypt


class Hashing():
    def Hash(string: str):
        stringBytes = string.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=stringBytes, salt=salt).decode('utf8')

    def Verify(plainString: str, hashedString: str):
        plainStringByte = plainString.encode("utf-8")
        if isinstance(hashedString, str):
            hashedStringByte = hashedString.encode("utf-8")
        else:
            hashedStringByte = hashedString

        return bcrypt.checkpw(password=plainStringByte, hashed_password=hashedStringByte)
