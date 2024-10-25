## 추가할꺼 
# datatime, unixtimestamp 변환
# 

import os, json, shutil, re
from tqdm import tqdm
from glob import glob
import pandas as pd
import numpy as np
import os.path as osp
import open3d as o3d

def read_json(input_path):
    try:
        with open(input_path, 'r', encoding='utf-8')as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return e
    
def save_json(data, save_path):
    try:
        with open(save_path, 'w', encoding='utf-8')as save:
            json.dump(data, save_path, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
        return e
    
def change_json(data, key, target_values):
    data[f'{key}'] = target_values
    return data
    
def find_match_index_in_list(list_name, target_string):
    for index, sublist in enumerate(list_name):
        if target_string in sublist:
            return index
    return -1  # 특정 문자열을 찾지 못한 경우 -1을 반환

def save_pcd(src_path, dst_path, one_pcd):
    os.makedirs(osp.dirname(dst_path), exist_ok=True)
    try:
        shutil.copy(src_path, dst_path)
    except:
        print(src_path)

    o3d.io.write_point_cloud(dst_path, one_pcd)

def bin_to_pcd(bin_path):
    np_pcd = np.fromfile(bin_path, dtype=np.float32).reshape((-1, 4))
    np_pcd = np_pcd[:, :3]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np_pcd)
    return pcd

def aimmo_bin_to_pcd(src_path, dst_path):
    one_pcd = bin_to_pcd(src_path)
    save_pcd(src_path, dst_path, one_pcd)

def read_excel(excel_path):
    excel_pd = pd.read_excel(excel_path, encoding='utf-8')
    excel_pd = excel_pd.values.tolist()
    return excel_pd

def read_csv(csv_path):
    csv_pd = pd.read_csv(csv_path, encoding='utf-8')
    csv_pd = csv_pd.values.tolist()
    return csv_pd

def check_isfile(target_file_path):
    return os.path.isfile(target_file_path)

def check_isdir(target_dir_path):
    return os.path.isfile(target_dir_path)

def reverse_slash(win_path):
    return win_path.replace("\\","/")