import logging


def setup_logger():
    logging.basicConfig(
        filename="webhunter.log",
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
