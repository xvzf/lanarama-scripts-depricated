from helper import get_server

def main():
    with get_server("ebot") as ebot:
        ebot.run("service ebot start")

if __name__ == "__main__":
    main()
