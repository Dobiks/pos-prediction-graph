from randomize import randomize
from transformation_utils import get_rotation, get_rotation_nn
from sklearn.metrics import mean_absolute_error
import pandas as pd

def main():
    static = pd.read_csv('static_graph.csv')
    gt_l = []
    nn_l = []
    for i in range(20):
        gt = randomize()
        detected = pd.read_csv('randomized_graph.csv')
        nn_val = get_rotation_nn(static, detected)
        gt_l.append(gt)
        nn_l.append(nn_val)
    print('Mean absolute error:', mean_absolute_error(gt_l, nn_l))
        

if __name__ == '__main__':
    main()