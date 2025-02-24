import sys

if __name__ == "__main__":
    py_file = sys.argv[1]
    with open(py_file, "r") as f:
        file_contents = f.read()

    payload = r"""
    import sys
    with open('Q1B.out', 'a') as f:
        f.write(' '.join(sys.argv) + '\n')"""
    script_str = 'if __name__ == "__main__":'
    
    if (script_str in file_contents) and (payload not in file_contents):
        with open(py_file, "a") as f:
            f.write(payload + "\n")

