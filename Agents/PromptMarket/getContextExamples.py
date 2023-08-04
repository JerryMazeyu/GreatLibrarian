from Core import Agents
#import matplotlib.pyplot as pt

"提供针对性且有用的问题，预热大模型，使其能够更好地将大而泛"
"""设定大模型的身份，快速定位到该领域，能更专业地回答问题"""
"""相当于大模型的预热"""
def get_context_examples(self,knowledge_domain:str,concept:str,question=None)->list:
   self.knowledge_domain=knowledge_domain
   self.concept=concept
   self.question=question
   
   supported_knowledge_domain={"概率论","数理统计","大学物理","高等数学","生物"}
   supported_concept={
      "概率论":["概率密度","最大似然定理","随机变量"],
      "数理统计":["假设检验","卡方分布","回归分析"],
      "大学物理":["麦克斯韦方程组","牛顿定理","质能公式"],
      "高等数学":["微积分","格林公式","数列极限"],
      "生物":["遗传学","生态学","进化论"]
   }

   if knowledge_domain not in supported_knowledge_domain or concept not in supported_concept:
      return "该部分尚未收录"

   template=["作为{knowledge_domain}领域的专家，请对{concept}的概念进行详细解答。你的回答应该包括其起源、理论基础、公式推导、定理证明、应用要求等，以提供全面的理解。如果涉及公式，请用LaTeX表示。"
            #  "我需要你扮演一位大学的{knowledge_domain}讲师，我将给你一些关于{knowledge_domain}的细节。接下来希望你根据这些预设能够更好地回答概率论的问题。我的第一个问题是{question}。",
            #  "我希望你能像一名{knowledge_domain}老师一样，我将输入一个{knowledge_domain}问题或者知识点，你将根据我的输入的问题或知识点给出一个详细的解释，并根据涉及的知识点生成2个随机的问题。你不需要解释这些问题。",
            #  "我希望你充当一名{knowledge_domain}老师，我将提供一些{concept}的概念。你的工作是用易于理解的术语解释它们"
             ]
   
   formatted_string=template.__format__(knowledge_domain,concept,question or "概念")

   return [formatted_string]





# if domain=="概率论":
#         # 我接下来要给你一些概率论的预设，希望扮演一个概率论的学者，我希望你根据这些预设，能够更好的回答我的概率论的问题
#         return [
#            "贝叶斯定理用于在已知事件B发生的条件下，计算事件A发生的概率，计算公式为P(A|B)=P(B|A)*P(A)/P(B)",
#            ""
#         ]
# elif domain=="数理统计":
#         #Act as a statistician and respond in Chinese.
#         return [
#            "我需要你作为一名经验丰富的统计员，我将为你提供与数理统计有关的细节。你应该了解统计学术语、统计分布、置信区间、假设检验和统计图表",
#            ""
#         ]
# elif domain=="物理":
#         return [
#            "我希望你能像一个大学物理老师一样，我将输入一个数学问题或者知识点，你将根据我的输入的问题或知识点给出一个详细的解释，并根据涉及的知识点生成2个随机的问题。你不需要解释这些问题。",
#            ""
#         ]
# elif domain=="数学":
#         return [
#            ""
#         ]
# elif domain=="生物":
#         return [
           
#         ]
# else :
#         return ["该部分尚未收录！" ]
