from greatlibrarian.Configs import exconf
from greatlibrarian.Runner import AutoRunner
def main():
    runner = AutoRunner(exconf)
    runner.run()


if __name__ =='__main__':
    main()