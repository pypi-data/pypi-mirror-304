import os
import re
import sys

import click

from builddeck.helpers.config import load_config_new, ServiceNotFoundError
from builddeck.helpers.docker_compose import run_docker_compose, destroy_docker_compose, generate_docker_compose
from builddeck.helpers.get_logging import logger
from builddeck.helpers.processes import package_all_services, clean_all_services, verify_all_services, build_and_deploy_all_services, maven_test_all_services

def get_current_version():
    try:
        setup_file = os.path.join(os.path.dirname(__file__), 'setup.py')
        with open(setup_file, 'r') as file:
            setup_content = file.read()
            version_match = re.search(r"version=['\"]([^'\"]*)['\"]", setup_content)
            if version_match:
                return version_match.group(1)
            else:
                return "Unknown"
    except Exception:
        return "Unknown"


@click.group()
@click.option('--env', default='', help='Set the environment (e.g. dev, prod, staging)')
@click.option('--services', default='', help='Comma-separated list of services to include')
@click.pass_context
@click.version_option(version=get_current_version(), prog_name="BuildDeck", message="%(prog)s version %(version)s")
def cli(ctx, env, services):
    """BuildDeck CLI tool for automating services management tasks."""
    ctx.ensure_object(dict)
    ctx.obj['ENV'] = env
    ctx.obj['SERVICES'] = services.split(',') if services else []


def load_configuration(ctx):
    """Load configuration with context environment and services."""
    try:
        services, services_yml, environment = load_config_new(ctx.obj['ENV'], ctx.obj['SERVICES'])
        return services, services_yml, environment
    except ServiceNotFoundError as e:
        logger.error(f"❌ Service not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)

@cli.command()
@click.option('-s', '--single', is_flag=True, help='Operate on a single service instead of all services')
@click.pass_context
def mvn_build(ctx, single):
    """Build all services using Maven."""
    try:
        services, _, _ = load_configuration(ctx)
        if single and services:
            services = services[:1]  # Only process the first service as an example
        package_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.option('-s', '--single', is_flag=True, help='Operate on a single service instead of all services')
@click.pass_context
def mvn_test(ctx, single):
    """Test all services using Maven."""
    try:
        services, _, _ = load_configuration(ctx)
        if single and services:
            services = services[:1]  # Only process the first service as an example
        maven_test_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.option('-s', '--single', is_flag=True, help='Operate on a single service instead of all services')
@click.pass_context
def mvn_clean(ctx, single):
    """Clean all services using Maven."""
    try:
        services, _, _ = load_configuration(ctx)
        if single and services:
            services = services[:1]  # Only process the first service as an example
        clean_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.option('-s', '--single', is_flag=True, help='Operate on a single service instead of all services')
@click.pass_context
def mvn_verify(ctx, single):
    """Verify all services using Maven."""
    try:
        services, _, _ = load_configuration(ctx)
        if single and services:
            services = services[:1]  # Only process the first service as an example
        verify_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def build(ctx):
    """Build and deploy all services."""
    try:
        services, _, environment = load_configuration(ctx)
        build_and_deploy_all_services(services, environment, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def deploy(ctx):
    """Deploy all services and run Docker Compose."""
    try:
        services, services_yml, environment = load_configuration(ctx)
        build_and_deploy_all_services(services, environment, os.getcwd())
        run_docker_compose(services_yml, environment)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def compose(ctx):
    """Generate Docker Compose file."""
    try:
        _, services_yml, environment = load_configuration(ctx)
        generate_docker_compose(services_yml, environment)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def up(ctx):
    """Run Docker Compose."""
    try:
        _, services_yml, environment = load_configuration(ctx)
        run_docker_compose(services_yml, environment)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def down(ctx):
    """Stop and remove Docker Compose services."""
    try:
        destroy_docker_compose()
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
