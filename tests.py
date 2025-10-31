from functions.get_files_info import get_files_info
from functions.write_file_content import write_file_content
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

def read_files_tests():
    print(get_files_info("calculator", "."))
    print("")
    print(get_files_info("calculator", "pkg"))
    print("")
    print(get_files_info("calculator", "/bin"))
    print("")
    print(get_files_info("calculator", "../"))

def read_file_content_tests():
    print(get_file_content("calculator", "main.py"))
    print("")
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print("")
    # print(get_file_content("calculator", "lorem.txt"))
    # print("")
    print(get_file_content("calculator", "/bin/cat"))
    print("")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

def write_file_content_tests():
    print(write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("")
    print(write_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("")
    print(write_file_content("calculator", "/tmp/temp.txt", "this should not be allowed"))

def execute_code_tests():
    print(run_python_file("calculator", "main.py"))
    print("")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("")
    print(run_python_file("calculator", "../main.py"))
    print("")
    print(run_python_file("calculator", "nonexistent.py"))
    print("")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    # read_files_tests()
    # print("\n")
    # read_file_content_tests()
    # print("\n")
    # write_file_content_tests()
    execute_code_tests()
