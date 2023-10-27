import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# 示例数据
labels = ['A', 'B', 'C', 'D', 'E']
sizes = [10, 20, 15, 5, 30]

# 创建一个PDF文件对象
pdf_pages = PdfPages("pie_chart_with_default_colors.pdf")

# 生成饼状图
plt.figure(figsize=(8, 8))
patches, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Percentage of Categories")
plt.axis('equal')

# 创建图例，放在右侧
legend_labels = ['{} - {}'.format(label, sizes[i]) for i, label in enumerate(labels)]
legend = plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

# 调整图例的标签颜色
for text, patch in zip(legend.get_texts(), patches):
    text.set_color(patch.get_facecolor())

# 保存饼状图到PDF
pdf_pages.savefig()

# 关闭PDF文件
pdf_pages.close()

print("PDF文件 'pie_chart_with_default_colors.pdf' 已生成。")
