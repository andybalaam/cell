import os


def all_examples():
    return (
        "examples/" + filename
        for filename in os.listdir("examples")
        if filename.endswith(".cell")
    )
