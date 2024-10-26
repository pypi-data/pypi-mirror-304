from argparse import ArgumentParser
from lanoel.lanoel import secret_santa, Participant, Pair
import pathlib
import sys

DEFAULT_CATEGORY = "default"
DEFAULT_SEPARATOR = ","
DEFAULT_CSV_SEPARATOR = ";"


def parse_participant(participant_str: str, separator: str) -> Participant:
    """Parse a participant string and return a Participant object."""

    if separator not in participant_str:
        return Participant(participant_str.strip(), DEFAULT_CATEGORY)

    participant_args = participant_str.split(separator)
    if len(participant_args) != 2:
        sys.exit(f"Invalid participant string: {participant_str}")
    name, category = participant_args

    return Participant(name.strip(), category.strip())


def output_participants(participants: list[Participant]):
    print("-----Participants-----")
    for participant in participants:
        print(f"{participant.name} ({participant.category})")
    print()


def output_pairs(result: list[Pair]):
    print("-----Pairs-----")
    for pair in result:
        print(f"{pair.giver} est le secret santa de {pair.receiver}.")
    print()


def entrypoint():
    parser = ArgumentParser()

    parser.add_argument(
        "-p",
        "--participant",
        type=str,
        action="append",
        help=f"The name of participants and optionally category separated by a semicolon. If category is not provided, the participant will be in the default category. ex: Oliver{DEFAULT_SEPARATOR}Tuner",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        help=f"The path of the csv file. The file should be in the format 'name{DEFAULT_CSV_SEPARATOR}category'.",
    )

    args = parser.parse_args()
    print(args)

    participants = []
    if args.participant:
        participants.extend(
            [parse_participant(p, DEFAULT_SEPARATOR) for p in args.participant]
        )

    if args.file:
        with open(args.file, "r", encoding="utf-8") as participants_file:
            participants_lines = participants_file.readlines()
            participants.extend(
                [
                    parse_participant(p, DEFAULT_CSV_SEPARATOR)
                    for p in participants_lines
                ]
            )

    if len(participants) <= 1:
        sys.exit("The number of participants must be greater than 1.")

    output_participants(participants)

    result = secret_santa(participants)

    if len(result) != len(participants):
        sys.exit("The number of participants does not match the number of pairs.")

    output_pairs(result)
