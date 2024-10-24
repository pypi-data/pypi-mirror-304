import json
import warnings
from abc import ABC
from typing import Optional

from braket.aws import AwsDevice, AwsSession
from braket.aws.queue_information import QueueDepthInfo
from braket.circuits import GateCalibrations
from braket.device_schema import DeviceCapabilities
from braket.device_schema.pulse.frame_v1 import Frame
from braket.pulse import Port
from networkx import DiGraph
from planqk.backend import PlanqkBackend
from planqk.client.model_enums import Provider, BackendType, BackendStatus
from planqk.decorators import not_implemented, not_supported


class PlanqkAwsDevice(PlanqkBackend, AwsDevice, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def arn(self) -> str:
        warnings.warn("PlanQK AWS devices are identified by their id instead of the ARN.", UserWarning)
        return self.backend_info.internal_id

    @property
    @not_supported
    def aws_session(self) -> AwsSession:
        pass

    def refresh_metadata(self) -> None:
        """Refresh the `PlanqkAwsDevice` object with the most recent Device metadata."""
        self._backend_info = self._planqk_client.get_backend(backend_id=self.backend_info.id)

    @property
    def type(self) -> str:
        """str: Return the device type"""
        return "SIMULATOR" if self.backend_info.type == BackendType.SIMULATOR else "QPU"

    @property
    def backend_provider(self) -> str:
        return Provider.AWS.name

    @property
    def provider_name(self) -> str:
        """str: Return the provider name"""
        return self.backend_info.hardware_provider.name

    @property
    @not_implemented
    def ports(self) -> dict[str, Port]:
        """Returns a dict mapping port ids to the port objects for predefined ports
        for this device.
        """
        pass

    @property
    @not_implemented
    def gate_calibrations(self) -> Optional[GateCalibrations]:
        """Calibration data for a QPU. Calibration data is shown for gates on particular gubits.
        If a QPU does not expose these calibrations, None is returned.

        Returns:
            Optional[GateCalibrations]: The calibration object. Returns `None` if the data
            is not present.
        """
        pass

    @property
    def is_available(self) -> bool:
        """Returns true if the device is currently available.

        Returns:
            bool: Return if the device is currently available.
        """
        planqk_status: BackendStatus = self._planqk_client.get_backend_state(self._backend_info.id).status
        return True if planqk_status == BackendStatus.ONLINE else False

    @property
    def status(self) -> str:
        planqk_status: BackendStatus = self._planqk_client.get_backend_state(self._backend_info.id).status
        return "ONLINE" if planqk_status == BackendStatus.PAUSED else planqk_status.name

    @property
    def properties(self) -> DeviceCapabilities:
        """DeviceCapabilities: Return the device properties

        Please see `braket.device_schema` in amazon-braket-schemas-python_

        .. _amazon-braket-schemas-python: https://github.com/aws/amazon-braket-schemas-python
        """
        config = self._planqk_client.get_backend_config(self._backend_info.id)
        return DeviceCapabilities.parse_raw(json.dumps(config))

    @property
    @not_implemented
    def topology_graph(self) -> DiGraph:
        """DiGraph: topology of device as a networkx `DiGraph` object.

        Examples:
            >>> import networkx as nx
            >>> device = AwsDevice("arn1")
            >>> nx.draw_kamada_kawai(device.topology_graph, with_labels=True, font_weight="bold")

            >>> topology_subgraph = device.topology_graph.subgraph(range(8))
            >>> nx.draw_kamada_kawai(topology_subgraph, with_labels=True, font_weight="bold")

            >>> print(device.topology_graph.edges)

        Returns:
            DiGraph: topology of QPU as a networkx `DiGraph` object. `None` if the topology
            is not available for the device.
        """
        pass

    @property
    @not_implemented
    def frames(self) -> dict[str, Frame]:
        """Returns a dict mapping frame ids to the frame objects for predefined frames
        for this device.
        """
        pass

    @property
    @not_implemented
    def ports(self) -> dict[str, Port]:
        """Returns a dict mapping port ids to the port objects for predefined ports
        for this device.
        """
        pass

    @not_implemented
    def queue_depth(self) -> QueueDepthInfo:
        """Task queue depth refers to the total number of quantum tasks currently waiting
        to run on a particular device.

        Returns:
            QueueDepthInfo: Instance of the QueueDepth class representing queue depth
            information for quantum tasks and hybrid jobs.
            Queue depth refers to the number of quantum tasks and hybrid jobs queued on a particular
            device. The normal tasks refers to the quantum tasks not submitted via Hybrid Jobs.
            Whereas, the priority tasks refers to the total number of quantum tasks waiting to run
            submitted through Amazon Braket Hybrid Jobs. These tasks run before the normal tasks.
            If the queue depth for normal or priority quantum tasks is greater than 4000, we display
            their respective queue depth as '>4000'. Similarly, for hybrid jobs if there are more
            than 1000 jobs queued on a device, display the hybrid jobs queue depth as '>1000'.
            Additionally, for QPUs if hybrid jobs queue depth is 0, we display information about
            priority and count of the running hybrid job.

        """
        pass

    @not_implemented
    def refresh_gate_calibrations(self) -> Optional[GateCalibrations]:
        """Refreshes the gate calibration data upon request.

        If the device does not have calibration data, None is returned.

        Raises:
            URLError: If the URL provided returns a non 2xx response.

        Returns:
            Optional[GateCalibrations]: the calibration data for the device. None
            is returned if the device does not have a gate calibrations URL associated.
        """
        pass

