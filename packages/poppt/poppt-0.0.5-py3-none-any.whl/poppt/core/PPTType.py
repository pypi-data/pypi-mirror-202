import os
import time
from pathlib import *

import win32com.client
from pofile import get_files
from poprogress import simple_progress

from poppt.lib.ppt.ppt2pdf_service import ppt2pdf_single


class MainPPT():

    def ppt2pdf(self, path, output_path):
        """
        @Author & Date  : CoderWanFeng 2022/5/9 23:34
        @Desc  : path:存放ppt的路径
        """
        # 如果是相对路径，转为绝对路径
        filenames = get_files(path)
        # for循环依次访问指定目录的所有文件名
        for filename in simple_progress(filenames):
            # 判断文件的类型，对所有的ppt文件进行处理(ppt文件以ppt或者pptx结尾的)
            if filename.endswith('ppt') or filename.endswith('pptx'):
                # print(filename)           # PPT素材1.pptx -> PPT素材1.pdf
                new_pdf_name = Path(filename).stem + '.pdf'  # PPT素材1.pdf
                # ppt文件的完整位置: C:/Users/Administrator/Desktop/PPT办公自动化/ppt/PPT素材1.pptx
                # filename = path + '/' + filename
                # pdf文件的完整位置: C:/Users/Administrator/Desktop/PPT办公自动化/ppt/PPT素材1.pdf
                output_pdf_filename = Path(output_path).absolute() / new_pdf_name
                # 将ppt转成pdf文件
                ppt2pdf_single(filename, str(output_pdf_filename))
                # time.sleep(3)

    def ppt2img(self, input_path, output_path, img_type):
        '''将PPT另存为图片格式
          arguments:
              pptFullName: 要转换的ppt文件，
              pptName：转换后的存放JPG文件的目录
              imgType: 图片类型
        '''
        # 启动PPT
        pptClient = win32com.client.Dispatch('PowerPoint.Application')
        # 设置为0表示后台运行，不显示，1则显示
        pptClient.Visible = False
        # 打开PPT文件
        ppt = pptClient.Presentations.Open(input_path)

        # 另存为图片
        # Python路径操作模块pathlib，看这篇就够了！ https://zhuanlan.zhihu.com/p/475661402
        output_dir = Path(output_path) / str(Path(input_path).stem)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # JPG是17
        img_type_jpg = 17
        # PNG是18
        img_type_png = 18
        if img_type == 'jpg':
            ppt.SaveAs(output_dir, img_type_jpg)
        else:
            ppt.SaveAs(output_dir, img_type_png)
        # 退出
        pptClient.Quit()
