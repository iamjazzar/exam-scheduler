import argparse

from graphbuilder import GraphBuilder
from graphpainter import GraphPainter


def parse_arguments():
    """
    Command line arguments parser.
    """
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add an argument
    parser.add_argument(
        "--slots",
        "-s",
        type=int,
        required=False,
        default=5,
        help=(
            "Number of exam time slots in a given day (determined by the "
            "registrar and/or the faculty)"
        ),
    )

    parser.add_argument(
        "--days",
        "-y",
        type=int,
        required=False,
        default=20,
        help=(
            "The number of concurrent exam sessions. Bounded by available "
            "halls, and the availability of faculty to conduct the exams."
        ),
    )

    parser.add_argument(
        "--fairness",
        "-f",
        type=int,
        required=False,
        default=2,
        help=(
            "An Exam schedule should avoid conflicts, in the sense that no two or more "
            "exams (this value) for the same student are scheduled at the same time."
        ),
    )

    parser.add_argument(
        "--schedule",
        "-d",
        type=str,
        required=True,
        help="The path of the file for students' enrollments.",
    )

    parser.add_argument(
        "--courses",
        "-c",
        type=str,
        required=True,
        help="The path of the file that hosts courses' data.",
    )

    return parser.parse_args()


def main():
    # Remove 1st argument from the list of command line arguments
    args = parse_arguments()

    graph = GraphBuilder(args.slots, args.schedule, args.courses).build()

    painter = GraphPainter(graph, args.days, args.slots, fairness=args.fairness)
    painter.paint()


if __name__ == "__main__":
    exit(main())
