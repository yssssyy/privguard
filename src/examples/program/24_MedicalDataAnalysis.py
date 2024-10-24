from os import path

def run(data_folder, **kwargs):
    #start_time = time.time()
    cross_validation = kwargs.get('cross_validation')
    metrics = kwargs.get('metrics')
    pd = kwargs.get('pandas')
    ts = kwargs.get('tenseal')
    # load data
    df_train = pd.read_csv(path.join(data_folder, 'data.csv'), schema=['DEPOSIT','PROFIT','name'])
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    col1_encrypted = ts.ckks_tensor(context, ciphertexts=df_train['name'].values)
    col2_encrypted = ts.ckks_tensor(context, ciphertexts=df_train['PROFIT'].values)
    addition_result = col1_encrypted + col2_encrypted
    multiplication_result = col1_encrypted * col2_encrypted
    #end_time = time.time()
    #print("analysis time:", end_time - start_time, " second")
    return addition_result, multiplication_result
