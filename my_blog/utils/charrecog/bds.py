from aip import AipOcr, AipImageCensor, AipBodyAnalysis

import re
class Bd(object):

    """
    加载配置
    """
    def __init__(self):
        self.APP_ID     = '18977718'
        self.API_KEY    = '6tRM8KoxjpnQ8a50KzH9UoG6'
        self.SECRET_KEY = 'AKf55VaXTS8G3WpeSc4VttGQ01HXcvey'

    # 文字识别
    def identity_word(self, image):
        """

        :param image: 传送一个本地的图片地址
        :return:
        """
        client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        """ 读取图片 """
        with open(image, 'rb') as file:
            """ 调用通用文字识别, 图片参数为本地图片 """
            data = client.basicGeneral(file.read())

            # 数据处理
            res = data['words_result']
            res_num = data['words_result_num']
            print("结果数量：{}".format(res_num))
            for r in res:
                print(r['words'])

    # 鉴别图片合法性
    def identity_picture(self, file_name, flag):
        """

        :param file_name: 一个网络图片的url， 或者一个本地图片的地址
        :param flag: 传送指定的参数‘url’ 或者  ‘local’
        :return:
        """
        s_client = AipImageCensor(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        if flag == 'local':
            with open(file_name, 'rb') as f:
                try:
                    res = s_client.imageCensorUserDefined(f.read())
                    print(res)
                except TypeError:
                    raise print("类型错误")

        elif flag == 'url':
            res = s_client.imageCensorUserDefined(file_name)
            print(res)

    # 人体数据分析
    def analyse_people(self, filePath):
        client = AipBodyAnalysis(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        """ 读取图片 """
        with open(filePath, 'rb') as fp:
            data = client.bodyAttr(fp.read())
            data = str(data)
            res = re.findall(r"'(.*?)': {'score': (0.\d+), 'name': '(.*?)'}", data, re.S)
            del res[0]
            for r in res:
                print("{:—<20}特征:{:—<15}精准度:{}".format(r[0],r[2], r[1]))
            """ 如果有可选参数 """


if __name__ == '__main__':
    bd = Bd()
    information = '街拍5.15.jpg'
    bd.identity_word(information)
    bd.identity_picture(information, 'local')
    bd.analyse_people(information)


