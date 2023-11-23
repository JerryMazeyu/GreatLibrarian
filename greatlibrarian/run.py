from greatlibrarian.Configs import exconf
from greatlibrarian.Runner import AutoRunner
import click

@click.command()
@click.option('--path', default='TestCase', help='testcase的json文件所存放的文件夹路径')
def main(path):
    runner = AutoRunner(exconf,path)
    runner.run()

if __name__ =='__main__':
    main()