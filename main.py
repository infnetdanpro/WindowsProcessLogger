import click


@click.command()
@click.option("--sleep_time", default=0.5, help="Period of checking processes")
def run_logger(sleep_time):
    from process_logger import main

    main(sleep_time)


if __name__ == "__main__":
    run_logger()
