# trello-agent-script
A command-line interface for pushing JSON-defined cards into specific Trello lists.   Intended for fast task management without using the web UI.


## Installation

### Option 1: Install as a package (Recommended)

Clone the repository and install as a development package:

```bash
git clone <repo_url>
cd <repo_name>
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Now you can use the command from anywhere:
```bash
trello-task-maker --list today --file test.json
```

### Option 2: Run directly

Clone the repository and create a Python virtual environment:

```bash
git clone <repo_url>
cd <repo_name>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run with local changes:
```bash
python3 main.py --list today --file test.json
```

## Usage
The CLI accepts two required arguments:
--list: target Trello list
--file: path to a JSON file with card definitions

## Supported lists
--list must be one of:
  - default: planning list
  - today: Today's tasks
  - weekly: Weekly backlog
  - progress: Tasks in progress
  - done: Completed tasks

## Command format

### When installed as package:
```bash
trello-task-maker --list <list_name> --file <json_file>
```

### When running directly:
```bash
python3 main.py --list <list_name> --file <json_file>
```

## Examples

Push cards to today's list:
```bash
trello-task-maker --list today --file example.json
```

Push backlog into planning:
```bash
trello-task-maker --list planning --file backlog.json
```

Archive finished tasks:
```bash
trello-task-maker --list done --file archive.json
```
