
import pickle
import os
import click
import pkgutil
import importlib.resources

def _get_folder_file_structure_of_templates():
    #TODO Not able to find a way to read files strucute and folder structure
    # from within the packages. Hence creating a pickle that stores the
    # folder structure in a dictionary

    dir_file_names_dict = pickle.load(
    importlib.resources.open_binary("viperD", "dir_file_names.pkl"))
    return dir_file_names_dict['dirs'], dir_file_names_dict['files']

def _create_folders(path_app, dirs):

    # create main directory for the application
    try:
        os.mkdir(path_app)
    except:
        click.echo(f"Can not make directory with the name {app_name}")
        click.echo(f"Either directory {app_name} exists \
            or do not have required permissions to create directory!")
        return
    # create sub directories for the application
    for dir in dirs:
        path_new_folder = os.path.join(path_app, dir)
        os.mkdir(path_new_folder)

def _read_files(file_rel_path):
    data = pkgutil.get_data(__name__, f'templates/{file_rel_path}')
    data = data.replace(b"package_name", b"test package")
    return data

def _create_files(app_name, path_app, files):
    for file_rel_path in files:
        data = _read_files(file_rel_path)
        data = data.replace(b'__viper__', app_name.encode('ascii'))
        file_path = os.path.join(path_app, file_rel_path)
        with open(file_path, 'wb') as f:
            f.write(data)

if __name__ == "__main__":
    # List down all the directories/sub directories and files present
    # in template folder and save them in a pkl object
    base_path = os.path.dirname(__file__)
    base_path_template = os.path.join(base_path, "templates")
    dir_list = []
    file_list = []

    for dir_, _, files in os.walk(base_path_template):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, base_path_template)
            if not ((rel_dir in dir_list) | ('.' in rel_dir.__str__())):
                dir_list.append(rel_dir)
                # print(f"'{rel_dir}'")
            rel_file = os.path.join(rel_dir, file_name)
            if not (( rel_file in file_list) | ('.DS_Store' in rel_file.__str__()) | ('__init__' in rel_file.__str__()) ):
                file_list.append(rel_file)
                print(f"'{rel_file}'")
    dir_file_names_dict = {}
    dir_file_names_dict['dirs']=dir_list
    dir_file_names_dict['files']=file_list

    dir_file_names_ = os.path.join(base_path, 'dir_file_names.pkl')
    with open(dir_file_names_, 'wb') as f:
        pickle.dump(dir_file_names_dict, f)
