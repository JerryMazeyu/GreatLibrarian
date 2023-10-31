from Utils import add_logger_name_cls
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from matplotlib.backends.backend_pdf import PdfPages

add_logger_to_class = add_logger_name_cls('analyse')
@add_logger_to_class
class Analyse():
    def __init__(self,score_dict) -> None:
        self.score_dict = score_dict
    
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
            conclude_info += f'The model {mean_score_list[i]} in {field_list[i]} field.\n'
        print(get_score_info)
        print(conclude_info)
        return(get_score_info,conclude_info,plotinfo)

    def report(self,plotinfo):#TODO:用图像展示以下测评结果：各领域题目回答准确率，各领域题目占比，测试题目总数，测试用时等
        field = plotinfo[0]
        score_get = plotinfo[1]
        total_score = plotinfo[2]
        totalnum = sum(total_score)

        plt.rcParams['font.size'] = 18

        pdf_file = "report.pdf"
        pdf_pages = PdfPages(pdf_file)
        # colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta']

        filtered_fields = [fields for fields, total_scores in zip(field,total_score) if total_scores > 0]
        filtered_totalscore = [totalscores for totalscores in total_score if totalscores > 0]
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









        
