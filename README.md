# trello-agent-script
A command-line interface for pushing JSON-defined cards into specific Trello lists.   Intended for fast task management without using the web UI.


## Installation

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
python3 main.py --list <list_name> --file <json_file>

## Examples
push cards to today's list:
```bash
python3 main.py --list today --file example.json
```bash
Push backlog into planning:
```bash
python3 main.py --list planning --file backlog.json
```bash
Archive finished tasks:
```bash
python3 main.py --list done --file archive.json
```
