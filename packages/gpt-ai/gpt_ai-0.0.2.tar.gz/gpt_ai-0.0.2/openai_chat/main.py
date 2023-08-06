import click
from openai_chat.chat import Chat
import os
import re
import openai
import json
from datetime import datetime
from glob import glob

DATE_FMT = "%I.%M.%S %p %A %b %d %Y"
PATH_NAME = ".openai_chat_history"


@click.command()
@click.option("--resume", "-r", is_flag=True, help="Continue a previous chat")
@click.option("--jump", "-j", help="Jump to a previous chat. Pass positive integer to jump to nth most recent chat.", default=None)
def main(resume, jump):
    key = get_key()
    if not key:
        quit()
    openai.api_key = key

    path = os.path.join(os.path.expanduser("~"), PATH_NAME)
    if not os.path.exists(path):
        os.mkdir(path)

    curr_chat_file = datetime.now().strftime(DATE_FMT) + ".json"
    curr_chat_file = os.path.join(path, curr_chat_file)
    last_chat_file = None

    if resume or jump is not None:
        last_chat_file = get_name_of_historical_chat(path, jump)
        if not last_chat_file:
            print("No previous chat sessions found")
            quit()
        chat = Chat(last_chat_file)
        chat.display_history()
        print(f"(Resumed from {prettify_date(get_fname(last_chat_file))})")
        chat.display_sep('user')

    else:
        chat = Chat()
        chat.display_sep("user")

    previous_overwritten = False
    while True:
        user_input = input("")
        print()

        if user_input.lower() == "q":
            break

        chat.save(curr_chat_file)
        if last_chat_file and not previous_overwritten:
            os.remove(last_chat_file)
            previous_overwritten = True

        response = chat.send(user_input)
        chat.save(curr_chat_file)
        chat.display_message(response)

    chat.save(curr_chat_file)
    if last_chat_file and not previous_overwritten:
        os.remove(last_chat_file)


def validate_date(s) -> bool:
    try:
        datetime.strptime(s, DATE_FMT)
        return True
    except ValueError:
        return False

def get_fname(path) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def prettify_date(s) -> str:
    s = s.replace(".", ":")
    s = re.sub(r"(\d\d:\d\d):\d\d", r"\1", s)
    s = re.sub(r" \d\d\d\d$", "", s)
    s = re.sub(r" AM ", "am ", s)
    s = re.sub(r" PM ", "pm ", s)
    s = re.sub(r"^0", "", s)
    return s

def get_name_of_historical_chat(path, jump_index=None) -> str | None:
    if jump_index is None:
        jump_index = 0

    jump_index = int(jump_index)

    if jump_index > 0:
        index = - (jump_index + 1)
    else:
        index = jump_index

    # Filter the files by the desired format
    json_files = [
        f
        for f in glob(os.path.join(path, "*.json"))
        if validate_date(get_fname(f))
    ]
    if not json_files:
        return None

    # Find the most recent file by timestamp
    sorted_history = list(sorted(
        json_files,
        key=lambda f: datetime.strptime(
            get_fname(f), DATE_FMT
        ),
    ))
    if len(sorted_history) < abs(index):
        print(f"Jump index '{jump_index}' out of bounds. Only {len(sorted_history)} chats available. Defaulting to earliest chat.")
        return sorted_history[1]
    return sorted_history[index]


def get_key() -> str | None:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        bash_file = os.path.join(os.path.expanduser("~"), ".bashrc")
        print(
            "Please set the OPENAI_API_KEY environment variable.\n"
            "You can get an API key from https://beta.openai.com/account/api-keys.\n"
            "You can set the environment variable by running the following command\n"
            "in your terminal:\n"
            "   export OPENAI_API_KEY='XXXXXX'\n"
            "This will only set it temporarily. To set it permanently, add the command above\n"
            "to the end of your shell's startup script (e.g. ~/.bashrc or ~/.zshrc)."
            "To see which kind of shell you are using, run the following command:\n"
            "   echo $SHELL\n"
            f"For example, if you're using bash, look for the file, '{bash_file}'.\n"
            "If it doesn't exist, create it. Then add the above 'export ...' command\n"
            "to the file."
        )
        return None
    return key




