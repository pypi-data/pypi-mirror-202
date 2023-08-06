import click
import pkg_resources

# cli
@click.group()
def cli(): pass

# create cmds
@click.command()
def version():
    "Show openart version"
    click.echo(pkg_resources.get_distribution("openart").version)

# add cmds
cli.add_command(version)

# check and run
if __name__ == "__main__":
    try:
        cli()
    except Exception as err: raise err