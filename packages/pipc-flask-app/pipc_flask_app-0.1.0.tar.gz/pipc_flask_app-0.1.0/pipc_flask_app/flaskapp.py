import os
import sys
from string import ascii_lowercase, ascii_uppercase, digits

from pipcreator.constants import *
from pipcreator.writer import virtual_env, create_pyprojecttoml, create_readme, create_requirements, create_gitignore, create_license
from pipc_flask_app.flask_func import * 
from textPlay.colors import *
from textPlay import list_dir

from textPlay import backend_exec


def file_proj_name():
    directory = os.getcwd()
    proj_name = os.path.basename(directory)
    return proj_name

def create_flask(directory):

    folder_name = ascii_lowercase + ascii_uppercase + digits + '_./'

    if "-" in directory:
        print(f"{YELLOW}The ' - ' will be replaced as '_' in the folder name{RESET}")
        directory = directory.replace("-", "_")

    if any(char not in folder_name for char in directory):
        print(f"{RED}Invalid directory name{RESET}")
        print(f"{YELLOW}Directory name must contain only the following characters:{RESET}")
        print(f"{GREEN}A to Z   {BLUE}a-z   {MAGENTA}0-9 _ \n{RESET}")
        print(footer)
        sys.exit(1)

    if directory == '.' or directory == './':
        directory = os.getcwd()

    proj_name = os.path.basename(directory)
    print(f'Creating project @ {BLUE}{os.getcwd()}{RESET}\n')
    check_directory(directory, proj_name)



# CHECK DIRECTORY
def check_directory(directory, proj_name):

    # Check if directory exists
    if not os.path.exists(directory):
        # options()
        print(f"{YELLOW}Directory doesn't exist.{RESET}")

        dir_loop = True
        while dir_loop:
            dir_crt = input(f"Do you like to create the directory? (y/n) [{CYAN}Y{RESET}] ")
            if dir_crt.lower() == 'y' or dir_crt.lower() == '':
                os.makedirs(directory)
                print(f"{tic}Directory created successfully.{RESET}\n")
                time.sleep(0.5)
                proj_name, description, keywords, author, author_mail, licence, dependencies = options(proj_name)
                dependencies = flask_requirements + dependencies
                create_files_and_folders(directory, description, keywords, author, author_mail, proj_name, licence, dependencies)
                dir_loop = False

            elif dir_crt.lower() == 'n':
                print(f"{RED}Creating project aborted.{RESET}")
                print(f"\n{footer}")
                sys.exit(1)

            else:
                print(invalid_input)

    else:
        try:
            # Check if directory is empty
            if not os.listdir(directory):
                proj_name, description, keywords, author, author_mail, licence, dependencies = options(proj_name)
                dependencies = "Flask==2.3.2 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4 Flask-WTF==1.0.1  " + dependencies
                time.sleep(1.0)
                create_files_and_folders(directory, description, keywords, author, author_mail, proj_name, licence, dependencies)
            else:
                print(check_directory_err)
                lst =list_dir(directory)
                for i in lst:
                    print(YELLOW + i + RESET)

        except Exception as e:
            print(f"{BOLD}{RED}ERROR: {RESET}{e}")



