import pandas as pd
import os
import json

# 使用目前資料夾為路徑
folder_path = "."

csv_files = [
    "有尾目山椒魚科.csv",
    "無尾目叉舌蛙科.csv",
    "無尾目林蛙科赤蛙類.csv",
    "無尾目狹口蛙科.csv",
    "無尾目樹蛙科.csv",
    "無尾目蟾蜍科.csv",
    "無尾目蟾科.csv"
]

species = []

for file in csv_files:
    path = os.path.join(folder_path, file)
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    name_col = "學名" if "學名" in df.columns else df.columns[1]
    species += df[name_col].dropna().astype(str).str.strip().tolist()

# 去除重複並排序
species = sorted(set(species))

# 包成 JSON 格式
output_data = [{"sourceScientificName": name} for name in species]

# 輸出 JSON
output_path = os.path.join(folder_path, "tbia_Amphibious_nocturnal_list.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"✅ 已輸出：{output_path}")
