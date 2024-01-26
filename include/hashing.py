import bcrypt


class Hashing():
    def Hash(string: str):
        stringBytes = string.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=stringBytes, salt=salt)

    def Verify(plainString: str, hashedString: str):
        plainStringByte = plainString.encode("utf-8")
        hashedStringByte = hashedString
        return bcrypt.checkpw(password=plainStringByte, hashed_password=hashedStringByte)
