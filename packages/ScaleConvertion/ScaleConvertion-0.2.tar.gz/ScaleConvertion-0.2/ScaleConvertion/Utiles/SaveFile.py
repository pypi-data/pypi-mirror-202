# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 19:18
# @Author  : qxcnwu
# @FileName: SaveFile.py
# @Software: PyCharm
import os
from typing import List

import numpy as np
import pandas as pd
import qt5_applications
from matplotlib import pyplot as plt

dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

def save_csv(refs: List[np.array], altitudes: List[float], save_dir: str):
    """
    save ref to csv
    :param refs:
    :param altitudes:
    :param save_dir:
    :return:
    """
    for ref, alt in zip(refs, altitudes):
        pd.DataFrame(np.mean(ref, axis=1)).to_csv(os.path.join(save_dir, str(alt) + ".csv"))
        plt.plot(np.mean(ref, axis=1), label=str(alt))
    plt.legend()
    plt.show()
    return
