# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License in the project root for
# license information.
# --------------------------------------------------------------------------
import fastapi
from azure.monitor.opentelemetry import configure_azure_monitor

# Configure Azure monitor collection telemetry pipeline
configure_azure_monitor(
    connection_string="<your-connection-string>",
    disable_logging=True,
    disable_metrics=True,
    instrumentation_config={
        "fastapi": {
            "excluded_urls": "http://127.0.0.1:8000/exclude",
        }
    },
    tracing_export_interval_ms=15000,
)

app = fastapi.FastAPI()


# Requests made to fastapi endpoints will be automatically captured
@app.get("/")
async def test():
    return {"message": "Hello World"}


# Exceptions that are raised within the request are automatically captured
@app.get("/exception")
async def exception():
    raise Exception("Hit an exception")


# Telemetry from this endpoint will not be captured due to excluded_urls config above
@app.get("/exclude")
async def exclude():
    return {"message": "Telemetry was not captured"}
