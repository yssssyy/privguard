import tenseal as ts
import pandas as pd

def run():
    # 读取序列化的上下文
    with open('context.bin', 'rb') as f:
        context_data = f.read()
    
    context = ts.context_from(context_data)
    
    # 读取序列化的加密数据
    with open('add_result.bin', 'rb') as f:
        add_e = f.read()  # 读取加法结果
    with open('mult_result.bin', 'rb') as f:
        mul_e = f.read()  # 读取乘法结果
    
    return add_e, mul_e, context

def decrypt_result(encrypted_bytes, context):
    # 反序列化加密向量并解密
    encrypted_result = ts.ckks_vector_from(context, encrypted_bytes)
    decrypted_result = encrypted_result.decrypt()
    return decrypted_result

if __name__ == "__main__":
    add_e, mul_e, context = run()
    decrypted_add_result = decrypt_result(add_e, context)
    decrypted_mult_result = decrypt_result(mul_e, context)

    dec_result = {'decrypted_mult_result': decrypted_mult_result}
    df = pd.DataFrame(dec_result)
    df.index.name = 'index'
    df.reset_index(inplace=True)
    df.to_csv('result.csv', index=False)


