import os

def is_subdirectory(wd, d):
    if d == ".":
        return True
    
    working_directory = os.path.realpath(wd)
    directory = os.path.realpath(os.path.join(wd, d))
    working_directory = os.path.join(working_directory, '')
    return os.path.commonprefix([working_directory, directory]) == working_directory


def get_files_info(working_directory, directory="."):
    
    path = os.path.join(working_directory, directory)
    if not os.path.isdir(path):
        return f'    Error: "{directory}" is not a directory'
    
    base = ''
    if is_subdirectory(wd=working_directory, d=directory):
        if directory == ".":
            base = "current"
        else:
            base = f"'{directory}'"
            
        all_things = os.listdir(path)
        info = [f" - {thing}: file_size={os.path.getsize(os.path.join(path, thing))} bytes, is_dir={os.path.isdir(os.path.join(path, thing))}" for thing in all_things]
        return f"Result for {base} directory:\n" + '\n'.join(info)
        #for thing in all_things:
        #    thing_path = os.path.join(path, thing)
        #    print(f" - {thing}: file_size={os.path.getsize(thing_path)} bytes, is_dir={os.path.isdir(thing_path)}")
    
    return f"Result for {directory} directory:\n" + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'









