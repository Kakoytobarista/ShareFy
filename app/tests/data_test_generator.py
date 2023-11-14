from abc import ABC, abstractmethod

from faker import Faker

faker = Faker()

class AbstractAuthDataGen(ABC):

    @abstractmethod
    def get_data(self):
        raise NotImplemented

class AuthDataGen(AbstractAuthDataGen):
    def __init__(self, email: str = faker.email(), hashed_password: str = faker.password()):
        self.email = email
        self.hashed_password = hashed_password

    def get_data(self):
        return {"email": self.email, "hashed_password": self.hashed_password}
