"""
布里斯托大便分類法規則引擎。

依據大便形狀（Bristol Stool Scale Type 1-7）與顏色等屬性提供健康狀態評估與警示。
"""

BRISTOL_TYPES = {
    1: {
        "status": "嚴重便秘",
        "description": "一顆顆硬硬的球狀，像堅果一樣，非常難排出。",
        "suggestion": "水分極度匱乏！請立刻補充大量水分，多攝取水溶性膳食纖維，必要時請諮詢醫師。"
    },
    2: {
        "status": "輕微便秘",
        "description": "香腸狀，但表面凹凸不平、呈塊狀凹陷。",
        "suggestion": "水分與膳食纖維攝取不足。請增加日常飲水量，多吃蔬菜水果與全穀類食物。"
    },
    3: {
        "status": "正常/理想",
        "description": "香腸狀，但表面有裂痕。容易排出。",
        "suggestion": "這是正常的便便狀態！請繼續維持均衡的飲食與良好的作息習慣。"
    },
    4: {
        "status": "最完美/健康",
        "description": "像香腸或蛇一樣，表面光滑且柔軟。非常容易排出。",
        "suggestion": "最理想的黃金便便！您的腸胃非常健康，請繼續保持目前的飲食與生活形態。"
    },
    5: {
        "status": "纖維不足",
        "description": "斷裂成一塊塊質地柔軟的斑塊，邊緣切口整齊。容易排出。",
        "suggestion": "雖然好排出，但代表膳食纖維稍有不足。建議多攝取非水溶性纖維（如麥麩、蔬菜）來幫助便便成形。"
    },
    6: {
        "status": "輕微腹瀉",
        "description": "粗糙分散的糊狀塊，糊糊爛爛的。邊緣呈不規則撕裂狀。",
        "suggestion": "腸道可能輕微發炎、消化不良或菌群失調。建議飲食清淡，暫時避免油膩與辛辣刺激性食物。"
    },
    7: {
        "status": "嚴重腹瀉",
        "description": "水狀、無固體顆粒，完全是液體狀態。",
        "suggestion": "嚴重腹瀉！請注意補充水分與電解質以防脫水。若持續超過兩天或伴隨發燒、腹痛，請立即就醫。"
    }
}

COLOR_GUIDE = {
    "brown": {
        "name": "棕色 / 黃褐色",
        "health_msg": "正常顏色。膽汁混合食物消化後的健康顏色。"
    },
    "yellow": {
        "name": "黃色",
        "health_msg": "可能表示油脂吸收不良，或是腸道蠕動過快。若持續黃色且油黏，請多加留意。"
    },
    "green": {
        "name": "綠色",
        "health_msg": "可能是攝取了大量綠色蔬菜，或食物通過腸道速度太快，膽汁來不及分解。通常為暫時現象。"
    },
    "black": {
        "name": "黑色 (柏油狀)",
        "health_msg": "警告：可能是上消化道出血（如胃出血、十二指腸潰瘍）。若非服用鐵劑或特定食物（如墨魚汁），建議就醫檢查。"
    },
    "red": {
        "name": "紅色 / 帶血",
        "health_msg": "警告：可能是下消化道出血（如痔瘡、肛裂或腸道腫瘤）。若持續有血便，請務必立即就醫檢查。"
    },
    "gray": {
        "name": "灰白色 / 陶土色",
        "health_msg": "警告：可能表示膽管阻塞，膽汁無法排入腸道。請儘速就醫檢查肝膽胰臟功能。"
    }
}

def analyze(log):
    """
    分析單次排便記錄。
    
    Args:
        log (PoopLog): 包含 bristol_type, color, odor, mood 等欄位的 PoopLog 物件。
        
    Returns:
        dict: 包含類型評估、顏色分析與綜合健康建議的字典。
    """
    bristol_type = int(log.bristol_type)
    color = log.color.lower()
    
    # 獲取布里斯托類型分析
    type_info = BRISTOL_TYPES.get(bristol_type, {
        "status": "未知狀態",
        "description": "無效的布里斯托類型編號。",
        "suggestion": "請重新輸入有效的 1 至 7 類型。"
    })
    
    # 獲取顏色分析
    color_info = COLOR_GUIDE.get(color, {
        "name": color,
        "health_msg": "此顏色較為罕見，請持續觀察是否與特定食物或藥物有關。"
    })
    
    # 綜合評估
    is_warning = bristol_type in [1, 7] or color in ['black', 'red', 'gray']
    
    return {
        "bristol_type": bristol_type,
        "status": type_info["status"],
        "description": type_info["description"],
        "bristol_suggestion": type_info["suggestion"],
        "color_name": color_info["name"],
        "color_analysis": color_info["health_msg"],
        "is_warning": is_warning
    }
