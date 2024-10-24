# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast_fireball import ObservedRoute
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast.utils.timer import now_ms
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class _Traces(BaseTsAppMessage):
    """This class should only be instantiated by Preflight's response handler"""

    def __init__(self, finding, reportable_request):
        super().__init__()

        self.headers.update({"Report-Hash": finding.preflight.split(",")[-1]})

        self.body = self._build_body(finding, reportable_request)

    @property
    def name(self) -> str:
        return "traces"

    @property
    def path(self) -> str:
        return "traces"

    @property
    def request_method(self):
        return requests.Session.put

    @fail_loudly("Failed to process Traces response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)

    def _route_to_json(self, route: ObservedRoute):
        return {
            # "The number of times this route was observed; must be more than 0"
            "count": 1,
            "observations": [{"url": route.url, "verb": route.verb}],
            "signature": route.signature,
        }

    def _build_body(self, finding, reportable_request):
        base_body = {
            "created": (
                finding.events[-1].timestamp_ms if len(finding.events) > 0 else now_ms()
            ),
            "events": [event.to_json() for event in finding.events],
            "properties": finding.properties,
            "routes": [self._route_to_json(route) for route in finding.routes],
            "ruleId": finding.rule_id,
            "tags": self.settings.config.assess_tags,
            "version": finding.version,
        }
        if session_id := self.settings.config.session_id:
            base_body["session_id"] = session_id
        if reportable_request is not None:
            base_body["request"] = reportable_request

        return base_body
