import os


def all_examples(file_ext=".cell"):
    return (
        "examples/" + filename
        for filename in os.listdir("examples")
        if filename.endswith(file_ext)
    )


def all_sessions():
    return all_examples(".cellsession")
