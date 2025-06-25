import os.path as path
import os

def isinsidewrkDIR(working_directory, file_path):
    if  path.commonpath([working_directory]) == path.commonpath([working_directory, file_path]):
            # print(f'Error: "{directory}" is outside the working directory')
            return True 
    return False


def resolve_dir(working_directory, directory):
        main_dir = "./"
        working_directory = path.abspath(path.expanduser(path.join(main_dir, working_directory)))
        if not os.path.isabs(directory):
                directory = path.abspath(path.expanduser(path.join(working_directory, directory)))

        return working_directory, directory 
