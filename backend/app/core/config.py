from pydantic_settings import BaseSettings,SettingsConfigDict
from urllib.parse import quote_plus
class Settings(BaseSettings):

    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    SECRET_KEY:str


    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATABASE_URL(self):
        pwd = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

