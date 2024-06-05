"""
* 这里编写batch任务，调用zhipu api实现构建词云图
"""

from zhipuai import ZhipuAI

import logger
from utils import load_config

# TODO： 命令行交互
# & 填写zhipu ai的api key 在config.json中
config = load_config()
APIKEY = config['zhipu_API_KEY']

# ! 存在问题，使用test_comment?.jsonl 传入会报错，还未解决，这个点待后续解决，我向官方提了问题，但未得到结果，其返回的报错原因不够清晰

# 上传文件 - 创建Batch任务 - 获取结果
def batch_task(api_key:str):
    client = ZhipuAI(api_key=api_key)
    # 上传文件，获取id
    # ! 注意，这里的路径要和data2jsonl存入的文件路径一致
    result = client.files.create(
        file=open(file='test_comment3.jsonl', mode='rb'),
        purpose="batch"
    )
    
    # 创建任务
    create = client.batches.create(
        input_file_id=result.id,
        endpoint="/v4/chat/completions",
        completion_window="24h", # & 只有这个选项，会非常慢，得排队，测试结果过了一个晚上完成
        metadata={
            "description": "Sentiment analysis on movie reviews",
        }
    )
    print(create)

    batch_job = client.batches.retrieve(create.id)

    # ? 在这里处理异常是否合适
    """ 
    log = logger.init_logger()
    log2 = logger.init_console_logger()
    if batch_job.status == "completed":
        # 下载结果
        content = client.files.content(batch_job.output_file_id)
        content.write_to_file("output.jsonl")
        log.info(f"Batch job completed. Results saved to output.jsonl")
    elif batch_job.status == "in_progress":
        log.info(f"Batch job is in progress. Please wait.....(withing 24h)")
    elif batch_job.status == "failed":
        log2.error(f"Batch job failed: 文件未通过验证")
    elif batch_job.status == "expired":
        log2.debug(f"Batch job expired: Batch任务未在24小时内完成")
     """

    return batch_job

def batch_download(api_key:str, batch_id:str):
    client = ZhipuAI(api_key)
    # 下载结果
    content = client.files.content(batch_id)
    content.write_to_file("output.jsonl")
    return "FINISHED"

# TEST 直接在这里调用进行测试
#batch = batch_task(APIKEY)
#print(batch.status)
        

    