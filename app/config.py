import os

class Config:
    # 从环境变量中读取 MongoDB URI 或使用默认值
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ooc')

# 其他配置项
