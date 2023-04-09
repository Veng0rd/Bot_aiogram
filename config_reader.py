from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    rate_price_token: SecretStr
    url_price: str

    # Вложенный класс с дополнительными указаниями для настроек
    class Config:
        # Имя файла, откуда будут прочитаны данные
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
