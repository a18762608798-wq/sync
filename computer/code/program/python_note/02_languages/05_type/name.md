# name

## decription

```python
num_qubits # 数量

qubit_idx # 下标

embedding_dim
seq_len # 序列长度
batch_size # batch 大小

is_training # 布尔变量
has_bias
use_cache

attention_weights
hidden_states
input_ids
output_logits
```

## get、set、load、save 要区分

- get_user(): 一般表示“获取已有对象”.

- load_model(): 更强调从文件、磁盘、数据库等外部资源读取.

- save_model(): 表示持久化.

- create_model(), build_model(): 表示创建新对象.
