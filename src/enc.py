import tenseal as ts
import pandas as pd
import os
import pickle
#need to change: row8 path, 18-21 Col1_name, Col2_name
#df = pd.read_csv('/home/hao/Documents/InfoSecurity/PrivProtecter/Example/MedicalDataAnalysis/diabetes.csv')
df = pd.read_csv('/home/ys/Documents/PrivProtecter/PrivGuard/src/01.csv')

context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
context.global_scale = 2**40
context.generate_galois_keys() 
encrypted_data = {}

with open('context.bin', 'wb') as f:
    f.write(context.serialize(save_secret_key=True))  
encrypted_data = {}
encrypted_data['col1'] = ts.ckks_vector(context, df['DEPOSIT'].values.tolist())

encrypted_data['col2'] = ts.ckks_vector(context, df['PROFIT'].values.tolist())



with open('col1.bin', 'wb') as f:
   f.write(encrypted_data['col1'].serialize())
with open('col2.bin', 'wb') as f:
   f.write(encrypted_data['col2'].serialize())

   

