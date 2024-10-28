import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

# from src.common.middleware import OPLogMiddleware
from junoaccessmanager.src.core import router
# from src.events.initialize import lifespan
from junoaccessmanager.src.settings import settings

from junoaccessmanager.src.core.database import engine_mysql, Base_mysql

Base_mysql.metadata.create_all(bind=engine_mysql)


def create_app():
    app = FastAPI(
        # lifespan=lifespan,
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        summary=settings.PROJECT_SUMMARY,
        version=settings.PROJECT_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url=f"/{settings.API_PREFIX}/openapi.json" if settings.API_PREFIX else "/openapi.json",
    )

    if settings.API_PREFIX:
        static_url = f"/{settings.API_PREFIX}/static"
        docs_url = f"/{settings.API_PREFIX}/docs"
        redoc_url = f"/{settings.API_PREFIX}/redoc"
        swagger_js_url = f"/{settings.API_PREFIX}/static/swagger-ui-bundle.js"
        swagger_css_url = f"/{settings.API_PREFIX}/static/swagger-ui.css"
        redoc_js_url = f"/{settings.API_PREFIX}/static/swagger-ui.css"
    else:
        static_url = "/static"
        docs_url = "/docs"
        redoc_url = "/redoc"
        swagger_js_url = "/static/swagger-ui-bundle.js",
        swagger_css_url = "/static/swagger-ui.css",
        redoc_js_url = "/static/redoc.standalone.js",

    app.mount(static_url, StaticFiles(directory="src/static"), name="static")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            summary=settings.PROJECT_SUMMARY,
            description=settings.PROJECT_DESCRIPTION,
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {"url": "/static/shuhan.png"}
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    @app.get(docs_url, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=swagger_js_url,
            swagger_css_url=swagger_css_url,
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(redoc_url, include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=redoc_js_url,
        )

    # app.add_middleware(OPLogMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.RUNNING_PORT, timeout_keep_alive=600)
