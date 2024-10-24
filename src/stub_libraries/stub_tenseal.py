from blackbox import Blackbox
class SCHEME_TYPE:
    CKKS = "CKKS"

class context:
    def __init__(self, scheme_type, poly_modulus_degree, coeff_mod_bit_sizes):
        self.scheme_type = scheme_type
        self.poly_modulus_degree = poly_modulus_degree
        self.coeff_mod_bit_sizes = coeff_mod_bit_sizes

class ckks_tensor:
    def __init__(self, context=None, ciphertexts=None):
        self.context=context
        if ciphertexts is not None:
            self.policy = ciphertexts.policy
        else:
            self.policy = None
    def __str__(self):
        return str(self.policy)
    __repr__ = __str__
    def __add__(self, other):
        if isinstance(other, ckks_tensor):
            ans=ckks_tensor()
            #ans.ciphertexts+=other.ciphertexts
            ans.policy = self.policy.join(other.policy)

            return  ans
        else:
            raise ValueError("Addition only supported with another ckks_tensor.")

    def __mul__(self, other):
        if isinstance(other, ckks_tensor):
            ans=ckks_tensor()
            ans.policy = self.policy.join(other.policy)
            return ans
        else:
            raise ValueError("Multiplication only supported with another ckks_tensor.")
