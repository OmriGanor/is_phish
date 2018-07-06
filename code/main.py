"""
Author: Omri Ganor
Purpose: launches the is_phish engine with given parameters.
"""

import engine
import user_input


def main():
    args = user_input.parse_args()
    report = engine.run_engine(args.o, args.t)


if __name__ == "__main__":
    main()