import json
from fastapi import FastAPI
from app.api.routers import (hub, hub_configs, hub_insights, hub_metrics,
                            forex,
                            hub_reports)


with open('app/metadata.json', 'r') as f:
    metadata = json.load(f)

app = FastAPI(
    title= metadata["title_api"],
    description= metadata["description"],
    version=metadata["version_api"],
    openapi_tags=metadata["tags_metadata"]
)

app.include_router(hub.router)
app.include_router(hub_metrics.router)
app.include_router(hub_insights.router)
app.include_router(hub_reports.router)
app.include_router(hub_configs.router)
app.include_router(forex.router)
