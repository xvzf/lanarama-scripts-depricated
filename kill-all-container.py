import click
from helper import get_server, perror

@click.command()
@click.option("--servername")
def main(servername):
    if servername:
        with get_server(servername) as server:
            server.run(" docker kill $(docker ps -q)")
    else:
        perror("servername not defined")

if __name__ == "__main__":
    main()
