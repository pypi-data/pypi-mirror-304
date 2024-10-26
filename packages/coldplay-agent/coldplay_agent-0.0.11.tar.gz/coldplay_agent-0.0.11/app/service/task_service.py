# app/service/task_service.py

import json
import shlex
import subprocess
from urllib.parse import quote, urlparse, urlunparse
from app.service.curl_service import CurlService
from app.service.util_service import UtilService
from pathlib import Path

class TaskService:
    
    @staticmethod
    def task_run(data):
        """
        处理任务运行逻辑
        """
        print(f"data: {data}")  # 打印传入的数据，便于调试
        
        # 执行脚本文件
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        task_type = data['task_type'] 
        code_type = data['code_type']
        match code_type: 
            case '1':#上传文件方式
                # 构建项目URL
                project_url = data['code_url']
                project_file_uri = data['code_file_uri'] 
                
                
                # 获取脚本的执行URL和脚本名称
                script_run_url = data['script_run_url']  # 获取脚本的运行URL
                script_name = data['script_name']  # 获取脚本的名称
                
                # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
                script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
                
                print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
                
                # 使用shlex.quote来安全处理字符串，避免命令注入
                # project_url = shlex.quote(project_url)  
                script_run_url_new = shlex.quote(script_run_url_new)

                # 获取当前文件的绝对路径
                current_file = Path(__file__).resolve()  
                
                # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
                project_app_root = current_file.parent.parent  
                
                # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
                # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
                process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new, project_file_uri]) 
            case '2':#git方式
                # 构建项目URL
                project_url = data['code_url']
                project_file_uri = data['code_file_uri'] 
                
                
                # 获取脚本的执行URL和脚本名称
                script_run_url = data['script_run_url']  # 获取脚本的运行URL
                script_name = data['script_name']  # 获取脚本的名称
                
                # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
                script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
                
                print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
                
                # 使用shlex.quote来安全处理字符串，避免命令注入
                # project_url = shlex.quote(project_url)  
                script_run_url_new = shlex.quote(script_run_url_new)

                # 获取当前文件的绝对路径
                current_file = Path(__file__).resolve()  
                
                # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
                project_app_root = current_file.parent.parent  
                
                # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
                # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
                process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new, project_file_uri])  
        
        #回传状态数据
        CurlService.update_task_status(data['task_id'],3)
        
        print(f"执行成功")  # 打印执行成功的消息
        
        return True  # 返回True表示任务执行成功

    
    @staticmethod
    def task_stop(data):
        """
        处理任务终止逻辑
        """
        print(f"stop run")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()

        # 获取脚本的执行URL和脚本名称
        script_run_url = data['script_run_url']  # 获取脚本的运行URL
        script_name = data['script_name']  # 获取脚本的名称
        
        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent  # 假设项目目录在上级
        subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_task.sh", script_run_url_new])

        #回传状态数据
        CurlService.update_task_status(data['task_id'],6)
        print(f"执行成功")

        return True
    

    @staticmethod
    def task_pause(data):
        """
        处理任务暂停逻辑
        """
        print(f"pause run")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()

        # 获取脚本的执行URL和脚本名称
        script_run_url = data['script_run_url']  # 获取脚本的运行URL
        script_name = data['script_name']  # 获取脚本的名称
        
        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent  # 假设项目目录在上级
        subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_task.sh", script_run_url_new])
        #回传状态数据
        CurlService.update_task_status(data['task_id'],4)
        print(f"执行成功")

        return True
    
    def task_restart(data):
        """
        处理任务重新运行逻辑
        """
        print(f"data: {data}")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        coldplay_config = UtilService.load_coldplay_config()
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')
        # 构建项目URL
        project_url = data['code_url']
        project_file_uri = data['code_file_uri'] 
        
        
        # 获取脚本的执行URL和脚本名称
        script_run_url = data['script_run_url']  # 获取脚本的运行URL
        script_name = data['script_name']  # 获取脚本的名称
        
        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        
        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
        
        # 使用shlex.quote来安全处理字符串，避免命令注入
        # project_url = shlex.quote(project_url)  
        script_run_url_new = shlex.quote(script_run_url_new)

        # 获取当前文件的绝对路径
        current_file = Path(__file__).resolve()  
        
        # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
        project_app_root = current_file.parent.parent  
        
        # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
        # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
        process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new, project_file_uri]) 
        #回传状态数据
        CurlService.update_task_status(data['task_id'],3)
        print(f"执行成功")

        return True