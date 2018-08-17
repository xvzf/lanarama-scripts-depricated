import click
from helper import get_server, perror

def deploy_cmd(rcon_password, ip, cpu_offset, cpuset):
    """
    :param rcon: RCON password
    :param ip: IP
    """
    return f"docker run " + \
           f"-e CSGO_SERVERNAME=\"lanarama-gameserver-{ip}\" " + \
           "-e CSGO_GAMEMODE=\"competitive\" " + \
           f"-e CSGO_RCON_PASSWORD=\"{rcon_password}\" " + \
           "--network=\"servernetwork\" " + \
           f"--cpuset-cpus=\"{','.join([str(i + cpu_offset) for i in range(cpuset)])}\" " + \
           f"--ip=\"{ip}\" " + \
           "--restart unless-stopped " + \
           "-d 192.168.10.13:5000/lanarama/csgo-128tick-server"

@click.command()
@click.option("--servername",
        help="Servername")
@click.option("--ip-start",
        help="Start ip for the servers")
@click.option("--server-count", default=12,
        help="Number of CSGO server to spawn")
@click.option("--cpuset-count", default=2,
        help="Number of cores for the CSGO server")
@click.option("--ip-offset", default=0,
        help="Offset of the servername (lanarama-0...lanarama-XX)")
@click.option("--cpu-offset", default=0,
        help="Offset of the servername (lanarama-0...lanarama-XX)")
@click.option("--rcon-password", default="NopeNotThisOne",
        help="RCON password for the server(s)")
def main(
        servername,
        ip_start,
        rcon_password,
        server_count,
        cpuset_count,
        cpu_offset,
        ip_offset):

    if not servername or not ip_start:
        return

    with get_server(servername) as server:
        num_cpu = int(server.run("nproc").stdout)

        # Check CPU count
        if cpuset_count * server_count > num_cpu:
            perror("Too many servers")
            return

        baseip = ".".join(ip_start.split(".")[:-1])
        start = int(ip_start.split(".")[-1])

        for sub in range(server_count):
            server.run(deploy_cmd(
                rcon_password,
                f"{baseip}.{sub + start}",
                cpu_offset + sub * cpuset_count,
                cpuset_count
                ))


if __name__ == "__main__":
    main()
