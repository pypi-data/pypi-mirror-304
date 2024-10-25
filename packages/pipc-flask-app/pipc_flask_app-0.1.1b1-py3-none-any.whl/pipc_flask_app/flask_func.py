from pipc_flask_app.flask_constants import *
import os
import time
from pipc_flask_app.images import *


# CREATE TEMPLATE =========================================================

def template(directory, proj_name, path = os.path.join('app', 'templates')):
    # TEMPLATE
    os.makedirs(os.path.join(directory, path))
    with open(os.path.join(directory, path, 'layout.html'), 'w') as f:
        f.write(app_template_layout)
        print(f"{tic}{proj_name}/{path}/layout.html created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, path, 'home.html'), 'w') as f:
        f.write(app_template_home)
        print(f"{tic}{proj_name}/{path}/home.html created successfully.{RESET}")
        time.sleep(0.5)


# CREATE APP ==============================================================
def app(directory, proj_name,path = "app"):

    os.makedirs(os.path.join(directory, path), exist_ok=True)

    with open(os.path.join(directory, path, '__init__.py'), 'w') as f:
        f.write(app_init)
        print(f"{tic}{proj_name}/app/__init__.py created successfully.{RESET}")
        time.sleep(0.5)
    
    with open(os.path.join(directory, path, 'routes.py'), 'w') as f:
        f.write(app_routes)
        print(f"{tic}{proj_name}/app/routes.py created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, path, 'forms.py'), 'w') as f:
        f.write(app_forms) 
        print(f"{tic}{proj_name}/app/forms.py created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, path, 'models.py'), 'w') as f:
        f.write(app_models)
        print(f"{tic}{proj_name}/{path}/models.py created successfully.{RESET}")
        time.sleep(0.5)



# CREATE APP STATIC ======================================================
def app_static(directory, proj_name, path= os.path.join('app', 'static')):
    # STATIC
    os.makedirs(os.path.join(directory, path))

    os.makedirs(os.path.join(directory, path, 'css'))
    with open(os.path.join(directory, path, 'css', 'style.css'), 'w') as f:
        f.write(app_static_css)
        print(f"{tic}{proj_name}/{path}/css/style.css created successfully.{RESET}")
        time.sleep(0.5)

    os.makedirs(os.path.join(directory, path, 'js'))
    with open(os.path.join(directory, path, 'js', 'script.js'), 'w') as f:
        f.write(app_static_js)
        print(f"{tic}{proj_name}/{path}/js/script.js created successfully.{RESET}")
        time.sleep(0.5)

    os.makedirs(os.path.join(directory, path, 'images'))
    with open(os.path.join(directory, path, 'images', 'logoDark.svg'), 'w') as f:
        f.write(pipcreator_logo)
    with open(os.path.join(directory, path, 'images', 'flask.svg'), 'w') as f:
        f.write(flask_logo)
    print(f"{tic}{proj_name}/{path}/images/ created successfully.{RESET}")
    time.sleep(0.5)



# FLASK MAIN DIRECTORY =========================================================
def flask_directory(directory, proj_name):
    # MIGRATIONS
    os.makedirs(os.path.join(directory, 'migrations'))
    print(f"{tic}{proj_name}/migrations/ created successfully.{RESET}")
    time.sleep(0.5)

    # INSTANCE
    os.makedirs(os.path.join(directory, 'instance'))
    with open(os.path.join(directory, 'instance', 'config.py'), 'w') as f:
        f.write(instance_config)
        print(f"{tic}{proj_name}/instance/config.py created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, 'config.py'), 'w') as f:
        f.write(config)
        print(f"{tic}{proj_name}/config.py created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, 'run.py'), 'w') as f:
        f.write(run)
        print(f"{tic}{proj_name}/run.py created successfully.{RESET}")
        time.sleep(0.5)

    with open(os.path.join(directory, '.flaskenv'), 'w') as f:
        f.write(flask_env)
        print(f"{tic}{proj_name}/.flaskenv created successfully.{RESET}")
        time.sleep(0.5)



# BASIC APP ============================================================== 

def basic_app(directory, proj_name):
    with open(os.path.join(directory, 'app.py'), 'w') as f:
        f.write(basic_flask_app)
        print(f"{tic}{proj_name}/app.py created successfully.{RESET}")
        time.sleep(0.5)


# REACT FRAMEWORK ========================================================
from textPlay import backend_exec
from pipcreator.constants import error_msg

def app_react(directory, proj_name):
    if directory == os.getcwd():
        path = os.path.join('client')
    else:
        path = os.path.join(proj_name,'client')
    try:
        backend_exec(f"npx create-react-app@latest {path}")
        print(f"{tic}{proj_name}/client created successfully.{RESET}")
    except Exception as e:
        print(error_msg," ",e)

def app_nextjs(directory, proj_name):
    if directory == os.getcwd():
        path = os.path.join('client')
    else:
        path = os.path.join(proj_name,'client')

    try:
        backend_exec(f"npx create-next-app@latest {path}")
        print(f"{tic}{proj_name}/client created successfully.{RESET}")
    except Exception as e:
        print(error_msg," ",e)

def app_vite(directory, proj_name):
    if directory == os.getcwd():
        path = os.path.join('client')
    else:
        path = os.path.join(directory,'client')

    try:
        backend_exec(f"npx create-vite@latest {path}")
        print(f"{tic}{proj_name}/client/vite created successfully.{RESET}")
    except Exception as e:
        print(error_msg," ",e)

def other_framework(directory, proj_name, script):
    
    print("Make sure your script is in the client folder")
    try:
        if script:
            backend_exec(script)
            print(f"{tic}{proj_name}/client created successfully.{RESET}")
        else:
            print(error_msg," No script provided")

    except Exception as e:
        print(error_msg," ",e)