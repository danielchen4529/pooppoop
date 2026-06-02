"""
綜合飲食與健康改善建議規則引擎。

分析使用者過去一段時間的排便記錄趨勢，給出客製化的飲食建議、飲水提醒與生活作息指引。
"""

from typing import List

def generate_suggestion(logs) -> dict:
    """
    根據使用者最近的排便紀錄趨勢，生成綜合飲食建議。
    
    Args:
        logs (list): PoopLog 物件的清單。
        
    Returns:
        dict: 包含建議摘要、主要趨勢、飲食建議、應避免食物與日常建議的字典。
    """
    if not logs or len(logs) < 3:
        return {
            "summary": "記錄不足",
            "trend": "資料收集階段",
            "content": "目前記錄筆數小於 3 筆，系統尚無法產出精準趨勢分析。請持續記錄您的每日排便狀況！",
            "dietary_recommendations": [],
            "avoid_foods": [],
            "lifestyle_tips": ["每天固定時間排便", "多走動以促進腸道蠕動"],
            "water_target": "2000ml"
        }
        
    # 計算各種類型的次數
    total = len(logs)
    constipation_count = 0
    diarrhea_count = 0
    normal_count = 0
    
    for log in logs:
        b_type = int(log.bristol_type)
        if b_type in [1, 2]:
            constipation_count += 1
        elif b_type in [3, 4, 5]:
            normal_count += 1
        elif b_type in [6, 7]:
            diarrhea_count += 1
            
    # 計算比例
    constipation_ratio = constipation_count / total
    diarrhea_ratio = diarrhea_count / total
    normal_ratio = normal_count / total
    
    # 決定主要趨勢與建議
    if constipation_ratio >= 0.4:
        summary = "便秘傾向警告"
        trend = "您的排便記錄顯示出較明顯的便秘傾向 (Type 1 或 2)。這通常與膳食纖維或水分不足有關。"
        dietary_recommendations = [
            "多攝取高纖食物：如燕麥、地瓜、糙米、黑豆、綠花椰菜、奇異果與蘋果。",
            "補充足夠的高品質油脂：適度補充橄欖油、酪梨油或堅果，有助於潤滑腸道。",
            "多喝水：建議每日飲水量提升至體重 (kg) x 35-40 ml。"
        ]
        avoid_foods = [
            "精製澱粉：白麵包、白米飯、蛋糕等，缺乏纖維且易吸水。",
            "高脂肪肉類與炸物：消化緩慢，會延長食物滯留腸道時間。",
            "過量咖啡因與酒精：具有利尿作用，反而可能使身體與大便脫水。"
        ]
        lifestyle_tips = [
            "每日早晨起床後喝一杯 300ml 溫開水，喚醒腸胃蠕動。",
            "多進行有氧運動，如慢跑、快走或腹部核心伸展，刺激腸道壁收縮。",
            "不要憋便：有便意時應立即如廁，可使用踏腳凳墊高雙腿呈 35 度角以利排便。"
        ]
        water_target = "2500ml"
        
    elif diarrhea_ratio >= 0.4:
        summary = "腹瀉/消化不良警示"
        trend = "您的排便記錄顯示出較明顯的腹瀉或糊狀便傾向 (Type 6 或 7)。這可能與腸道發炎、感染、菌群失調或特定食物不耐受有關。"
        dietary_recommendations = [
            "採用低渣飲食：白米粥、吐司、去皮雞肉、蒸蛋或熟香蕉，減輕腸胃負擔。",
            "補充電解質：腹瀉會流失大量水分與礦物質，可飲用稀釋運動飲料或椰子水。",
            "補充益生菌：適量補充優格（無糖）或益生菌產品，協助重建腸道健康菌群。"
        ]
        avoid_foods = [
            "乳製品：腹瀉期間小腸乳糖酶可能暫時減少，應避免牛奶、起司以防加劇拉肚子。",
            "高油高糖與辛辣刺激性食物：油炸食品、麻辣鍋、甜食會刺激腸黏膜，加劇蠕動。",
            "容易脹氣的食物：豆類、洋蔥、花椰菜、碳酸飲料。"
        ]
        lifestyle_tips = [
            "注意腹部保暖，避免吹風受涼。",
            "飲食改為少量多餐，細嚼慢嚥，避免暴飲暴食增加消化道負擔。",
            "保持充足睡眠，因為壓力與焦慮會透過「腦腸軸」引發腸道蠕動失調。"
        ]
        water_target = "2000ml (少量多次，並補充電解質)"
        
    else:
        summary = "黃金腸胃狀態"
        trend = "您的排便狀況非常均衡穩定！大部分的紀錄都處於最健康的黃金區間 (Type 3、4 或 5)。"
        dietary_recommendations = [
            "維持多樣化均衡飲食：每日攝取不同顏色的蔬菜與水果，補充多元植化素。",
            "攝取優質蛋白質與健康脂肪：魚肉、雞肉、豆腐、堅果與橄欖油。"
        ]
        avoid_foods = [
            "過度加工食品：泡麵、罐頭、零食等高鈉、多化學添加物的食品。",
            "過量含糖飲料與手搖飲：高果糖糖漿對腸道菌相有負面影響。"
        ]
        lifestyle_tips = [
            "繼續維持規律的運動習慣（每週至少 3 次，每次 30 分鐘）。",
            "保持規律的作息與充足睡眠，這能讓自主神經穩定，有助腸胃長久健康。"
        ]
        water_target = "2000ml"
        
    return {
        "summary": summary,
        "trend": trend,
        "dietary_recommendations": dietary_recommendations,
        "avoid_foods": avoid_foods,
        "lifestyle_tips": lifestyle_tips,
        "water_target": water_target
    }
