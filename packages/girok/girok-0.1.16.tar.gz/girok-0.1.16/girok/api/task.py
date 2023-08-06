from typing import Union
from textual import log
from datetime import datetime
import requests

from girok.config import get_config
import girok.utils.auth as auth_utils
import girok.utils.display as display_utils
import girok.utils.general as general_utils
import girok.utils.task as task_utils
import girok.constants as constants

import girok.server.src.task.router as task_router

cfg = get_config()

def create_task(task_data: dict):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.post(
            cfg.base_url + "/tasks",
            json=task_data,
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 201:
            task = general_utils.bytes2dict(resp.content)
            task_id = task['task_id']
            return task_id
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, constants.DISPLAY_TERMINAL_COLOR_ERROR)
            exit(0)
        else:
            display_utils.center_print("Error occurred.", constants.DISPLAY_TERMINAL_COLOR_ERROR)
            exit(0)
    elif mode == "guest":
        resp = task_router.create_task(task_data)
        if resp['success']:
            task = resp['new_task']
            task_id = task['task_id']
            return task_id
        else:
            display_utils.center_print(resp['detail'], type="error")
            exit(0)
    exit(0) 


def get_single_task(task_id: int):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.get(
            cfg.base_url + f"/tasks/{task_id}",
            headers=auth_utils.build_jwt_header(cfg.config_path),
        )
        if resp.status_code == 200:
            task = general_utils.bytes2dict(resp.content)
            return task
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
        else:
            display_utils.center_print(resp.content, type="error")
    elif mode == "guest":
        resp = task_router.get_single_task(task_id)
        if resp['success']:
            task = resp['task']
            return task
        else:
            display_utils.center_print(resp['detail'], type="error")
    exit(0)


def get_tasks(
    cats: Union[list, None] = None,
    start_date: Union[str, None] = None,
    end_date: Union[str, None] = None,
    tag: Union[str, None] = None,
    priority: Union[int, None] = None,
    no_priority: bool = False,
    view: str = "category"
):
    mode = auth_utils.get_mode(cfg.config_path)
    query_str_obj = {
        "category": cats,
        "start_date": start_date,
        "end_date": end_date,
        "tag": tag,
        "priority": priority,
        "no_priority": no_priority,
        "view": view
    }
    if mode == "user":
        resp = requests.get(
            cfg.base_url + "/tasks",
            headers=auth_utils.build_jwt_header(cfg.config_path),
            params=query_str_obj
        )
        if resp.status_code == 200:
            return general_utils.bytes2dict(resp.content)['tasks']
        if resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
            exit(0)
        elif resp.status_code:
            display_utils.center_print("Error occurred.", type="title")
            exit(0)
    elif mode == "guest":
        resp = task_router.get_tasks(query_str_obj)
        if resp['success']:
            return resp['tasks']
        else:
            display_utils.center_print(resp['detail'], type="error")
            
    exit(0)


def remove_task(task_id: int):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.delete(
            cfg.base_url + f"/tasks/{task_id}",
            headers=auth_utils.build_jwt_header(cfg.config_path),
        )
        if resp.status_code == 204:
            return True
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
        else:
            display_utils.center_print(resp.content, type="error")
    elif mode == "guest":
        resp = task_router.delete_task(task_id)
        if resp['success']:
            return True
        else:
            display_utils.center_print(resp['detail'], type="error") 
    exit(0)

def get_tags():
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.get(
            cfg.base_url + "/tasks/tags",
            headers=auth_utils.build_jwt_header(cfg.config_path)
        )
        if resp.status_code == 200:
            return general_utils.bytes2dict(resp.content)['tags']
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
            exit(0)
        else:
            exit(0)
    elif mode == "guest":
        resp = task_router.get_tags()
        if resp['success']:
            return resp['tags']
        else:
            display_utils.center_print(resp['detail'], type="error")
    exit(0)
            
    
def change_task_tag(task_id: int, new_tag_name: str):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.patch(
            cfg.base_url + f"/tasks/{task_id}/tag",
            headers=auth_utils.build_jwt_header(cfg.config_path),
            json={
                "new_tag_name": new_tag_name
            }
        )
        
        if resp.status_code == 200:
            task = general_utils.bytes2dict(resp.content)
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s tag to {new_tag_name}.", type="success")
            return
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
        else:
            display_utils.center_print(resp.content, type="error")
    elif mode == "guest":
        resp = task_router.change_task_tag(task_id, {"new_tag_name": new_tag_name})
        if resp['success']:
            task = resp['updated_task']
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s tag to {new_tag_name}.", type="success")
            return
        else:
            display_utils.center_print(resp['detail'], constants.DISPLAY_TERMINAL_COLOR_ERROR)
    exit(0)
        
        
def change_task_priority(task_id: int, new_priority: int):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.patch(
            cfg.base_url + f"/tasks/{task_id}/priority",
            headers=auth_utils.build_jwt_header(cfg.config_path),
            json={
                "new_priority": new_priority
            }
        )
        
        if resp.status_code == 200:
            task = general_utils.bytes2dict(resp.content)
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s priority to {new_priority}.", type="success")
            return
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
        else:
            display_utils.center_print(resp.content, type="error")
    elif mode == "guest":
        resp = task_router.change_task_priority(task_id, {"new_priority": new_priority})
        if resp['success']:
            task = resp['updated_task']
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s priority to {new_priority}.", type="success")
            return
        else:
            display_utils.center_print(resp['detail'], type="error")
    exit(0)
            

        
def change_task_name(task_id: int, new_name: str):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.patch(
            cfg.base_url + f"/tasks/{task_id}/name",
            headers=auth_utils.build_jwt_header(cfg.config_path),
            json={
                "new_name": new_name
            }
        )
        
        if resp.status_code == 200:
            task = general_utils.bytes2dict(resp.content)
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s name to {new_name}.", type="success")
            return
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, constants.DISPLAY_TERMINAL_COLOR_ERROR)
        else:
            display_utils.center_print(resp.content, constants.DISPLAY_TERMINAL_COLOR_ERROR)
    elif mode == "guest":
        resp = task_router.change_task_name(task_id, {"new_name": new_name})
        if resp['success']:
            task = resp['updated_task']
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s name to {new_name}.", type="success")
            return
        else:
            display_utils.center_print(resp['detail'], constants.DISPLAY_TERMINAL_COLOR_ERROR)
    exit(0)
        

def change_task_date(task_id: int, new_date: str):
    mode = auth_utils.get_mode(cfg.config_path)
    if mode == "user":
        resp = requests.patch(
            cfg.base_url + f"/tasks/{task_id}/date",
            headers=auth_utils.build_jwt_header(cfg.config_path),
            json={
                "new_date": new_date
            }
        )
        
        if resp.status_code == 200:
            task = general_utils.bytes2dict(resp.content)
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s date to {new_date.split()[0]}.", type="success")
        elif resp.status_code == 400:
            err_msg = general_utils.bytes2dict(resp.content)['detail']
            display_utils.center_print(err_msg, type="error")
        else:
            display_utils.center_print(resp.content, type="error")
    elif mode == "guest":
        resp = task_router.change_task_date(task_id, {"new_date": new_date})
        if resp['success']:
            task = resp['updated_task']
            task_name = task['name']
            display_utils.center_print(f"Successfully changed [{task_name}]'s date to {new_date.split()[0]}.", type="success")
        else:
            display_utils.center_print(resp['detail'], type="error")
    exit(0)