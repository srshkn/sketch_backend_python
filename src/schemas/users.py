from pydantic import EmailStr, Field, field_validator, model_validator

from .schemas import APIModel


class UserCreate(APIModel):
    name: str = Field(index=True, unique=True, min_length=5, max_length=20)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    password: str = Field(min_length=5, max_length=75)
    confirm_password: str = Field(min_length=5, max_length=75)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, value: str):
        if " " in value:
            raise ValueError("Пароль не должен содержать пробелы")
        if value.isdigit():
            raise ValueError("Пароль не может состоять только из цифр")
        return value

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        return self


class UserOut:
    pass