def create_files_and_folders(
        directory, description, keywords, 
        author, author_mail, proj_name, 
        licence, dependencies
        ): 

    # TEST
    test = input(f"\nDo you want to create a test folder? (y/n) [{CYAN}Y{RESET}] ")
    if not test:
        test = "Y"

    # INIT GIT
    git = input(f"Do you want to initialize git? (y/n) [{CYAN}Y{RESET}] ")
    if not git:
        git = "Y"

    if git.lower() == 'y' or git.lower() == 'yes':
        from  textPlay import backend_exec 
        try:
            backend_exec("git init")
        except Exception as e:
            print(f"{BOLD}{RED}Error: {e}{RESET}")



    # FLASK TEMPLATES (FLASK) ================================================

    print(f"\nFlask Templates: {BOLD}{GREEN}Basic {YELLOW}Advanced (default) {BLUE}With Frameworks{RESET}")
    flask_temp = ""
    loop = True
    count = 0
    while loop:
        basic_flask = input(f"{GREEN}●{RESET} Do you want to create a Basic Flask App? (y/n) ")
        if basic_flask.lower() == 'y' or basic_flask.lower() == 'yes':
            flask_temp = "Basic"
            break
        
        advanced_flask = input(f"{YELLOW}●{RESET} Do you want to create a Advanced Flask App? (y/n) ")
        if advanced_flask.lower() == 'y' or advanced_flask.lower() == 'yes':
            flask_temp = "Advanced"
            break

        react_flask = input(f"{BLUE}●{RESET} Do you want to create a Flask App with Frameworks? (y/n) ")
        if react_flask.lower() == 'y' or react_flask.lower() == 'yes':
            flask_temp = "Frameworks"
            while True:
                print(f"\n{MAGENTA}Available frameworks:{RESET} React, Next, Vite")
                print(f"Type the name of the framework you want to use, for other frameworks type 'others'")
                framework = input(f"{BLUE}Which framework do you want to use? {RESET}").lower()
                if framework == 'others':
                    script = input("\nEnter framework comand (e.g. `npx create-next-app`): ")
                elif framework not in ["react", "next", "vite"]:
                    print(f"{RED}Invalid framework{RESET}")
                    continue
                elif framework in ["react", "next", "vite"]:
                    script = None
                break
            break

        count += 1  

        if count == 3:
            print("\nlimit reached")
            print("defaulting to advanced flask app\n")
            flask_temp = "Advanced"
            break
    
    # FLASK TEMPLATES (FLASK) ================================================



    # venv ====================================================================

    if dependencies:
        print("Creating virtual environment (venv) for safer installation...")
        if flask_temp == "Frameworks":
            venv_status = virtual_env(venv_name=os.path.join(directory, "server", "venv"))
        else:
            venv_status = virtual_env(venv_name=os.path.join(directory,"venv"))
    
    # venv ====================================================================


    # PYPROJECT TOML ===========================================================
        
    pyproj = create_pyprojecttoml(directory, description, keywords, author, author_mail, proj_name, licence, dependencies)
    time.sleep(0.5)
    setup = "pyproject.toml"

    # SETUP FILE DEFAULT
    if setup == "":
        print(f"{DIM}{YELLOW}No setup file created{RESET}\n{YELLOW}●{RESET} Defaulting to create pyproject.toml\n")
        pyproj = create_pyprojecttoml(directory, description, keywords, author, author_mail, proj_name, licence, dependencies)
        setup = "pyproject.toml"
        time.sleep(0.5)

    # PYPROJECT TOML ===========================================================


    # MAIN FILES ===============================================================

    readme = create_readme(directory, description, proj_name)
    time.sleep(0.5)
    gitignore_fh = create_gitignore(directory)
    time.sleep(0.5)
    licence = create_license(directory)
    time.sleep(0.5)
    requirements = create_requirements(directory, dependencies)
    time.sleep(0.5)

    # CREATING TEST FOLDER
    if test.lower() == 'y' or test.lower() == 'yes':
        os.makedirs(os.path.join(directory, 'test'))
        with open(os.path.join(directory, 'test', 'test_basic.py'), 'w') as f:
            f.write(test_basic)
            print(f"{tic}{proj_name}/test/test_basic.py created successfully.{RESET}")
            time.sleep(0.5)

        with open(os.path.join(directory, 'test', 'conftest.py'), 'w') as f:
            f.write(tests_conftest)
            print(f"{tic}{proj_name}/test/conftest.py created successfully.{RESET}")
            time.sleep(0.5)
        test = True

    # MAIN FILES ===============================================================



    # FLASK TEMPLATES (FLASK) ================================================

    if flask_temp == "Advanced":
        flask_app = create_app(directory, proj_name)
        time.sleep(0.5)
    elif flask_temp == "Frameworks":
        flask_app = create_framework_app(directory, proj_name,framework=framework, script=script)
        time.sleep(0.5)
    elif flask_temp == "Basic":
        flask_app = create_app_basic(directory, proj_name)
        time.sleep(0.5)

    # FLASK TEMPLATES (FLASK) ================================================

    print(files_success)
    time.sleep(0.5)
    print(flask_structure(proj_name, test, flask_temp))
    time.sleep(0.5)
    check_package_latest("pipCreator")
    if venv_status:
        print(f"\nHow to Using/Activation virtual environment\n   use: {MAGENTA}pipc guide --see on-package{RESET}")
        time.sleep(0.5)
    print(ready_to_code)
    print(f"\n\t {BRIGHT_BLUE}cd{RESET} {directory}\n")
    print(footer)



def create_app(directory, proj_name):
    try:
        app(directory, proj_name)

        template(directory,proj_name)

        app_static(directory, proj_name)

        flask_directory(directory, proj_name)


    except Exception as e:
        print(f"{error} {RESET}{e}")
    
def create_app_basic(directory, proj_name):
    try:
        basic_app(directory, proj_name)

        template(directory,proj_name,path = 'templates')

        app_static(directory, proj_name, path = 'static')



    except Exception as e:
        print(f"{error} {RESET}{e}")

def create_framework_app(directory, proj_name, framework = 'react', script = None):
    try:
        app(directory, proj_name, path="server")

        with open(os.path.join(directory, 'server', 'app.py'), 'w') as f:
            f.write(run)
            print(f"{tic}{proj_name}/server/app.py created successfully.{RESET}")
            time.sleep(0.5)

        os.makedirs(os.path.join(directory, 'client'), exist_ok=True)

        if framework == 'react' or framework == "reactjs":
            app_react(directory, proj_name)

        elif framework == "next" or framework == 'nextjs':
            app_nextjs(directory, proj_name)

        elif framework == 'vite' or framework == "vitejs":
            app_vite(directory, proj_name)
        
        else:
            if script is not None:
                other_framework(directory, proj_name,script = script)
            else:
                print(f"{error} {RESET}No script provided skipping framework creation")


        print(f"{MAGENTA}Note: {RESET}Add proxy in your client side package.json")




    except Exception as e:
        print(f"{error} {RESET}{e}")