from Utils import add_logger_name_cls,generate_logger_subfile,generate_name_new
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.pdfgen import canvas
import os 
from Utils import extract_mistaken_info
import matplotlib
import textwrap

# log_name = generate_name_new('analyse')
log_name = 'analyse'
logger_name = 'analyse.log'
logger_subfile = generate_logger_subfile()
add_logger_to_class = add_logger_name_cls(log_name,os.path.join('Logs',logger_subfile))
logger_path = os.path.join(os.path.join('Logs',logger_subfile))
@add_logger_to_class
class Analyse():
    def __init__(self,score_dict) -> None:
        self.score_dict = score_dict
        self.logger_path = logger_path
    
    def analyse(self):
        """
        A function to analyse the score that LLM gets in the testproject, including many testcases.
        The information used for analysis comes from the function get_eval_result in class getinfo.
        By reading the information(a dictionary) provided by the function get_eval_result, this function will create a new log file and write the analysis in it.
        The avarage socre that the LLM gets in testcase will be recorded, and finally the function will give an overall evaluation of the LLM.
        The log file generated by this function is formatted like: 
        "By 'keywords' evaluation, the LLM gets XX(0-1) scores in average.
         By 'toolUsage' evaluation, the LLM gets XX(0-1) scores in average.
         By 'gpt4Eval' evaluation, the LLM gets XX(0-1) scores in average.
         To conclude, the LLM …"
        
        """
        score = self.score_dict
        score_list = []
        score_mean = [0]*10
        score_get = [0]*10
        field_list = ['knowledge_understanding', 'coding', 'common_knowledge', 'reasoning', 'multi_language', 'specialized_knowledge', 'traceability', 'outputformatting', 'internal_security', 'external_security']
        total_score = [0]*10

        for i in range(10):
            score_list.append(score[field_list[i]])

        for i in range(10):
            if score_list[i] == []:
                score_mean[i] = 'Not evaluated in this field'
            else:
                score_mean[i] = float('%.3f'%(sum(score_list[i])/len(score_list[i])))
                total_score[i] = (len(score_list[i]))
                score_get[i] = float('%.3f'%(sum(score_list[i])))
        get_score_info=''

        for i in range (10):
            get_score_info += f'\nIn {field_list[i]} field, the LLM gets "{score_get[i]}/{total_score[i]}" scores.\n'

        plotinfo = [field_list,score_get,total_score]

        mean_score_list=[]
        for score in score_mean:
            if score!='Not evaluated in this field':
                if score>=0.6:
                    mean_score_list.append('does well in')
                else:
                    mean_score_list.append('is not good at')
            else:
                mean_score_list.append('is not evaluated')
        conclude_info = 'To conclude:\n'
        for i in range (10):
            conclude_info += f'\nThe model {mean_score_list[i]} in {field_list[i]} field.\n'
        print(get_score_info)
        print(conclude_info)
        return(get_score_info,conclude_info,plotinfo)

    def report(self,plotinfo,log_path):#TODO:用图像展示以下测评结果：各领域题目回答准确率，各领域题目占比，测试题目总数，测试用时等
        """
        log_path:The path of the dialog_init.log
        logger_path:A gloabal variable, the path to the analyse.log

        """
        field = plotinfo[0]
        score_get = plotinfo[1]
        total_score = plotinfo[2]
        totalnum = sum(total_score)

        plt.rcParams['font.size'] = 18

        pdf_name = "report.pdf"
        pdf_file_path = os.path.join(logger_path,pdf_name)

        pdf_pages = PdfPages(pdf_file_path)
        # colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta']

        fig = plt.figure(figsize=(20,20))


        title = "Test Statistics"
        plt.title(title, fontsize=32, ha='center',y=1.1)

        filtered_fields = [fields for fields, total_scores in zip(field,total_score) if total_scores > 0]
        filtered_totalscore = [totalscores for totalscores in total_score if totalscores > 0]
        filtered_score_get = [score for score,total_scores in zip(score_get,total_score) if total_scores > 0]

        field_info = ''
        if len(filtered_fields)<=3:
            for fields in filtered_fields:
                field_info += f'"{str(fields)}"'
        else:
            for i in range (3):
                field_info += f'"{str(filtered_fields[i])}"'
            field_info += ' and so on.'

        testcasenum_info = ''
        for i in range (len(filtered_fields)):
            testcasenum_info += f'\nThere are {filtered_totalscore[i]} testcases in "{filtered_fields[i]}"\n'

        score_info = ''
        for i in range (len(filtered_score_get)):
            score_info += f'\nIn "{filtered_fields[i]}" ,The score of the LLm is : {filtered_score_get[i]}/{filtered_totalscore[i]}\n'

        conclude_info = f'This test contains {totalnum} testcases.\n\nThe testcases involves ' + field_info + f'\n\nAmong all testcases:\n' + testcasenum_info + score_info
        
        fig.text(0.1,0.55, conclude_info, fontsize=21, ha='left', va='center')

        plt.axis('off')

        pdf_pages.savefig(fig)


        fig = plt.figure(figsize=(30, 30))

        title = "Mistaken Cases"
        plt.title(title, fontsize=32, ha='center',y=1.1)

        mistaken_list = extract_mistaken_info(log_path)
        mistaken_txt = ''

        for i in range (len(mistaken_list)):
            mistaken_list[i][0] = textwrap.fill(mistaken_list[i][0], width=80)
            mistaken_list[i][1] = textwrap.fill(mistaken_list[i][1], width=80)

        if len(mistaken_list) <= 5:
            for mistakens in mistaken_list:
                mistaken = f'\n\nFor this testcase in {mistakens[2]} field, the LLM made a mistake.\n\nTo LLM:“{mistakens[0]}”\n\nTo user:“{mistakens[1]}”'
                mistaken_txt += mistaken
        else:
            for i in range (5):
                mistaken = f'\n\nFor this testcase in {mistaken_list[i][2]} field, the LLM made a mistake.\n\nTo LLM:“{mistaken_list[i][0]}”\n\nTo user:“{mistaken_list[i][1]}”'
                mistaken_txt += mistaken
        
        fig.text(0.1,0.5, mistaken_txt, fontsize=22, fontfamily='SimSun',ha='left', va='center')
        plt.axis('off')

        pdf_pages.savefig(fig)
        
        
        percentages = [num / totalnum for num in filtered_totalscore]
        plt.figure(figsize=(20, 20))
        patches, texts, autotexts = plt.pie(percentages, labels=filtered_fields, autopct='%1.1f%%', startangle=140)
        plt.title("Percentage of fields",fontsize=50, y=1.15)
        plt.axis('equal')
        # for i, label in enumerate(field):
        #     plt.text(2, -1 - i * 0.5, label, color=colors[i])
        ax = plt.gca()
        ax.set_aspect('equal')  
        ax.set_position([0.2, 0.2, 0.6, 0.6])  
        legend_labels = ['{}'.format(filtered_field) for filtered_field in filtered_fields]
        legend = plt.legend(patches, legend_labels, loc="lower left", bbox_to_anchor=(-0.3, -0.3))

        pdf_pages.savefig()
        plt.clf()

        accuracies = []
        labels = []

        for score, total in zip(score_get, total_score):
            if total == 0:
                accuracy = 0
                label = "Not Tested"
            else:
                accuracy = (score / total) * 100
                label = f"{accuracy:.2f}%"
            accuracies.append(accuracy)
            labels.append(label)

        plt.figure(figsize=(20, 20))
        bars = plt.bar(field, accuracies)
        plt.xlabel('Field',fontsize = 25)
        plt.ylabel('Accuracy',fontsize = 25)
        plt.title('Accuracy in each field',fontsize=50, y=1.15)
        plt.xticks(rotation=45, ha="right")

        for i, (bar, label) in enumerate(zip(bars, labels)):
            if label == "Not Tested":
                plt.text(i, bar.get_height(), label, ha="center", va="bottom")
            elif accuracies[i] >= 0:
                plt.text(i, bar.get_height(), label, ha="center", va="bottom")

        plt.tight_layout()
        pdf_pages.savefig()
        pdf_pages.close()

        print("Report Generated !")









        
