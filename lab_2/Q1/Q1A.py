import os

if __name__ == "__main__":
    py_files = [f for f in os.listdir() if f[-3:] == ".py"]
    with open("Q1A.out", "w") as f:
        f.write("\n".join(py_files))
    
    for f in py_files:
        print(f)

