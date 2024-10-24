import os


def returnCentered(message):
    message_lines = [line for line in message.split("\n") if line.strip() != ""]
    message_line_amount = len(message_lines)
    chars_per_line = max(len(line) for line in message_lines)
    col, row = os.get_terminal_size()
    centered_message_lines = [line.center(col) for line in message_lines]
    top_padding = (row - message_line_amount) // 2
    bottom_padding = row - message_line_amount - top_padding
    return (
        "\n" * top_padding + "\n".join(centered_message_lines) + "\n" * bottom_padding
    )


def printCentered(message):
    message_lines = [line for line in message.split("\n") if line.strip() != ""]
    message_line_amount = len(message_lines)
    chars_per_line = max(len(line) for line in message_lines)
    col, row = os.get_terminal_size()
    centered_message_lines = [line.center(col) for line in message_lines]
    top_padding = (row - message_line_amount) // 2
    bottom_padding = row - message_line_amount - top_padding
    os.system("clear")
    print(
        "\n" * top_padding + "\n".join(centered_message_lines) + "\n" * bottom_padding
    )
