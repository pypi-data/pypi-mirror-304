from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec, SpecValidator
from digitalhub.entities.task._base.models import K8s


class RunSpec(Spec):
    """RunSpec specifications."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        **kwargs,
    ) -> None:
        self.task = task
        self.local_execution = local_execution
        self.function = function
        self.node_selector = node_selector
        self.volumes = volumes
        self.resources = resources
        self.affinity = affinity
        self.tolerations = tolerations
        self.envs = envs
        self.secrets = secrets
        self.profile = profile


class RunValidator(SpecValidator, K8s):
    """
    RunValidator validator.
    """

    function: str = None
    """The function associated with the run."""

    task: str = None
    """The task string associated with the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
