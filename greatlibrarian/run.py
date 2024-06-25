from .Runner import AutoRunner, UpdateRunner
import click
from .register import register
import importlib.util
import os
import traceback


def sub_main(testcase_path, config_path, project_name, test_id, test_name, logs_path, test_type) -> None:
    spec = importlib.util.spec_from_file_location("conf", config_path)
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    config = conf_module.config
    Regis = register(config)
    testcase = testcase_path
    if Regis.checkllm():
        runner = AutoRunner(
        cfg=config,
        path=testcase,
        project_name=project_name,
        test_id=test_id,
        test_name=test_name,
        logs_path=logs_path,
        test_type=test_type
        )
        runner.run()
    else:
        error_message = "The __call__ function of your LLM can't work properly!"
        raise Warning(error_message)
    
@click.command()
@click.option(
    "--testcase_path",
    default = r"D:\GL\safetyjson",
    help="testcase的json文件所存放的文件夹路径",
)
@click.option(
    "--config_path",
    default=r"D:\GL\register_usr.py",
    help="配置文件的绝对路径",
)
@click.option("--project_name", default="", help="项目名称，默认为空字符串")
@click.option("--test_name", default="", help="实验名称，默认为空字符串")
@click.option("--test_id", default="", help="实验ID，默认为空字符串")
@click.option("--logs_path", default="", help="日志路径")
@click.option("--test_type", default="safety", help="测试类型")
def main(testcase_path, config_path, project_name, test_id, test_name, logs_path, test_type) -> str:
    # sub_main(testcase_path, config_path, project_name, test_id, test_name, logs_path,test_type)
    try:
        sub_main(testcase_path, config_path, project_name, test_id, test_name, logs_path, test_type)
    except Exception as e:
        tb_str = traceback.format_exc()
        Logs_dir = os.path.join(logs_path,'Logs')
        path = os.path.join(Logs_dir, test_id)
        record_traceback(tb_str, path)


def sub_update(config_path, test_id, logs_path,test_type) -> None:
    path = os.path.join(logs_path, "Logs")
    if os.path.exists(os.path.join(path, test_id)):
        spec = importlib.util.spec_from_file_location("conf", config_path)
        conf_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conf_module)
        config = conf_module.config
        runner = UpdateRunner(
        cfg = config, 
        Test_ID = test_id, 
        log_dir = logs_path,
        test_type = test_type
        )
        runner.run()
    else:
        error_message = "Files not Found! Please use gltest before glupdate."
        raise Warning(error_message)

@click.command()
@click.option(
    "--config_path",
    default = r"D:\GL\register_usr.py",
    help="配置文件的绝对路径",
)
@click.option("--test_id", default="", help="实验ID，默认为空字符串")
@click.option("--logs_path", default="", help="日志路径")
@click.option("--test_type", default="general", help="测试类型")
def update(config_path, test_id, logs_path, test_type) -> str:
    # sub_update(config_path, test_id, logs_path)
    try:
        sub_update(config_path, test_id, logs_path,test_type)
    except Exception as e:
        tb_str = traceback.format_exc()
        path = os.path.join(logs_path,'Logs')
        path = os.path.join(path, test_id)
        record_traceback(tb_str, path)




def record_traceback(traceback_info, file_path) -> None:
    temp_path = os.path.join(file_path, "traceback.temp")
    if traceback_info is not None:
        if not os.path.exists(temp_path):
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as temp:
            temp.write(traceback_info)



if __name__ == "__main__":
    main()
