# 场景化大语言模型自动化测评工具箱  

*****
  
![piDYfgK.jpg](https://z1.ax1x.com/2023/11/29/piDYfgK.jpg)
  
  
本项目旨在对场景化的大语言模型进行**自动化的评测**，用户只需要提供测试的大语言模型的 `API Key` 以及准备用于测试的**测试用例**，该工具就可以自动完成一个完整的测评过程，包括：**用户选择各个评分方法的评分细则** → **工具箱自动的与大语言模型进行交互** → **将对话内容记录进日志** → **对每一条测试用例进行打分** → **对得分情况进行分析** → **总结本次测评的信息并生成报告**。在自动化评测的流程结束后，用户可以在最终生成测评报告中直观的查看到本次测评的所有信息。  

![](https://jerrymazeyu.oss-cn-shanghai.aliyuncs.com/2023-07-06-DALL%C2%B7E%202023-07-06%2013.39.16%20-%20An%20omnipotent%20librarian%20with%20a%20galaxy%20as%20his%20head-%20suitable%20for%20a%20logo..png)  

## 介绍  

本项目主要实现语言为python，测试用例为`json`格式，最终生成的报告为PDF格式。按照工具的功能模块，分为四个部分介绍工具箱，分别为：**测前准备、自动化测评、评分规则、报告生成**。  

### 测前准备  
  
需要用户在`GreatLibrarian`目录下的`register_usr.py`文件中进行一些基本的配置
  
#### LLM配置  
 
如果需要加入LLM并用其`API Key`进行测试，需要先在`/GreatLibrarian/register_usr.py`中创建一个新的LLMs的子类（下文用`new_llm`指代这个新的子类的名称），并用LLM_base.register_module("name of your LLM")装饰器装饰，其方法需包括：  
1. 包括LLM的 `API Key` 以及`name` 等信息的 `__init__` 函数(**`self.llm_intro`可以选择设置成该LLM的背景介绍或为空，但是建议设置为LLM的详细背景介绍**）  
2. 输入为字符串格式的`prompt`，输出为字符串格式的该LLM的对于该`prompt`的回答的 `__call__` 函数。在定义该 `call` 函数时，请尽量保证其**鲁棒性** ，以防因**响应故障**等非工具箱内部原因导致的测试异常中止。**我们要求在API正常响应时返回字符串类型的回答，API异常时返回"API Problem"**。
3. 使用该LLM类设置基本信息（`name`,`API Key`等等）作为参数，创建一个`llm_cfg`  

`llm_cfg = dict(type='qwen_turbo',apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8", name = "qwen_turbo",llm_intro = '千问')`  

4. 使用创建的`llm_cfg`作为参数，用LLM_base.build（）创建一个LLM的实例
5.  以下是一个例子，该范例也在`register_usr.py`文件中，可以用于用户新增LLM类时的参考，请注意，**务必使用范例中的装饰器，参数为LLM的名称，类型是字符串；并且该类必须继承抽象类LLMs**。   
  

        from greatlibrarian.Configs import ExampleConfig
        from greatlibrarian.Utils import Registry
        from greatlibrarian.Core import LLMs,FinalScore  
  
        @LLM_base.register_module("qwen_turbo")
        class new_llm(LLMs):
            def __init__(self,apikey,name,llm_intro):
                self.apikey = apikey
                self.name = name
                self.llm_intro = llm_intro
    
            def get_intro(self):
                return self.llm_intro
    
            def get_name(self):
                return self.name
    
            def __call__(self, prompt: str) -> str:
                dashscope.api_key = self.apikey
                response = dashscope.Generation.call(
                model = dashscope.Generation.Models.qwen_turbo,
                prompt=prompt
                )

                if response:
                    if response['output']:
                        if response['output']['text']:
                           return(response['output']['text'])
                return('API Problem')

        llm_cfg = dict(type='qwen_turbo',apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8", name = "qwen_turbo",llm_intro = '千问')
        qw = LLM_base.build(llm_cfg)
    
然后用户需要在该文件中中创建一个`ExampleConfig()`类的实例config（**请勿修改该实例名称config**），并用刚刚创建的实例（`qw`）对其进行初始化  
  
`config = ExampleConfig(qw)`


#### 测试用例配置  


本工具箱使用的测试用例为统一的`json`格式，示范格式如下：

    {
    "name": "地理知识",  
    "description": "中考真题",  
    "field":"knowledge_understanding",  
    "prompts": [
        "我国最早发展高新技术产业的地区是_____。",
        "我国位置最北、纬度最高的省级行政区：",
        "我国面积最大的省级行政区： ",
        "邻省最多的省级行政区：",
        "我国面积最大的平原： "],
    "evaluation": {
            "0": [{"keywords":[["中关村"]],"blacklist":[["硅谷"]]}],
            "1": [{"keywords":[["黑龙江省"]]},"GPT4eval":[[True]]],
            "2": [{"keywords":[["新疆维吾尔自治区"]]}],
            "3": [{"keywords":[["内蒙古自治区", "陕西省"]]}],
            "4": [{"keywords":[["东北平原"]]}]
    }
    }


一组测试用例整体是一个字典，在示范的配置中，`name`和`description`两个字符串，分别是这段测试用例组的名称和描述，主要起区分作用，对测试结果无影响。 

 `field`字符串用于定义测试用例组所属的领域，在我们的工具箱中，测试领域一个被划分为十种，它们分别为：语言理解、代码、知识与常识、逻辑推理、多语言、专业知识、可追溯性、输出格式化、内生安全性、外生安全性。它们对应的 `field` 名称分别为：`knowledge_understanding、coding、common_knowledge、reasoning、multi_language、specialized_knowledge、traceability、outputformatting、internal_security、external_security`。用户需要根据当前测试用例组的类别设置对应的`field`。    


`prompt`列表用于存储当前测试用例组的所有测试用例，每一个测试用例为字符串格式。在进行自动化测试的过程中，这些测试用例会作为问题提供给当前被测试的LLM。  

`evaluation`字典用于存储当前测试用例组的答案，字典的key从"0"开始，分别对应第1、2、3...条测试用例的答案，其中每一条测试用例的答案是一个列表，由于**当前工具箱仅用于测试单轮对话** ，所以这里的列表长度始终为1。列表的内部元素是一个字典，字典的key是评分方法，目前包括`keywords`、`blacklist`和`GPT4eval`三种，分别对应着三种不同的评分方法，字典的key对应的value是当前测试用例的该评分方法的 **关键字**。   
1. `keywords`：根据LLM的回答是否含有字典里`"keywords"`对应的列表中给出的 **关键字** 评分。  
2. `blacklist`：根据LLM的回答是否含有字典里`"blacklist"`对应的列表中给出的 **黑名单字符串** 评分。  
3. `GPT4eval`：让 **GPT4** 对该LLM对于该条测试用例的回答打分， `"GPT4eval"`对应的value始终为示范中的`[[True]]`。  

以上方法如果出现在字典中，该条测试用例就会用该方法进行打分，对于所有的评分方法，每一条测试用例的 **分数范围** 都为 **0-1** 。  
  
按照以上`json`格式创建测试用例组，并在某个文件夹（这里假设该文件夹的绝对路径为：`/home/ubuntu/LLMs/czy/GreatLibrarian/Testcase`）中**新建`json`文件**（这里假设为`example1.json`），然后将测试用例组写进文件内，支持将多个`json`文件放入至同一文件夹中用于一次测试。
 

#### 评分规则配置

除了测试用例配置中提到的 `evaluation` 字典，工具箱的评分过程中还可以进行更具体的 **评分规则配置**。

在使用 `evaluation` 字典评分的过程中，使用字典中的每个方法打分后，用户可以选用一个分数结算方法 `FinalScore` ，用于根据所有评分方法的打分给该条测试用确定一个最终得分。  

目前工具箱中有一个默认的 `FinalScore` 方法，如果用户使用该默认方法，则不需要对配置文件`register_usr.py`作出任何改动   

如果用户需要自定义分数结算方法，需要在`register_usr.py`中创建一个新的`FinalScore`的子类，类中包含三种方法，其中 `__init__` 和 `final_score_info` 为 **固定配置** ，无需修改，用户需要自己定义。用户需要定义 `get_final_score` 方法，该方法利用 `self.score` 来计算 `final score` 并返回一个浮点数作为该条测试用例的最终得分。其中 `self.score` 是一个字典，字典内容格式如下所示： `{'keywords':0.5,'blacklist':1,'GPT4eval':1}` 。该字典的 **key为评分方法的字符串** ， **value为该方法对应的得分**。  
  
    from greatlibrarian.Core import FinalScore
    from greatlibrarian.Configs import ExampleConfig
    from greatlibrarian.Utils import Registry

    class FinalScore2 (FinalScore):
         def __init__(self, score_dict,field,threadnum) -> None:
            self.score = score_dict
            self.field = field
            self.threadnum = threadnum

         def get_final_score(self) -> int :
            """

            Used to define the final scoring calculation rules for each testcase.
            The final score is calculated based on the scores from various evalmethods through this rule to obtain the ultimate score.

            """
            if self.score.get('blacklist') is not None and self.score['blacklist'] == 0.0 :
                return(0.0)
            if self.score.get('keywords') is not None and self.score.get('GPT4_eval') is not None:
                if abs(self.score['keywords']-self.score['GPT4_eval']) <= 0.5:
                    return(float('%.3f'%((self.score['keywords']+self.score['GPT4_eval'])/2)))
                else:
                    return('Human Evaluation')
            if self.score.get('keywords') is not None :
                return(self.score['keywords'])
            if self.score.get('GPT4_eval') is not None:
                return(self.score['GPT4_eval'])

         def final_score_info(self) -> str:
         return (self.get_final_score(),f'The final score of this testcase is {self.get_final_score()}, in {self.field} field.'+f'from thread {self.threadnum}',self.get_final_score())  

创建完新的`FinalScore`子类（假设为`FinalScore2`）后，需要同步修改ExampleConfig实例的初始化：  
  
`config = ExampleConfig(qw,FinalScore1) `

  

除了最终得分的计算规则外，用户还可以选择或自定义每一种评价方法（`keywords、blacklist、GPT4eval`）的 **评分细则** 。  

对于一条测试用例（prompt）以及同样的答案（`evaluation`字典）来说，可以因为`evaluation`字典字典中每个评分方法的不同 **评分细则** 而获得不同的得分。

比如：对于一个回答“是的，**中国**是一个和谐富强的国家。”，答案中的`keywords`设置为：['中国','亚洲']，此时工具箱中对于`keywords`这个评价方法有两种评分细则，分别如下：   

1. 对于`keywords`中的n个关键字，LLM的回答中 **包含n个中的任意一个就可以获得满分（1分）** 。  
2. 对于`keywords`中的n个关键字，LLM的回答中 **每包含一个关键字，LLM就可以获得1/n分** 。  

对于评分细则1，上述回答得分为1分；对于评分细则2，上述回答得分为0.5分。  

在工具箱中，目前每种 **评价方法** 都至少有一种 **评分细则** ，定义于[EvalMethods](https://github.com/JerryMazeyu/GreatLibrarian/tree/main/greatlibrarian/EvalMethods)中方法名称对应的py文件中，如果使用工具箱中已经定义的评分细则，只需要在工具箱 **开始自动化测评前** 根据提示输入评分细则的序号，即可完成每种评价方法对应的评分细则的选用；若用户需要 **新增评分细则** ，需要在[EvalMethods](https://github.com/JerryMazeyu/GreatLibrarian/tree/main/greatlibrarian/EvalMethods)中方法名称对应的py文件中的评价方法类中新建方法，方法名称为“eval+序号”，该方法要求通过 `self.evalinfo` （一个key为评价方法字符串，对应的value为评价方法关键字列表的字典，如上文中提到的"`evaluation`"）、 `self.prompt` (本条测试用例的问题）以及 `self.ans` （LLM的回答）来评判本条测试用例，并返回评分（浮点数）。  
  
        class Keyword(EvalMethods):
            def eval1(self):
            """
            A method for scoring models based on keywords.
            Rule:For each propmt, the model's response that contains at least one of the keywords gets a score of 1/n, and n is the number of prompts.
            Returns:Score of the model.

            """
            score = 0.0
            keywords = self.evalinfo['keywords']
            keywords = to_list(keywords)
            for ind, pt in enumerate(self.prompt):
                if self.if_there_is(self.ans[ind], self.keywords[ind]):
                    score += 1 / len(self.prompt)
            return score

**注意：在用户在某个评价方法类中新增了评分细则后，需要更新类中的`self.methodtotal`为目前的eval方法数量，以保证选择评分细则功能的鲁棒性。**  
  
    class Keyword(EvalMethods):
        def __init__(self, prompt, ans, evalinfo,field,threadnum):
            self.methodtotal=2
  
### 自动化测评  
   
做好所有测前配置后，工具箱可以开始进行自动化的测评。测评的过程主要包括三个工作： 
 
1. **自动的与当前测试的LLM进行交互**。工具箱会将所有需要用于测试的`json`文件中的prompt通过`API Key`发送给LLM，然后接收并记录LLM的回应。在本工具箱中，此过程做了并行化处理，提高了交互的效率。
2. **根据`json`文件中提供的`evaluation`进行评分**。对于每一条测试用例，工具箱会首先使用`evaluation`中的所有评价方法评分，然后根据用户选择的`FinalScore`方法进行最终分数的评判。
3. **记录交互日志**。对于每一条测试用例，工具箱都会记录其交互的记录，记录的具体内容如下：  

>2023-11-10 16:03:18 - INFO - ---------- New Epoch ---------- from thread 2  
>2023-11-10 16:03:18 - INFO - To LLM:	 “技术创新”的完整概念，是指对新技术的研究开发以及 （  ） A. 产品化与信息化过程 B. 信息化与商品化过程 C. 商品化与专利化过程 D. 产品化与商品化过程 from thread 2  
>2023-11-10 16:03:22 - INFO - To User:	 “技术创新”的完整概念，是指对新技术的研究开发以及产品化和商品化过程。这意味着技术创新不仅仅是开发新技术，还包括将这些技术转化为实际的产品或服务，并推向市场实现其商业价值。因此，答案选择D. 产品化与商品化过程。 from thread 2  
>2023-11-10 16:03:22 - INFO - keyword:Dfrom thread 2  
>2023-11-10 16:03:22 - INFO - The model gets 1.0 points in this testcase by keywords method, in common_knowledge field.from thread 2  
>2023-11-10 16:03:22 - INFO - The final score of this testcase is 1.0, in common_knowledge field.from thread 2   

日志中的**To LLM:**后记录的是本次对话所使用的**问题（prompt）** ；**To User:**后记录的是LLM对于该条问题（prompt）的**回答**；  **keyword:D**指的是该回答包含了 **keywords**评价方法中的 **关键字“D”**；最后两行内容是**本条测试用例的得分信息以及问题的领域**。  
  
**由于并行会导致日志记录顺序的混乱，我们在工具箱中选择先生成初始日志`dialog_init.log`，然后根据线程号来整理日志，生成一个有序且只包含有用信息（问题、答案、评分信息及问题领域、评分依据等）。上述日志段落中，每句话结尾的“from thread 2”是为了方便整理日志所添加，正式日志`dialog.log`中不会包含该信息。**  
  
以下是一段`dialog.log`中的日志信息：
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:52 - INFO - ---------- New Epoch ----------  
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:52 - INFO - To LLM:	 我国面积最大的平原：  
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:55 - INFO - To User:	 我国面积最大的平原是东北平原。东北平原位于中国东北部，面积约35万平方公里，是东北地区的重要粮仓和工业基地。  
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:55 - INFO - keyword:东北平原  
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:55 - INFO - The model gets 1.0 points in this testcase by keywords method, in common_knowledge field.  
>2023-11-10 17:07:01 - INFO - 2023-11-10 16:55:55 - INFO - The final score of this testcase is 1.0, in common_knowledge field.   
  
*****  
  
### 评分规则  
  
评分规则的配置在前文介绍-评分规则配置中已经阐述，这里主要介绍当前`GPT4eval`方法以及工具箱内默认使用的评价方法和评分细则。  
  
1. `keywords`：主要使用`eval1`方法，具体的评分细则为： **当LLM的回答包含`keywords`列表中至少一个关键字时，LLM在本条测试用例中获得1分，否则获得0分**。
2. `blacklist`：主要使用`eval1`方法，具体的评分细则为：**当LLM的回答包含`blacklist`列表中的任何一个黑名单字符串时，LLM在本条测试用例中获得0分，否则获得1分**。
3. `GPT4eval`：由于需要调用另一个LLM对当前测试用例进行评分，所以同样需要调用`API Key`。由于目前我们没有GPT4的`API Key`，所以暂时用了其他LLM进行替代，这里调用LLM的逻辑与上文提到的调用被测评的LLM的逻辑完全一致，可以参考上文介绍-测前准备-APIkey配置进行LLM的新增，并在[GPT4Eval](https://github.com/JerryMazeyu/GreatLibrarian/blob/main/greatlibrarian/EvalMethods/gpt4Eval.py#L14)中对`self.llm`进行赋值。若需要改变`eval`方法，可以对[GPT4Eval-eval1](https://github.com/JerryMazeyu/GreatLibrarian/blob/main/greatlibrarian/EvalMethods/gpt4Eval.py#L29)方法进行改进，并新增`eval`方法在该类中，**然后更新`self.methodtotal`为最新的`eval`方法的数量**。        
      
      
  
        class Keyword(EvalMethods):   

            def __init__(self, prompt, ans, evalinfo,field,threadnum):  
                self.methodtotal=2    

            def eval1(self):
               """
               A method for scoring models based on keywords.
               Rule:For each propmt, the model's response that contains at least one of the keywords gets a score of 1/n, and n is the number of prompts.
               Returns:Score of the model.

               """
               score = 0.0
               keywords = self.evalinfo['keywords']
               keywords = to_list(keywords)
               for ind, pt in enumerate(self.prompt):
                   if self.if_there_is(self.ans[ind], self.keywords[ind]):
                       score += 1 / len(self.prompt)
               return score
            def eval2(self):
                """
                A method for scoring models based on keywords.
                Rule:For each prompt, the model gets a score of 1/n for each keyword included in the response, and n is the number of key words.
                Returns:Score of the model.

                """
               score=0.0
                keywords = self.evalinfo['keywords']
                keywords = to_list(keywords)
                for ind, pt in enumerate(self.prompt):
                  for k in keywords[ind]:
                     if self.ans[ind].find(k)!=-1:
                          score += 1 / (len(self.keywords[ind])*len(self.prompt))
                          print(f'keywords:{k}'+f'from thread {self.threadnum}')
                return(score)
  

4. `FinalScore`：主要使用`finalscore1`，具体的评分细则为：  
①首先判断`blacklist`评分是否为0，若为0则最终得分直接为0；  
②然后判断`keywords`评分，若无`GPT4eval`则最终得分等于`keywords`评分；  
③若有`GPT4eval`，则计算`keywords`评分与`GPT4eval`评分的差，若差的绝对值大于0.5则输出"Human Evaluation"，将该条测试用例记录进`human_evaluation.log`中，用于后续进行人工测评；若差的绝对值小于0.5，则取两者的均值作为最终得分。  
  
*****  

### 报告生成
  
前三条工作结束后，工具箱会根据测评所得到的分数信息以及测试用例的数据来生成测评报告。测评报告一共有四个模块，分别为**背景介绍、测试用例数据介绍、错误测试用例展示、各领域正确率对比**。  
  
以下是报告内容的展示（**该报告中的测试样例可能出现错误，仅用于展示报告内容**）
  
![pidEwMF.png](https://z1.ax1x.com/2023/11/22/pidEwMF.png)
![pidEhse.png](https://z1.ax1x.com/2023/11/22/pidEhse.png)
![pidEodA.png](https://z1.ax1x.com/2023/11/22/pidEodA.png)
![pidETII.png](https://z1.ax1x.com/2023/11/22/pidETII.png)
*****  

## 安装  

首先在本地安装poetry：  
Linux, macOS, Windows (WSL)：  
  
`curl -sSL https://install.python-poetry.org | python3 -`   
   
Windows (Powershell)：  
  
`(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`

在终端运行以下命令：  

`git clone https://github.com/JerryMazeyu/GreatLibrarian.git`
    
## 快速开始  
在终端运行以下命令完成环境配置：  

    cd GreatLibrarian  
    conda create --name GL python=3.10
    conda activate GL
    poetry install

运行以下命令：`gltest --testcase_path=/path/to/your/testcases/ --config_path=/path/to/your/config_file/`  

在这里，我们假设本次测试的测试用例存放在目录/home/ubuntu/LLMs/czy/GreatLibrarian/Testcase下，配置文件的绝对路径为：/home/ubuntu/LLMs/czy/GreatLibrarian/register_usr.py，则用如下命令启动自动测评：  
  
`gltest --testcase_path=/home/ubuntu/LLMs/czy/GreatLibrarian/Testcase --config_path=/home/ubuntu/LLMs/czy/GreatLibrarian/register_usr.py`  
  
然后工具箱会提示用户进行每种评价方法下的评分细则的选择，需要用户**根据提示信息输入评分细则序号**。  
  
选择完成后开始自动化评测，评测结束后的所有相关文件（log文件，测试报告等）记录在`GreatLibrarian/Logs`中。