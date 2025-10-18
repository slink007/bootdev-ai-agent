# from functions.helpers import get_files_info
# from functions.get_files_info import get_files_info
# from functions.helpers import get_file_content
from functions.helpers import Helpers

def read_files_tests():
    print(Helpers.get_files_info("calculator", "."))
    print("")
    # print(get_files_info("calculator", "pkg"))
    # print("")
    print(Helpers.get_files_info("calculator", "/bin"))
    print("")
    print(Helpers.get_files_info("calculator", "../"))

def read_file_content_tests():
    print(Helpers.get_file_content("calculator", "main.py"))
    print("")
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print("")
    # print(get_file_content("calculator", "lorem.txt"))
    # print("")
    print(Helpers.get_file_content("calculator", "/bin/cat"))
    print("")
    print(Helpers.get_file_content("calculator", "pkg/does_not_exist.py"))

def write_file_content_tests():
    print(Helpers.write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("")
    print(Helpers.write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("")
    print(Helpers.write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    # read_files_tests()
    # print("\n")
    # read_file_content_tests()
    # print("\n")
    write_file_content_tests()
