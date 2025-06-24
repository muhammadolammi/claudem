import os
import os.path as path

def get_files_info(working_directory, directory=None):
    try:
        main_dir = "./"
        working_directory = path.abspath(path.expanduser(path.join(main_dir, working_directory)))
        directory = path.abspath(path.expanduser(path.join(working_directory, directory)))
        
        if not path.commonpath([working_directory]) == path.commonpath([working_directory, directory]):
            # print(f'Error: "{directory}" is outside the working directory')
            return f'Error: "{directory}" is outside the working directory'

        # if not path.exists(directory):
        #     # print(f'Error: "{directory}" does not exist')
        #     return f'Error: "{directory}" does not exist'

        if not path.isdir(directory):
            # print(f'Error: "{directory}" is not a directory')
            return f'Error: "{directory}" is not a directory'

        file_contents = os.listdir(directory)
        files_infos = {}
        for content in file_contents:
            content_full_path = path.join(directory, content)
            file_size = path.getsize(content_full_path)
            is_dir = path.isdir(content_full_path)
            files_infos[content] = {
                "file_size": file_size,
                "is_dir": is_dir,
            }

        return_str = "\n"
        for content in file_contents:
            result = f"{content}: file_size={files_infos[content]['file_size']} bytes, is_dir={files_infos[content]['is_dir']}\n"
            return_str += result
        return return_str

    except Exception as e:
        return f"ERROR: {e}"


