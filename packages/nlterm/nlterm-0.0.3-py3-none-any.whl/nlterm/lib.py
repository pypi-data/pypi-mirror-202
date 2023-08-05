from typing import List
import openai
import os

def current_shell_name():
    """
    Get the name of the current shell running this script. (e.g. bash, zsh, fish, etc.)
    """
    shell = os.environ.get("SHELL")
    if shell is None:
        return None
    return os.path.basename(shell)

def get_ls(max_files_per_type=5):
    """
    Get a list of files in the current directory, and return a list of strings.
    Each file extension will have at most `max_files_per_type` files.
    """
    ext_map = {} # map from file extension to list of files
    for filename in os.listdir("."):
        ext = os.path.splitext(filename)[1]
        ext_map.setdefault(ext, []).append(filename)
    ls = []
    for ext, files in ext_map.items():
        if len(files) > max_files_per_type:
            files = files[:max_files_per_type]
        ls.extend(files)
    return ls

def get_os():
    """
    Get the OS name.
    """
    import platform
    return platform.system()


def get_username():
    """
    Get the username.
    """
    return os.environ.get("USER")

def get_prompt(current_shell: str, ls: List[str], instruction: str):
    ls_str = "\n".join(ls)
    return [
        {"role": "system", "content": "You are a helpful assistant that translates natural language instructions into terminal commands. You only output commands and nothing else."},
        {"role": "user", "content": f"""Given the environment and instruction below, output code and answer very concisely. Wrap your code in triple backticks (```) and put it on a new line. Example:
```
echo "Hello World"
```
You can output multiple commands.

Current LS:
{ls_str}

Current Shell: {current_shell}
Current OS: {get_os()}
Current Username: {get_username()}

Natural Language Command: {instruction}
Answer:"""}]

def extract_command_from_completion(completion: str):
    """
    The command is always wrapped by the line "```ANYTHING" and "```". This function extracts the command from the completion.
    There may be multiple commands.
    """
    lines = completion.splitlines()
    commands = []
    commands_line_numbers = []
    in_command = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_command = not in_command
        else:
            if in_command:
                commands.append(line)
                commands_line_numbers.append(i)

    return commands, commands_line_numbers

def print_completion_with_color(completion: str, commands_line_numbers: List[int]):
    """
    Print completion with color. The commands are printed in green.
    """
    lines = completion.splitlines()
    for i, line in enumerate(lines):
        if i in commands_line_numbers:
            print("\033[92m" + line + "\033[0m")
        else:
            print(line)


def get_completion(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )


def main_func():
    current_shell = current_shell_name()
    ls = get_ls()
    # Get instruction interactively
    try:
        instruction = input("Instruction: ")
        prompt = get_prompt(current_shell, ls, instruction)
        completion = get_completion(prompt)
        completion = completion["choices"][0]["message"]["content"]
        commands, commands_line_numbers = extract_command_from_completion(completion)
        print_completion_with_color(completion, commands_line_numbers)

        # ask for execution
        execute = input("Execute? (y/n): ")
        if execute == "y":
            for command in commands:
                os.system(command)
    except KeyboardInterrupt:
        print()
        return

if __name__ == "__main__":
    main_func()