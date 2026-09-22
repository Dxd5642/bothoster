from typing import Any, Dict, Optional
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

async def render_template(
        template_name: str,
        request: Request,
        context: Optional[Dict[str, Any]] = None,
        status_code: int = 200,
) -> HTMLResponse:
    if context is None:
        context = {}

        is_htmx = request.get("HX-Request") == "true"

        context["request"] = request

        context["base_template"] = "partical_base.html" if is_htmx else "base.html"

        return templates.TemplateResponse(
            request=request,
            name=template_name,
            context=context,
            status_code=status_code,
        )