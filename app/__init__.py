import logging
from pathlib import Path
from config import DevelopmentConfig
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from app.controllers import index
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.graphs.route_nlp import nlp
from app.logs.app_logs import CustomizeLogger
#from autocomplete import models

# with open("app/page/nlp/nlp.txt", "r") as f:
#     text = f.read()
# models.train_models(text)

# Initialize FastAPI
app = FastAPI(
    title="VIZB API",
    description="Backend API",
    # version="2.0",
    docs_url="/docs",
    redoc_url=None,
    debug=DevelopmentConfig.DEBUG,
    # swagger="2.0"
)

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("log_config.json")
logger = CustomizeLogger.make_logger(config_path)


# def init_db():
    # cur, conn = db_v_connect()
    # load_staging_tables(cur, conn)


def create_app():
    # init_db()
    # app.add_middleware(GZipMiddleware)
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"]
)
    app.include_router(index.index)
    app.include_router(nlp)
    return app
