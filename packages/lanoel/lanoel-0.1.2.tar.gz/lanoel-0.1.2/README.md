# La Noel (Secret Santa)

A Secret Santa generator for groups of people.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

To install lanoel, run the following command:

```bash
pip install lanoel
```

## Usage

To use lanoel, simply run the following command:

```bash
$lanoel --help
usage: lanoel [-h] [-p PARTICIPANT] [-f FILE]

options:
  -h, --help            show this help message and exit
  -p PARTICIPANT, --participant PARTICIPANT
                        The name of participants and optionally category separated by a semicolon. If category is not
                        provided, the participant will be in the default category. ex: Oliver,Tuner
  -f FILE, --file FILE  The path of the csv file. The file should be in the format 'name;category'.
```

## Features

- Generate Secret Santa pairs for groups of people
- Support for categories to ensure participants are not paired with someone from the same category
- Easy to use command-line interface
