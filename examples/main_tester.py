from rich.console import Console


def main():
    # clear scren, print in green color the project name and in blue italic the version
    # use rich for printing
    console = Console()
    console.clear()
    console.print("[bold green]Some ASM[/]", end=" ")
    console.print("[italic= blue]v0.0.1[/]")


if __name__ == "__main__":
    main()
