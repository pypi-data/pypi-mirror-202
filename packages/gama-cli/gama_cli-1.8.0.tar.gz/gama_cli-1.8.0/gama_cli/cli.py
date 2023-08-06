import gama_cli.groups.attach as attach
import gama_cli.groups.docker as docker
import gama_cli.groups.git as git
import gama_cli.groups.gs as gs
import gama_cli.groups.misc as misc
import gama_cli.groups.sim as sim
import gama_cli.groups.vessel as vessel
import gama_cli.groups.setup as setup
from gama_cli.helpers import is_dev_version, get_gama_version
from gama_cli.banner import get_banner
from gama_cli.config.gama_gs import GamaGsConfig
from gama_cli.config.gama_vessel import GamaVesselConfig
import click
import os
from dc_schema import get_schema
import json
from pathlib import Path


def generate_schemas():
    """Generates the schemas for the config files"""
    SCHEMAS_PATH = Path(os.path.dirname(__file__)) / "schemas"
    with open(SCHEMAS_PATH / "gama_vessel.schema.json", "w") as f:
        json.dump(get_schema(GamaVesselConfig), f, indent=2)
    with open(SCHEMAS_PATH / "gama_gs.schema.json", "w") as f:
        json.dump(get_schema(GamaGsConfig), f, indent=2)


def cli():
    dev_mode = is_dev_version()
    version = get_gama_version()
    mode = "Developer" if dev_mode else "User"
    banner = get_banner(mode, version)

    if dev_mode:
        generate_schemas()

    os.environ["GAMA_CLI_DEV_MODE"] = "true" if dev_mode else "false"

    @click.group(help=banner)
    def gama_cli():
        pass

    gama_cli.add_command(misc.authenticate)
    gama_cli.add_command(misc.upgrade)

    gama_cli.add_command(vessel.vessel)
    vessel.vessel.add_command(vessel.up)
    vessel.vessel.add_command(vessel.down)
    vessel.vessel.add_command(vessel.configure)
    vessel.vessel.add_command(vessel.install)

    gama_cli.add_command(gs.gs)
    gs.gs.add_command(gs.up)
    gs.gs.add_command(gs.down)
    gs.gs.add_command(gs.configure)
    gs.gs.add_command(gs.install)

    if dev_mode:
        gama_cli.add_command(misc.test)
        gama_cli.add_command(misc.test_e2e)
        gama_cli.add_command(misc.lint)

        gama_cli.add_command(attach.attach)
        attach.attach.add_command(attach.vessel)
        attach.attach.add_command(attach.ui)
        attach.attach.add_command(attach.gs)

        gama_cli.add_command(docker.docker)
        docker.docker.add_command(docker.clearlogs)

        gama_cli.add_command(git.git)
        git.git.add_command(git.pull)

        gama_cli.add_command(sim.sim)
        sim.sim.add_command(sim.build)
        sim.sim.add_command(sim.up)
        sim.sim.add_command(sim.down)
        sim.sim.add_command(sim.base_ue)

        gama_cli.add_command(setup.setup)
        setup.setup.add_command(setup.secrets)
        setup.setup.add_command(setup.env)

        vessel.vessel.add_command(vessel.build)
        vessel.vessel.add_command(vessel.bake)
        vessel.vessel.add_command(vessel.test)
        vessel.vessel.add_command(vessel.type_generate)
        vessel.vessel.add_command(vessel.test_ui)
        vessel.vessel.add_command(vessel.test_e2e)
        vessel.vessel.add_command(vessel.test_ros)

        gs.gs.add_command(gs.build)
        gs.gs.add_command(gs.bake)
        gs.gs.add_command(gs.test)

    gama_cli()


if __name__ == "__main__":
    cli()
