import json
from typing import Optional

import click
import questionary

from autumn8.cli import options
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.cli.interactive import normalize_args
from autumn8.common.config.settings import CloudServiceProvider
from autumn8.common.types import Sla
from autumn8.lib import logging
from autumn8.lib.api import cloud

logger = logging.getLogger(__name__)


@click.group(context_settings={"token_normalize_func": normalize_args})
def cloud_commands_group():
    pass


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(optional=True)
@click.option(
    "-m",
    "--model_id",
    help="Model ID to get the deployments for",
    prompt_required=False,
    default=None,
)
def list_deployments(
    organization_id: int,
    model_id: int,
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """List running deployments."""
    logger.info("Fetching the list of deployments...")
    deployments = cloud.get_running_deployments(
        organization_id,
        environment,
        model_id=model_id,
        service_provider=cloud_provider,
    )

    click.echo(json.dumps(deployments, indent=4))
    return


@cloud_commands_group.command()
@click.option(
    "-hw",
    "-t",
    "--machine_type",
    type=str,
    help="Server type to use for the deployment",
    # TODO: add a better interactive prompt listing all available servers
)
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@click.option(
    "-m",
    "--model_id",
    prompt=True,
    type=int,
    help="Model ID to deploy",
    # TODO: add a better interactive prompt listing all available models
)
@click.option(
    "-b",
    "--deploy_best",
    "autopick_machine_by_best_sla",
    type=click.Choice(list(Sla), case_sensitive=False),
    help="Let Autumn8 pick the server type automatically for the deployment",
)
@options.use_cloud_provider_picker(
    # prompt disabled, as only A8F works atm
    optional=True,
    default_value=CloudServiceProvider.AUTUMN8,
)
def deploy(
    organization_id: int,
    model_id: int,
    machine_type: Optional[str],
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    autopick_machine_by_best_sla: Optional[Sla],
    quiet,
):
    """Deploy a model from AutoDL onto cloud."""

    if machine_type is None and autopick_machine_by_best_sla is None:
        machine_type = questionary.text(
            message="Machine type (ie. c5.2xlarge)"
        ).ask()

    logger.info(
        "Launching a new deployment with %s...",
        machine_type or f"best {autopick_machine_by_best_sla}",
    )
    if machine_type is not None:
        deployments = cloud.deploy(
            organization_id,
            environment,
            machine_type=machine_type,
            service_provider=cloud_provider,
            model_id=model_id,
        )
    else:
        assert autopick_machine_by_best_sla is not None

        deployments = cloud.deploy_by_best_sla(
            organization_id,
            environment,
            best_sla=autopick_machine_by_best_sla,
            service_provider=cloud_provider,
            model_id=model_id,
        )

    click.echo(json.dumps(deployments, indent=4))


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(
    # prompt disabled, as only A8F works atm
    optional=True,
    default_value=CloudServiceProvider.AUTUMN8,
)
@click.option(
    "-d",
    "--deployment_id",
    prompt=True,
    help="ID of the deployment to terminate",
)
def terminate_deployment(
    organization_id: int,
    deployment_id: str,
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """Terminate a running deployment."""
    response = cloud.terminate_deployment(
        organization_id, environment, deployment_id, cloud_provider
    )
    click.echo(json.dumps(response, indent=4))
