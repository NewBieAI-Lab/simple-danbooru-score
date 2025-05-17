## Danbooru美学评分

一个小的脚本，用来给d站对应id的图片评分。一天时间写出来的，bug估计有点多。

左上角可以输入图片id，点击右边的跳转按钮跳转到对应图片，如果已经评分中间的评分栏会显示分数，如果没有则显示未评分。评分储存在根目录下的image_scores.csv中，**程序运行期间请不要动这个文件。**

点击对应的分数按钮就可以记录评分、并跳转到下一张图片。

如果出现“图片不存在或代理问题”，有两种可能：一是你处在国内没有挂代理，二是d站已经删掉了这张图片（但是图片id还在）。这种情况点下一张就可以了。



## 安装

* 去官网安装Python10

* 打开命令行，输入以下命令安装依赖

  ```bash
  pip install gradio requests pandas
  ```

  

## 启动

在项目文件夹下打开命令行，输入

```bash
python main.py
```

 一定注意：在启动时**关闭代理**，一直到出现

```
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://bfb5e50a91ed4384d9.gradio.live

This share link expires in 1 week. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)
```

才能开启代理。然后**开启代理**访问两个URL中的其中一个。也就是说你要在启动时关闭代理，启动完成后开启代理。

