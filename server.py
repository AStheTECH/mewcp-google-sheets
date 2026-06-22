#!/usr/bin/env python3
"""MCP Server for Google Sheets."""

import logging

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend

from mewcp_google_sheets.cli import parse_args
from mewcp_google_sheets.config import configure_logging
from mewcp_google_sheets.tools import register_tools

configure_logging()
logger = logging.getLogger("google-sheets-mcp-server")

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "MewCP Google Sheets MCP Server",
    middleware=[CredentialMiddleware(backend, "oauth")],
)
register_tools(mcp)

# Expose ASGI app for hosting platform's (e.g. Vercel / Cloud Run) runtime.
app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("MewCP Google Sheets MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
