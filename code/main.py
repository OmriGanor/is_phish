"""
Author: Omri Ganor
Purpose: launches the is_phish engine with given parameters.
"""
import engine
import input.user
import input.config
import os.path
import logging


def set_logger(log_path):
    directory_name = os.path.dirname(log_path)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def main():
    args = input.user.parse_args()
    if args.l:
        logger = set_logger(args.l)
    else:
        logger = set_logger(os.path.join(os.path.dirname(os.path.realpath(__file__)), r"Logs\log.log"))
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"config\config.json")
    logger.debug("Attempting to load config from {0}".format(config_path))
    config = input.config.load_config(config_path)
    logger.debug("Running engine with {0} {1} {2}".format(args.o, args.t, config))
    report = engine.run_engine(args.o, args.t, config)
    logger.debug("Engine returned report: {0}".format(report))
    print(report)


if __name__ == "__main__":
    main()