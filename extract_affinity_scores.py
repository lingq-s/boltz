import json
import csv
import os
import glob

def extract_scores_from_folders(base_dir, mapping_file, output_csv):
    """
    从每个文件夹的JSON文件中提取分数，并根据映射文件转换为原始ID
    
    Args:
        base_dir: 包含所有编号文件夹的基目录
        mapping_file: id_mapping.csv文件路径
        output_csv: 输出CSV文件路径
    """
    
    # 读取映射文件，创建numeric_id到original_id的映射
    id_mapping = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_mapping[row['numeric_id']] = row['original_id']
    
    # 准备输出数据
    output_data = []
    
    # 查找所有四位编号的文件夹
    folders = glob.glob(os.path.join(base_dir, '[0-9][0-9][0-9][0-9]'))
    
    for folder_path in folders:
        folder_name = os.path.basename(folder_path)
        
        # 检查映射文件中是否存在这个numeric_id
        if folder_name not in id_mapping:
            print(f"警告: 文件夹 {folder_name} 在映射文件中未找到对应项，跳过")
            continue
        
        # 构建JSON文件路径
        json_file = os.path.join(folder_path, f"affinity_{folder_name}.json")
        
        # 检查JSON文件是否存在
        if not os.path.exists(json_file):
            print(f"警告: JSON文件 {json_file} 不存在，跳过")
            continue
        
        try:
            # 读取JSON文件
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # 提取所有分数
            scores = {
                'original_id': id_mapping[folder_name],
                'numeric_id': folder_name
            }
            
            # 添加所有以'affinity_'开头的字段
            for key, value in data.items():
                if key.startswith('affinity_'):
                    scores[key] = value
            
            output_data.append(scores)
            
        except Exception as e:
            print(f"错误: 处理文件夹 {folder_name} 时出错: {e}")
    
    # 写入CSV文件
    if output_data:
        # 获取所有字段名
        fieldnames = ['original_id', 'numeric_id']
        # 添加所有affinity字段（从第一个数据项中获取）
        for key in output_data[0].keys():
            if key not in fieldnames:
                fieldnames.append(key)
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_data)
        
        print(f"成功处理 {len(output_data)} 个文件夹的数据，结果已保存到 {output_csv}")
    else:
        print("未找到任何有效数据")

if __name__ == "__main__":
    # 配置参数
    base_directory = "boltz_results_7sxf/predictions"
    mapping_file_path = "7sxf_id_mapping.csv"
    output_csv_path = "2650_boltz2.csv"
    
    # 执行提取
    extract_scores_from_folders(base_directory, mapping_file_path, output_csv_path)
