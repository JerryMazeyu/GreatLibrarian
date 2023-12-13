from greatlibrarian.Runner import AutoRunner
import click
from greatlibrarian.register import *
import importlib.util
import warnings


@click.command()
@click.option(
    "--testcase_path",
    default="/home/ubuntu/LLMs/czy/GreatLibrarian/Test",
    help="testcase的json文件所存放的文件夹路径",
)
@click.option(
    "--config_path",
    default="/home/ubuntu/LLMs/czy/GreatLibrarian/register_usr.py",
    help="配置文件的绝对路径",
)
@click.option("--project_name", default="", help="项目名称，默认为空字符串")
def main(testcase_path, config_path, project_name):
    spec = importlib.util.spec_from_file_location("conf", config_path)
    # spec = importlib.util.spec_from_file_location('conf', '/home/ubuntu/LLMs/czy/GreatLibrarian/register_usr.py')
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    config = conf_module.config
    Regis = register(config)
    testcase = testcase_path
    # testcase_path = '/home/ubuntu/LLMs/czy/GreatLibrarian/Testcase'
    if Regis.checkllm():
        runner = AutoRunner(config, testcase, project_name)
        runner.run()
    else:
        error_message = "The __call__ function of your LLM can't work properly!"
        raise Warning(error_message)


if __name__ == "__main__":
    main()
