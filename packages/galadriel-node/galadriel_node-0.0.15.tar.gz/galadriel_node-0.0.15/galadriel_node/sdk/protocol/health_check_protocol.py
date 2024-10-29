import json
from typing import Any
from typing import List

import rich

from fastapi.encoders import jsonable_encoder

from galadriel_node.config import config
from galadriel_node.sdk.protocol.entities import (
    HealthCheckRequest,
    HealthCheckResponse,
    HealthCheckMessageType,
    HealthCheckGPUUtilization,
)
from galadriel_node.sdk.system import report_utilization
from galadriel_node.sdk.system.entities import NodeUtilization


# pylint: disable=too-few-public-methods,
class HealthCheckProtocol:
    PROTOCOL_NAME = "health-check"
    PROTOCOL_VERSION = "1.0"

    def __init__(self):
        rich.print(f"{self.PROTOCOL_NAME}: Protocol initialized")

    async def handle(self, data: Any, my_node_id: str) -> str | None:
        try:
            request = HealthCheckRequest(**data)
        except Exception:
            rich.print(f"{self.PROTOCOL_NAME}: Invalid data received: {data}")
            return None

        rich.print(
            f"{self.PROTOCOL_NAME}: Received health request for {request.node_id}, "
            f"nonce: {request.nonce}"
        )
        if _protocol_validations(my_node_id, request) is False:
            return None

        if config.GALADRIEL_ENVIRONMENT == "local":
            utilization = NodeUtilization(
                cpu_percent=50,
                ram_percent=50,
                disk_percent=50,
                gpus=[],
            )
        else:
            utilization = await report_utilization.execute()
        gpus = _convert_gpu_stats(utilization)
        health_check_response = HealthCheckResponse(
            protocol_version=self.PROTOCOL_VERSION,
            node_id=request.node_id,
            nonce=request.nonce,
            cpu_percent=utilization.cpu_percent,
            ram_percent=utilization.ram_percent,
            disk_percent=utilization.disk_percent,
            gpus=gpus,
        )

        data = jsonable_encoder(health_check_response)
        response_message = json.dumps({"protocol": self.PROTOCOL_NAME, "data": data})
        rich.print(
            f"{self.PROTOCOL_NAME}: Sent health check response , "
            f"nonce: {health_check_response.nonce}, "
        )
        return response_message


def _protocol_validations(
    my_node_id: str, health_check_request: HealthCheckRequest
) -> bool:
    if my_node_id != health_check_request.node_id:
        rich.print(
            f"{HealthCheckProtocol.PROTOCOL_NAME}: Ignoring health check received for unexpected node "
            f"{health_check_request.node_id}"
        )
        return False
    if health_check_request.message_type != HealthCheckMessageType.HEALTH_CHECK_REQUEST:
        rich.print(
            f"{HealthCheckProtocol.PROTOCOL_NAME}: Received message other than health check from node "
            f"{health_check_request.node_id}, {health_check_request.message_type}"
            f"{HealthCheckMessageType.HEALTH_CHECK_REQUEST}"
        )
        return False
    if health_check_request.protocol_version != HealthCheckProtocol.PROTOCOL_VERSION:
        rich.print(
            f"{HealthCheckProtocol.PROTOCOL_NAME}: Received health check with invalid protocol version from node "
            f"{health_check_request.node_id}"
        )
        return False
    return True


def _convert_gpu_stats(utilization: NodeUtilization) -> List[HealthCheckGPUUtilization]:
    return [
        HealthCheckGPUUtilization(
            gpu_percent=gpu.gpu_percent, vram_percent=gpu.vram_percent
        )
        for gpu in utilization.gpus
    ]
