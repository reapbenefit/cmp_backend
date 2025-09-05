import os
from pydantic_settings import BaseSettings
from phoenix.otel import register

root_dir = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    openai_api_key: str
    phoenix_api_key: str | None = None
    phoenix_endpoint: str | None = None
    frappe_backend_base_url: str
    frappe_backend_client_id: str
    frappe_backend_client_secret: str
    frappe_sso_client_id: str
    frappe_sso_client_secret: str
    frappe_sso_redirect_uri: str
    env: str
    database_url: str

    class Config:
        env_file = f"{root_dir}/.env"


settings = Settings()

if settings.phoenix_api_key:
    os.environ["PHOENIX_API_KEY"] = settings.phoenix_api_key
    tracer_provider = register(
        protocol="http/protobuf",
        project_name=f"cmp-{settings.env or 'development'}",
        auto_instrument=True,
        batch=True,
        endpoint=settings.phoenix_endpoint,
    )
    tracer = tracer_provider.get_tracer(__name__)
