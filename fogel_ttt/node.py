
class NetNode():
    def __init__(self, num, act_func, bias=False):
        self.num = num
        self.act_func = act_func
        self.info_from = []
        self.info_to = []
        self.bias = bias
        self.input_val = None
        self.output_val = None

    def set_vals(self, input_val):
        self.input_val = input_val
        self.output_val = self.act_func(input_val)