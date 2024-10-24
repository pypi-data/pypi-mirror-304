# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.constants import (
    CURRENT_FINDING_VERSION,
    MINIMUM_FINDING_VERSION,
)


from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Finding:
    def __init__(self, rule, properties, **kwargs):
        self.events = kwargs.get("events", [])
        self.rule_id = rule.name
        self.properties = properties
        self.hash_code = rule.generate_preflight_hash(**kwargs)
        self.preflight = ",".join([rule.name, self.hash_code])

        self.routes = []
        self.version = None
        logger.debug("Created finding for %s", rule.name)
        logger.debug("initial preflight value: %s", self.preflight)

    def set_version(self):
        """
        Determine the finding version depending on its attributes.
        """
        # dataflow or non-dataflow finding with route(s)
        if self.routes:
            self.version = CURRENT_FINDING_VERSION

        # non-dataflow rules without routes
        elif not self.events:
            self.version = CURRENT_FINDING_VERSION

        # dataflow finding without routes
        else:
            self.version = MINIMUM_FINDING_VERSION


def send_finding(finding, context=None):
    """
    Send a finding by either appending it to request context
    OR sending it immediately.

    If `context` exists, agent should not sent message immediately because
    current route needs to be appended in `append_route_to_findings`

    :param finding:  api.Finding instance
    :param context: Request context instance
    :return: None
    """
    if context:
        if (
            context.input_exclusions_trigger_time
            and context.exclusions.evaluate_assess_trigger_time_exclusions(
                context, finding
            )
        ):
            return

        context.findings.append(finding)
        return

    from contrast.reporting import teamserver_messages
    from contrast.agent import agent_state

    agent_state.module.reporting_client.add_message(
        teamserver_messages.Preflight([finding], None)
    )
