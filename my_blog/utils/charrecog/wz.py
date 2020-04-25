from aip import AipOcr,AipBodyAnalysis
import re

""" 你的 APP_ID AK SK """
APP_ID = '18563771'
API_KEY = 'NubbFniqHspWvvmFhqpGsDyd'
SECRET_KEY = 'Dsmazo13qnjulpeYnowwd6GeVFcZrapK'



# 文字提取
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# """ 读取图片 """
#
# with open(r"wztp.jpg", 'rb') as fp:
#     image = fp.read()
#
# """ 调用通用文字识别, 图片参数为本地图片 """
# data = client.basicGeneral(image)
#
#
# # 数据处理
# res = data['words_result']
# res_num = data['words_result_num']
# print("结果数量：{}".format(res_num))
# for r in res:
#     print(r['words'])


# 人体分析
# client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
#
# """ 读取图片 """
#
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
# image = get_file_content('examples.jpg')
#
# """ 调用人体检测与属性识别 """
# client.bodyAttr(image);
#
# """ 如果有可选参数 """
#
# options = {}
#
# options["type"] = "gender,age"
#
# """ 带参数调用人体检测与属性识别 """
# res = client.bodyAttr(image, options)
#
# print(res)


