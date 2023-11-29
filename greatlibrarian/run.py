from greatlibrarian.Configs import exconf
from greatlibrarian.Runner import AutoRunner
import click
from greatlibrarian.register import *
import importlib.util

@click.command()
@click.option('--testcase_path', default='TestCase', help='testcase的json文件所存放的文件夹路径')
@click.option('--config_path', default=' ', help='配置文件的绝对路径')
def main(testcase_path,config_path):

    spec = importlib.util.spec_from_file_location('conf', config_path)
    # spec = importlib.util.spec_from_file_location('conf', '/home/ubuntu/LLMs/czy/GreatLibrarian/register_usr.py')
    conf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conf_module)
    config = conf_module.config
    Regis = register(config)
    testcase = testcase_path
    # testcase_path = '/home/ubuntu/LLMs/czy/GreatLibrarian/Testcase'
    if Regis.checkllm():
        runner = AutoRunner(config,testcase)
        runner.run()
    else:
        print('Something went wrong in your config file!')
        
    # runner = AutoRunner(testcase_path,config_path)
    # runner.run()

if __name__ =='__main__':
    main()