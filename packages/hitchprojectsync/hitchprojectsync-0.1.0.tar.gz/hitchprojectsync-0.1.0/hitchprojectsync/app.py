from strictyaml import load, Map, Str
from pathlib import Path
from sys import exit
import shutil
import click
import os


@click.command()
@click.argument("command")
def main(command):
    """Main command runner."""
    
    cwd = Path(os.getcwd())
    config_path = cwd / ".hitchprojectsync"
    
    if command == "updateproject":
        if config_path.exists():
            config_data = load(config_path.read_text(), Map({"source": Str()})).data
            base_source = config_data["source"]
            
            base_path = cwd / base_source
            
            if base_path.exists():
                for filepath in base_path.rglob("*"):
                    relative_path = filepath.relative_to(base_path)
                    print("Copying {}".format(relative_path))
                    shutil.copy(filepath, cwd / relative_path)
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()
            #click.echo("No .hitchprojectsync found in this folder", err=True)
            #sys.exit(1)
    else:
        raise NotImplementedError("command not found")
