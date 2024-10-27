# chat-gpt2-middle-124M 参数1.24亿

config_s = {
    "vocab_size": 50257,  # 词汇表大小
    "context_length": 256,  # 上下文长度
    "emb_dim": 768,     # 编码维度
    "n_heads": 12,  # 多头注意力头数
    "n_layers": 12,     # 编码器层数
    "drop_rate": 0.1,   # dropout
    "qkv_bias": False   # qkv矩阵的偏置值
}

config_m = {
    "vocab_size": 50257,  # 词汇表大小
    "context_length": 1024,  # 上下文长度
    "emb_dim": 768,     # 编码维度
    "n_heads": 24,  # 多头注意力头数
    "n_layers": 24,     # 编码器层数
    "drop_rate": 0.1,   # dropout
    "qkv_bias": False   # qkv矩阵的偏置值
}

config_l = {
    "vocab_size": 50257,  # 词汇表大小
    "context_length": 1024,  # 上下文长度
    "emb_dim": 1024,     # 编码维度
    "n_heads": 32,  # 多头注意力头数
    "n_layers": 32,     # 编码器层数
    "drop_rate": 0.1,   # dropout
    "qkv_bias": False   # qkv矩阵的偏置值
}
