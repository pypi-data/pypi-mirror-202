from pathlib import Path
import os.path as osp
import os
import time

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from girok.config import get_config
import girok.utils.general as general_utils
import girok.utils.auth as auth_utils
import girok.api.auth as auth_api
import girok.utils.display as display_utils

import girok.server.src.task.models as task_models
import girok.server.src.category.models as category_models
from girok.server.src.database import engine

app = typer.Typer(rich_markup_mode='rich')

cfg = get_config()
console=Console()


@app.command("mode", help="Current mode", rich_help_panel=":lock: [bold yellow1]Authentication Commands[/bold yellow1]")
def mode():
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "off":
        print("You're not logged in.")
    elif mode == "guest":
        print("[yellow]Guest mode[/yellow]")
    elif mode == "user":
        print("[yellow]User mode[/yellow]")
        

@app.command("guest", help="[yellow]Login as a guest user (using local storage)[/yellow]", rich_help_panel=":lock: [bold yellow1]Authentication Commands[/bold yellow1]")
def guest():
    if not os.path.exists(cfg.app_dir + "/database.db"):
        task_models.Base.metadata.create_all(bind=engine)
        category_models.Base.metadata.create_all(bind=engine)
    general_utils.update_json(cfg.config_path, {"mode": "guest"})
    print("[yellow]You're logged in as a guest![/yellow]")
    

@app.command("login", help="[yellow]Login[/yellow] with email and password", rich_help_panel=":lock: [bold yellow1]Authentication Commands[/bold yellow1]")
def login():
    # Check if the user holds a valid JWT (logged in)
    stored_access_token = auth_utils.get_access_token_from_json(cfg.config_path)
    if stored_access_token:
        resp = auth_api.validate_access_token(stored_access_token)
        if resp.status_code == 200:
            print("You have already logged in. Enjoy!")
            exit(0)
    
    # Log-in
    print("Please login to proceed\n")
    email = typer.prompt("Enter email address")
    password = typer.prompt("Enter password", hide_input=True)
    
    resp = auth_api.login(email, password)
    if resp.status_code == 200:
        access_token = general_utils.bytes2dict(resp.content)['access_token']
        general_utils.update_json(cfg.config_path, {"access_token": access_token, "mode": "user"})
        print("[yellow]You're logged in as a user![/yellow]")
    elif resp.status_code == 401:
        err_msg = general_utils.bytes2dict(resp.content)['detail']
        display_utils.center_print(err_msg, type="error")
        exit(0)
    else:
        print("Login failed. Please try again with [green]girok login[/green]")
        exit(0)
    exit(0)
    

@app.command("logout", help="[red]Logout[/red] from the currently logged-in account", rich_help_panel=":lock: [bold yellow1]Authentication Commands[/bold yellow1]")
def logout():
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "guest":
        auth_utils.log_out_from_guest(cfg.config_path)
        print("Successfully logged out from [yellow]guest mode[/yellow].")
    elif mode == "user":
        auth_utils.log_out_from_user(cfg.config_path)
        # auth_utils.remove_access_token(cfg.config_path)
        print("Successfully logged out from [yellow]user mode[/yellow].")
        exit(0)
    
    
@app.command("register", help="[green]Register[/green] a new account", rich_help_panel=":lock: [bold yellow1]Authentication Commands[/bold yellow1]")
def register():
    access_token = auth_utils.get_access_token_from_json(cfg.config_path)
    if access_token and auth_utils.is_logged_in(access_token):
        print("You're logged in. Please try after log out.")
        exit(0)
        
    print(":star: Welcome to [yellow]girok[/yellow]! :star:\n")
    is_register = typer.confirm("Do you want to register a new account?")
    if is_register:
        email = typer.prompt("\nEnter email address")
        password = typer.prompt("Enter password", hide_input=True)
        confirm_password = typer.prompt("Confirm password", hide_input=True)
        auth_utils.match_passwords(password, confirm_password)
        
        # register a new account
        register_resp = auth_api.register(email, password)
        if register_resp.status_code == 201:
            print("\nPlease enter the [yellow]verification code[/yellow] sent to your email.")
            print("If you don't find it in your inbox, please check [red]spam/junk[/red] email.\n")
            cnt_try = 3
            success = False
            while cnt_try > 0:
                verification_code = typer.prompt(f"Verification code [{cnt_try} tries left]")
                if auth_api.verify_verification_code(email, verification_code): 
                    success = True
                    break
                else:
                    cnt_try -= 1
            if not success:
                display_utils.center_print("Verification failed. Please register again.", type="error")
                exit(0)
        elif register_resp.status_code == 400:
            err_msg = general_utils.bytes2dict(register_resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
            exit(0)
        else:
            err_msg = general_utils.bytes2dict(register_resp.content)['detail'][0]['msg']
            display_utils.center_print(str(err_msg), type="error")
            exit(0)
            
        display_utils.register_welcome()
        exit(0)
    else:
        exit(0)

if __name__ == '__main__':
    app()