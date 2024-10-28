from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_PORT: str

    @property
    def MONGO_URI(self):
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/"


class Settings(MongoSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
