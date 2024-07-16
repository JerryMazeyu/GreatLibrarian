import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from greatlibrarian.Utils import extract_mistaken_info, extract_example_info
import matplotlib
import textwrap
from matplotlib import rcParams
import warnings
from typing import Tuple, List, Union
import re
from datetime import datetime
import matplotlib.font_manager as fm
import markdown
import markdown.extensions
from markdown.extensions import tables
from markdown.extensions import fenced_code
from markdown.extensions import extra
from markdown.extensions import codehilite
from markdown.extensions import toc
from markdown.extensions import md_in_html
from Utils import to_str
import pandoc
import pypandoc

# import pdfkit


# log_name = generate_name_new('analyse')
# log_name = "analyse"
# logger_name = "analyse.log"
# if Test_ID == '':
#     logger_subfile = generate_logger_subfile()
# else:
#     logger_subfile = Test_ID
# add_logger_to_class = add_logger_name_cls(
#     log_name, os.path.join("Logs", logger_subfile)
# )
# logger_path = os.path.join(os.path.join("Logs", logger_subfile))


# @add_logger_to_class
class Analyse:
    """A class to do the analysis after the interaction."""

    def __init__(self, score_dict) -> None:
        self.score_dict = score_dict

    def analyse(
        self,
    ) -> Tuple[str, str, List[Union[List[str], List[float], List[int]]]]:
        """
        A function to analyse the score that LLM gets in the testproject, including many testcases.
        The information used for analysis comes from the function get_eval_result in class getinfo.
        By reading the information(a dictionary) provided by the function get_eval_result, this function will create a new log file and write the analysis in it.
        The average score that the LLM gets in the testcase will be recorded, and finally the function will give an overall evaluation of the LLM.
        The log file generated by this function is formatted like:
        "By 'keywords' evaluation, the LLM gets XX(0-1) scores on average.
        By 'toolUsage' evaluation, the LLM gets XX(0-1) scores on average.
        By 'LLMEval' evaluation, the LLM gets XX(0-1) scores on average.
        To conclude, the LLM …"
        """

        score = self.score_dict
        score_list = []
        score_mean = [0] * len(score)
        score_get = [0] * len(score)
        field_list = list(score.keys())
        total_score = [0] * len(score)

        for i in range(len(score)):
            score_list.append(score[field_list[i]])

        for i in range(len(score)):
            if score_list[i] == []:
                score_mean[i] = "Not evaluated in this field"
            else:
                score_mean[i] = float(
                    "%.3f" % (sum(score_list[i]) / len(score_list[i]))
                )
                total_score[i] = len(score_list[i])
                score_get[i] = float("%.3f" % (sum(score_list[i])))
        get_score_info = ""

        for i in range(len(score)):
            get_score_info += f'\nIn {field_list[i]} field, the LLM gets "{score_get[i]}/{total_score[i]}" scores.\n'

        plotinfo = [field_list, score_get, total_score]

        mean_score_list = []
        for scores in score_mean:
            if scores != "Not evaluated in this field":
                if scores >= 0.6:
                    mean_score_list.append("does well in")
                else:
                    mean_score_list.append("is not good at")
            else:
                mean_score_list.append("is not evaluated")
        conclude_info = "To conclude:\n"
        for i in range(len(score)):
            conclude_info += (
                f"\nThe model {mean_score_list[i]} in {field_list[i]} field.\n"
            )
        print(get_score_info)
        print(conclude_info)
        return (get_score_info, conclude_info, plotinfo)

    def report(self, plotinfo, llm_intro, log_path, report_path, test_type) -> None:
        """
        log_path: The path of the dialog_init.log
        logger_path: the path to the analyse.log
        """
        custom_font_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fonts", "simsun.ttf"
        )
        plt.rcParams["font.family"] = fm.FontProperties(
            fname=custom_font_path
        ).get_name()
        field = plotinfo[0]
        score_get = plotinfo[1]
        total_score = plotinfo[2]
        totalnum = sum(total_score)

        version_number = self.get_next_version_number(report_path)
        # md_name = self.generate_new_name(report_path, "report")
        # md_files = self.change_extension(md_name, "") + "-md"
        md_files = 'report-v' + to_str(version_number) + '-md'
        md_files_path = os.path.join(report_path, md_files)
        md_name = "report-v" + to_str(version_number) + ".md"
        os.makedirs(md_files_path)
        md_file_path = os.path.join(md_files_path, md_name)

        # 1.背景介绍

        intro = self.introduction_of_llm(log_path, llm_intro)
        with open(md_file_path, "a", encoding="utf-8") as f:
            f.write("# 测试报告\n\n")
            f.write("## 背景介绍\n")
            f.write(intro)

        # 2.测试用例数据信息

        field_info = ""
        if len(field) <= 3:
            for fields in field:
                field_info += f'"{(fields)}"'
            field_info += "领域"
        else:
            for i in range(3):
                field_info += f'"{str(field[i])}"'
            field_info += "等领域。"

        testcasenum_info = ""
        for i in range(len(field)):
            testcasenum_info += f"\n “{field[i]}”领域中有{total_score[i]}条测试用例。\n"
        score_info = ""
        for i in range(len(score_get)):
            score_info += f"\n在“{field[i]}”领域中 ,该大语言模型的得分为: {score_get[i]}/{total_score[i]}。\n"

        time = self.extract_time(log_path)
        if totalnum != 0:
            time_per_testcase = round(time / totalnum, 3)
            time_info = (
                f"在本次测试中，LLM的响应时间为：平均每条测试用例{time_per_testcase}秒"
            )
        else:
            time_info = f"等待人工审核后计算平均响应时间"

        conclude_info = (
            f"本次测试包括{totalnum}条测试用例.\n这些测试用例主要包括"
            + field_info
            + f"\n在所有测试用例中:\n"
            + testcasenum_info
            + score_info
            + "\n"
            + time_info
        )
        with open(md_file_path, "a", encoding="utf-8") as f:
            f.write("# 测试用例数据\n")
            f.write(conclude_info)

        # 饼状图绘制

        # percentages = [num / sum(total_score) for num in total_score]
        # plt.figure(figsize=(20, 20))
        # patches, texts, autotexts = plt.pie(
        #     percentages, labels=field, autopct="%1.1f%%", startangle=140
        # )

        # for autotext in autotexts:
        #     autotext.set_size(24)
        # for text in texts:
        #     text.set_size(24)

        # plt.axis("equal")

        # plt.title("各领域测试用例占比", fontsize=32, pad=20, y=1.05)

        # plt.legend(patches, field, loc="lower right", fontsize=20, bbox_to_anchor=(1.05, 0.07))

        # pie_chart_filepath = os.path.join(report_path, 'pie.png')
        # plt.savefig(pie_chart_filepath)
        # plt.close()

        # with open(md_file_path, 'a', encoding='utf-8') as f:
        #     f.write('![Pie Chart](pie.png)\n')

        percentages = [num / sum(total_score) for num in total_score]
        plt.figure(figsize=(12, 12))
        patches, texts, autotexts = plt.pie(
            percentages, labels=field, autopct="%1.1f%%", startangle=140
        )

        for autotext in autotexts:
            autotext.set_size(15)
        for text in texts:
            text.set_size(15)

        plt.axis("equal")

        plt.title("各领域测试用例占比", fontsize=20, pad=12, y=1.05)

        plt.legend(
            patches, field, loc="lower right", fontsize=12, bbox_to_anchor=(1.05, 0.07)
        )

        pie_name = f"piev{version_number}.png"

        pie_chart_filepath = os.path.join(md_files_path, pie_name)
        plt.savefig(pie_chart_filepath)
        plt.close()

        with open(md_file_path, "a", encoding="utf-8") as f:
            f.write("![Pie Chart](" + pie_name + ")\n\n")

        # 3.错误的测试用例

        mistaken_list = extract_mistaken_info(log_path, test_type)
        mistaken_txt = ""

        if len(mistaken_list) <= 4:
            for mistakens in mistaken_list:
                mistakens[0] = mistakens[0].replace("\\\\", "\\")
                mistakens[1] = mistakens[1].replace("\\\\\\\\", "\\")
                mistakens[1] = mistakens[1].replace("\\\\n\\\\n", "<br>")
                mistakens[1] = mistakens[1].replace("\\\\n", "<br>")
                mistakens[1] = mistakens[1].replace("$$", "$")

                if len(mistakens) == 5:
                    mistaken = (
                        f"\n\n对于以下这条属于{mistakens[2]}领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistakens[0]}\n\n"
                        + f"回答：{mistakens[1]}"
                        + f"\n\n该问题的正确答案应包含关键字：{mistakens[3]},不应包含黑名单：{mistakens[4]}。\n\n"
                    )
                    mistaken_txt += mistaken
                if len(mistakens) == 4:
                    mistaken = (
                        f"\n\n对于以下这条属于{mistakens[2]}领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistakens[0]}\n\n"
                        + f"回答：{mistakens[1]}"
                        + f"\n\n该问题的正确答案应包含关键字：{mistakens[3]}。\n\n"
                    )
                    mistaken_txt += mistaken

                if len(mistakens) == 3:
                    mistaken = (
                        f"\n\n对于以下这条属于{mistakens[2]}领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistakens[0]}\n\n"
                        + f"回答：{mistakens[1]}"
                        + "\n\n"
                    )
                    mistaken_txt += mistaken
        else:
            for i in range(4):
                mistaken_list[i][0] = mistaken_list[i][0].replace("\\\\", "\\")
                mistaken_list[i][1] = mistaken_list[i][1].replace("\\\\\\\\", "\\")
                mistaken_list[i][1] = mistaken_list[i][1].replace("\\\\n\\\\n", "<br>")
                mistaken_list[i][1] = mistaken_list[i][1].replace("\\\\n", "<br>")
                mistaken_list[i][1] = mistaken_list[i][1].replace("$$", "$")
                if len(mistaken_list[i]) == 5:
                    mistaken = (
                        f'\n\n对于以下这条属于"{mistaken_list[i][2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistaken_list[i][0]}\n\n'
                        + f"回答：{mistaken_list[i][1]}"
                        + f"\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]},不应包含黑名单：{mistaken_list[i][4]}。\n\n"
                    )
                    mistaken_txt += mistaken
                if len(mistaken_list[i]) == 4:
                    mistaken = (
                        f'\n\n对于以下这条属于"{mistaken_list[i][2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistaken_list[i][0]}\n\n'
                        + rf"回答：{mistaken_list[i][1]}"
                        + f"\n\n该问题的正确答案应包含关键字：{mistaken_list[i][3]}。\n\n"
                    )
                    mistaken_txt += mistaken

                if len(mistaken_list[i]) == 3:
                    mistaken = (
                        f'\n\n对于以下这条属于"{mistaken_list[i][2]}"领域的问题，该大语言模型的回答出现了错误。\n\n问题：{mistaken_list[i][0]}\n\n'
                        + rf"回答：{mistaken_list[i][1]}"
                        + "\n\n"
                    )
                    mistaken_txt += mistaken
        if mistaken_txt == "":
            mistaken_txt += (
                "\n该LLM完全通过了本次测试，正确回答了所有的测试用例，无错误用例。\n"
            )

        with open(md_file_path, "a", encoding="utf-8") as f:
            f.write("## 错误用例展示\n")
            f.write(mistaken_txt)

        # 4.测试的各领域的得分率柱状图

        # accuracies = []
        # labels = []

        # for score, total in zip(score_get, total_score):
        #     if total == 0:
        #         continue
        #     else:
        #         accuracy = (score / total) * 100
        #         label = f"{accuracy:.2f}%"
        #     accuracies.append(accuracy)
        #     labels.append(label)

        # plt.figure(figsize=(26, 26))
        # bars = plt.bar(field, accuracies)
        # plt.xlabel("领域", fontsize=32)
        # plt.ylabel("得分率 (%)", fontsize=32)
        # plt.title("各领域答题得分率", fontsize=35, y=1.05)
        # plt.xticks(rotation=45, ha="right", fontsize=28)
        # plt.yticks(fontsize=28)

        # for i, (bar, label) in enumerate(zip(bars, labels)):
        #     plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, label,
        #             ha='center', va='bottom', fontsize=24)

        # bar_chart_filepath = os.path.join(report_path, 'bar.png')
        # plt.savefig(bar_chart_filepath)
        # plt.close()

        # with open(md_file_path, 'a', encoding='utf-8') as f:
        #     f.write('## 各领域答题得分率\n')
        #     f.write('![Bar Chart](bar.png)\n')

        # with open(md_file_path, 'r', encoding='utf-8') as f:
        #     markdown_text = f.read()

        # html_content = markdown.markdown(markdown_text)
        # html_name = self.change_extension(md_name, ".html")
        # html_path = os.path.join(report_path, html_name)
        # with open(html_path, 'w', encoding='utf-8') as f:
        #     f.write(html_content)

        accuracies = []
        labels = []

        for score, total in zip(score_get, total_score):
            if total == 0:
                continue
            else:
                accuracy = (score / total) * 100
                label = f"{accuracy:.2f}%"
            accuracies.append(accuracy)
            labels.append(label)

        plt.figure(figsize=(14, 14))
        bars = plt.bar(field, accuracies)
        plt.xlabel("领域", fontsize=16)
        plt.ylabel("得分率 (%)", fontsize=16)
        plt.title("各领域答题得分率", fontsize=18, y=1.05)
        plt.xticks(rotation=45, ha="right", fontsize=14)
        plt.yticks(fontsize=14)

        for i, (bar, label) in enumerate(zip(bars, labels)):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                label,
                ha="center",
                va="bottom",
                fontsize=12,
            )

        bar_name = f"barv{version_number}.png"

        bar_chart_filepath = os.path.join(md_files_path, bar_name)
        plt.savefig(bar_chart_filepath)
        plt.close()

        with open(md_file_path, "a", encoding="utf-8") as f:
            f.write("## 各领域答题得分率\n")
            f.write("![Bar Chart](" + bar_name + ")\n")

        html_name = self.change_extension(md_name, ".html")
        html_path = os.path.join(report_path, html_name)
        # self.convert_markdown_to_html(report_path, html_path)
        # pdf_name = self.change_extension(md_name, ".pdf")
        # pdf_path = os.path.join(report_path, pdf_name)
        # pdfkit.from_file(html_path, pdf_path)
        print("Report Generated !")

    def introduction_of_llm(self, log_path, llm_intro) -> str:

        ex_list = extract_example_info(log_path)

        example_txt = "以下是本次测试中的几条测试用例及其回答：\n"

        if len(ex_list) == 0:
            example_txt += "本次测试中，该大语言模型未答对任何问题"

        if len(ex_list) <= 3 and len(ex_list) > 0:
            for ex in ex_list:
                ex[0] = ex[0].replace("\\\\", "\\")
                ex[1] = ex[1].replace("\\\\\\\\", "\\")
                ex[1] = ex[1].replace("\\\\n\\\\n", "<br>")
                ex[1] = ex[1].replace("\\\\n", "<br>")
                ex[1] = ex[1].replace("$$", "$")
                example = (
                    "\n\n"
                    + f'对于以下这条属于"{ex[2]}"领域的问题，该大语言模型的回答完全正确。'
                    + "\n\n"
                    + f"问题：{ex[0]}"
                    + "\n\n"
                    + f"回答：{ex[1]}"
                    + "\n\n"
                )
                example_txt += example
        if len(ex_list) > 3:
            for i in range(3):
                ex_list[i][0] = ex_list[i][0].replace("\\\\", "\\")
                ex_list[i][1] = ex_list[i][1].replace("\\\\\\\\", "\\")
                ex_list[i][1] = ex_list[i][1].replace("\\\\n\\\\n", "<br>")
                ex_list[i][1] = ex_list[i][1].replace("\\\\n", "<br>")
                ex_list[i][1] = ex_list[i][1].replace("$$", "$")
                example = (
                    "\n\n"
                    + f'对于以下这条属于"{ex_list[i][2]}"领域的问题，该大语言模型的回答完全正确。'
                    + "\n\n"
                    + f"问题：{ex_list[i][0]}"
                    + "\n\n"
                    + f"回答：{ex_list[i][1]}"
                    + "\n\n"
                )
                example_txt += example

        intro = "这是一个对于场景化大语言模型的自动化测评报告。\n\n由于工具中暂无关于当前大语言模型的背景信息，所以当前页仅展示本次测评中大语言模型答对的数条测试样例。\n\n"

        if llm_intro != "":
            intro = llm_intro
            intro += "\n\n本次对该大语言模型的测试涉及多个领域的问题，测试的结果和分析如下文所示。\n\n"
            intro += example_txt
        return intro

    # def generate_new_name(self, folder_path, base_name):
    #     pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    #     version_numbers = [
    #         int(re.search(rf"{base_name}-v(\d+).pdf", f).group(1))
    #         for f in pdf_files
    #         if re.match(rf"{base_name}-v\d+.pdf", f)
    #     ]
    #     max_version = max(version_numbers) if version_numbers else 0
    #     new_name = f"{base_name}-v{max_version + 1}.pdf"
    #     return new_name

    def generate_new_name(self, folder_path, base_name):
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
        version_numbers = [
            int(re.search(rf"{base_name}-v(\d+).md", f).group(1))
            for f in pdf_files
            if re.match(rf"{base_name}-v\d+.md", f)
        ]
        max_version = max(version_numbers) if version_numbers else 0
        new_name = f"{base_name}-v{max_version + 1}.md"
        return new_name

    def get_next_version_number(self, folder_path):
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)) and f.startswith("report-")]
        version_numbers = [
            int(re.search(rf"report-v(\d+)-md", f).group(1))
            for f in subfolders
            if re.match(rf"report-v\d+-md", f)
        ]
        if version_numbers:
            next_version = max(version_numbers) + 1
        else:
            next_version = 1
        return next_version

    def extract_time(self, log_path):
        with open(log_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        time_pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

        all_times = []

        for line in lines:
            time_match = time_pattern.search(line)
            if time_match:
                time_str = time_match.group(0)
                time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                all_times.append(time_obj)

        if all_times:
            min_time = min(all_times)
            max_time = max(all_times)

            time_difference = max_time - min_time
            return time_difference.total_seconds()
        else:
            return None

    def change_extension(self, filename, new_extension):
        root, ext = os.path.splitext(filename)
        new_filename = root + new_extension

        return new_filename

    def convert_markdown_to_html(self, input_md_file, output_html_file):
        path = os.path.normpath(input_md_file)
        with open(path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        # 使用arithmatex扩展支持数学表达式
        extensions = [
            "markdown.extensions.tables",  # 支持表格
            "markdown.extensions.fenced_code",  # 支持代码块
            "markdown.extensions.extra",  # 支持额外的 Markdown 语法
            "markdown.extensions.codehilite",  # 代码块语法高亮
            "markdown.extensions.toc",  # 自动生成目录
            "pymdownx.arithmatex",  # 支持数学表达式
            "markdown.extensions.md_in_html",
        ]

        html_content = markdown.markdown(markdown_text, extensions=extensions)

        # 添加必要的MathJax脚本以支持数学表达式
        mathjax_script = """
        <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            },
            svg: {
                fontCache: 'global'
            }
        };
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
        </script>
        """

        html_with_style_and_mathjax = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Markdown to HTML</title>
            <style>
                body {{
                    font-size: 25px; /* 设置整体文本大小 */
                }}
                h2 {{
                    font-size: 32px; /* 设置 h2 标题大小 */
                }}
                /* 可以添加其他样式来调整不同元素的大小 */
            </style>
            {mathjax_script}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        with open(output_html_file, "w", encoding="utf-8") as f:
            f.write(html_with_style_and_mathjax)
