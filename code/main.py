"""
Author: Omri Ganor
Purpose: launches the is_phish engine with given parameters.
"""

import engine
import input.user
import input.config
import os.path


def main():
    args = input.user.parse_args()
    config = input.config.load_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), r"config\config.json"))
    report = engine.run_engine(args.o, args.t, config)
    print(report)


if __name__ == "__main__":
    main()