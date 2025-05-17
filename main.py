import gradio as gr
import requests
import tempfile
import csv
import os
import pandas as pd


# 在程序启动时读取CSV文件并存储在字典中
def load_scores():
    if os.path.exists('image_scores.csv'):
        df = pd.read_csv('image_scores.csv')
        if df.empty:
            scores = {}
        else:
            scores = {str(row['image_id']): row['score'] for _, row in df.iterrows()}
    else:
        scores = {}
    return scores

# 初始化评分数据
scores_data = load_scores()

# 获取Danbooru图片的URL
def fetch_danbooru_image(image_id):
    api_url = f"https://danbooru.donmai.us/posts/{image_id}.json"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("file_url")

            if image_url:
                return image_url
        
        return None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

# 下载图片到临时文件
def download_image_to_temp(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            with open(temp_file.name, 'wb') as file:
                file.write(response.content)
            return temp_file.name
        else:
            gr.Warning("图片加载失败，请检查网络或代理")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

# 显示图片
def show_image(image_id):
    if not image_id.strip():
        gr.Warning("无效的图片ID")
        return None

    try:
        image_id = int(image_id)
        image_url = fetch_danbooru_image(image_id)

        if image_url:
            temp_file_name = download_image_to_temp(image_url)
            return temp_file_name
        else:
            gr.Warning("图片不存在或代理问题")
            return None
    except ValueError:
        gr.Warning("图片ID必须是数字")
        return None

def show_score(image_id):
    if not image_id.strip():
        gr.Warning("无效的图片ID")
        return None
    image_score = scores_data.get((image_id), "未评分")
    return image_score

def show_image_and_score(image_id):
    score = show_score(image_id)
    return show_image(image_id), score

# 记录评分到字典和CSV文件
def record_score(image_id, score):
    print(f"Image {image_id} scored: {score}")
    scores_data[str(image_id)] = score  # 更新字典中的评分
    # 将字典写回CSV文件
    df = pd.DataFrame(list(scores_data.items()), columns=['image_id', 'score'])
    df.to_csv('image_scores.csv', index=False)
    gr.Info(f"Id为{image_id}的图片评分已更新为{score}")

# 跳转到下一张图片
def next_image(image_id):
    next_id = str(int(image_id) + 1)
    score = show_score(next_id)
    return show_image(next_id), next_id, score

# 跳转到上一张图片
def last_image(image_id):
    next_id = str(int(image_id) - 1)
    score = show_score(next_id)
    return show_image(next_id), next_id, score

# 中间函数，调用record_score和next_image
def handle_score_and_next(image_id, score):
    record_score(image_id, score)
    img, next_id, score_val = next_image(image_id)
    return img, next_id, score_val

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# danbooru图片美学评分")
    with gr.Row():
        image_id = gr.Textbox(label="图片ID", value="1")
        image_score = gr.Textbox(label="评分")
        jump_btn = gr.Button("跳转")
    output = gr.Image(label="图片", height=768)
    jump_btn.click(
        fn=show_image_and_score,
        inputs=image_id,
        outputs=[output, image_score]
    )

    # 添加评分按钮和跳转按钮
    with gr.Row():
        gr.Button("上一张").click(
            fn=last_image,
            inputs=image_id,
            outputs=[output, image_id, image_score]  # 确保输出包含图片、图片ID和评分
        )
        gr.Button("下一张").click(
            fn=next_image,
            inputs=image_id,
            outputs=[output, image_id, image_score]  # 确保输出包含图片、图片ID和评分
        )
    
    gr.Markdown("### 美学评分")
    with gr.Row():
        for score in [0, 2.5, 5, 7.5, 10]:
            gr.Button(str(score)).click(
                fn=lambda image_id, score=score: handle_score_and_next(image_id, score),
                inputs=image_id,
                outputs=[output, image_id, image_score],  # 这里要包含image_score
            )

demo.launch(share=True)