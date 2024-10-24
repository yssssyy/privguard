import tenseal as ts
import pandas as pd
import time
#no need to change
def run():

    with open('context.bin', 'rb') as f:
        context_data = f.read()
    context = ts.context_from(context_data)

    encrypted_data = {}
    col1 = None
    col2 = None
    with open('col1.bin', 'rb') as f:
        col1 = f.read()  
    with open('col2.bin', 'rb') as f:
        col2 = f.read()

    # 反序列化加密向量
    col1_enc = ts.ckks_vector_from(context, col1)
    col2_enc = ts.ckks_vector_from(context, col2)
    
    add_result = col1_enc + col2_enc
    mult_result = col1_enc * col2_enc
    with open('add_result.bin', 'wb') as f:
        f.write(add_result.serialize())
    with open('mult_result.bin', 'wb') as f:
        f.write(mult_result.serialize())
    return add_result, mult_result

if __name__ == "__main__":
    start_time = time.time()
    add_result, mult_result = run()
    end_time = time.time()
    print("culculate time:", end_time - start_time, " second")
    #result = {'add_result': [add_result], 'mult_result': [mult_result]}
    #df = pd.DataFrame(result)
    #df.index.name = 'index'
    #df.reset_index(inplace=True)
    #df.to_csv('unencrypted_result.csv', index=False)

