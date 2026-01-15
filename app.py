import streamlit as st
import pandas as pd

# --- 🛑 Layer 0: System Config (標題：台灣全島溫泉地圖) ---
st.set_page_config(
    page_title="三一協會：溫泉地圖", 
    page_icon="♨️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 📱 Mobile CSS (針對溫泉主題優化視覺) ---
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: "PingFang TC", "Microsoft JhengHei", sans-serif; }
    
    /* 卡片設計 - 溫泉暖色系 */
    .mobile-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #ffccbc; /* 淺橘色邊框 */
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.08);
        position: relative;
    }
    
    .recommend-badge {
        position: absolute; top: 0; right: 0;
        background-color: #FF5722; color: white; /* 深橘色 */
        padding: 6px 16px; border-radius: 0 16px 0 16px;
        font-weight: bold; font-size: 0.85rem;
    }
    
    .free-badge {
        position: absolute; top: 0; left: 0;
        background-color: #4CAF50; color: white; /* 綠色代表免費 */
        padding: 4px 12px; border-radius: 16px 0 16px 0;
        font-weight: bold; font-size: 0.8rem;
        z-index: 10;
    }
    
    .wild-badge {
        position: absolute; top: 0; left: 0;
        background-color: #5D4037; color: white; /* 深褐色代表野溪挑戰 */
        padding: 4px 12px; border-radius: 16px 0 16px 0;
        font-weight: bold; font-size: 0.8rem;
        z-index: 10;
    }

    .card-title { font-size: 1.4rem; font-weight: 800; color: #37474f; margin-bottom: 4px; }
    
    .nav-btn {
        display: block; width: 100%; text-align: center;
        background: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%); /* 溫泉橘漸層 */
        color: white !important; padding: 12px; border-radius: 12px;
        text-decoration: none; font-weight: bold; margin-top: 15px;
    }
    
    .tag { background-color: #eceff1; color: #455a64; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; margin-right: 5px; }
    
    /* 泉質與功效區塊 */
    .spring-info-box {
        background-color: #E3F2FD; /* 淡藍色水質感 */
        border-left: 5px solid #2196F3;
        padding: 10px 15px;
        margin-top: 10px;
        border-radius: 4px;
        color: #0D47A1;
        font-size: 0.95rem;
    }
    
    .price-tag {
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .price-0 { color: #2E7D32; background: #C8E6C9; } /* 免費 */
    .price-1 { color: #0277BD; background: #B3E5FC; } /* 百元 */
    .price-2 { color: #F57C00; background: #FFE0B2; } /* 千元 */
    .price-3 { color: #C2185B; background: #F8BBD0; } /* 奢華 */

    .stDataFrame { font-size: 1.1rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 🛑 Layer 1: The Massive Database (全國溫泉完整版) ---
# price_level: 0=免費, 1=百元(大眾), 2=千元(湯屋), 3=奢華
# difficulty: 1=開車即達, 3=需步行, 5=野溪健行, 8=攀岩拉繩, 10=特種部隊
data = [
    # ================= 北部 (12處) =================
    {
        "name": "北投溫泉 (地熱谷)", "region": "北部", "type": "青磺泉/白磺泉", 
        "ph": "PH 1-2 (強酸)", "benefit": "舒緩肌肉、皮膚病",
        "desc": "捷運可達，全台最方便的溫泉區，濃郁硫磺味。", 
        "price_level": 1, "price_desc": "💲 百元~千元皆有",
        "difficulty": 1, "diff_desc": "🟢 捷運直達", 
        "tags": ["捷運可達", "博物館", "日式風情"], "lat": 25.13, "lon": 121.50
    },
    {
        "name": "陽明山冷水坑", "region": "北部", "type": "弱酸性硫磺泉", 
        "ph": "PH 6", "benefit": "足湯、促進循環",
        "desc": "國家公園內的免費公共足湯與男/女裸湯。", 
        "price_level": 0, "price_desc": "🆓 完全免費",
        "difficulty": 2, "diff_desc": "🟢 需搭公車", 
        "tags": ["免費", "足湯", "需自備毛巾"], "lat": 25.16, "lon": 121.56
    },
    {
        "name": "金山萬里溫泉", "region": "北部", "type": "鐵泉/硫磺鹽泉", 
        "ph": "PH 5-6", "benefit": "保濕、婦女病",
        "desc": "以「海底溫泉」聞名，部分泉水帶有鹽分，金山總督溫泉為代表。", 
        "price_level": 1, "price_desc": "💲 百元 (公共池)",
        "difficulty": 1, "diff_desc": "🟢 開車/客運", 
        "tags": ["海底溫泉", "看海", "吃鴨肉"], "lat": 25.22, "lon": 121.64
    },
    {
        "name": "烏來溫泉", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7-8 (弱鹼)", "benefit": "美人湯、滋潤皮膚",
        "desc": "無色無味，泡完皮膚滑嫩，適合不喜歡硫磺味的人。", 
        "price_level": 2, "price_desc": "💲💲 景觀湯屋",
        "difficulty": 2, "diff_desc": "🟢 開車/客運", 
        "tags": ["美人湯", "老街美食", "台車"], "lat": 24.86, "lon": 121.55
    },
    {
        "name": "新竹秀巒野溪溫泉", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7", "benefit": "野趣、賞楓",
        "desc": "位於尖石鄉深山，需辦理入山證，秋季賞楓絕美。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 4, "diff_desc": "🟡 需步行下切", 
        "tags": ["野溪", "賞楓", "需辦入山證"], "lat": 24.62, "lon": 121.28
    },
    {
        "name": "新竹清泉溫泉", "region": "北部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7.5", "benefit": "歷史人文、關節",
        "desc": "張學良故居所在地，水質清澈無味，環境非常清幽。", 
        "price_level": 1, "price_desc": "💲 百元 (將軍湯)",
        "difficulty": 2, "diff_desc": "🟢 山路好走", 
        "tags": ["張學良", "將軍湯", "免費足湯"], "lat": 24.57, "lon": 121.10
    },
    {
        "name": "桃園嘎拉賀溫泉", "region": "北部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "瀑布SPA",
        "desc": "北部唯一的「溫泉瀑布」，需下切極陡的樓梯，回程是體力大考驗。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 6, "diff_desc": "🟠 陡峭階梯", 
        "tags": ["溫泉瀑布", "膝蓋殺手", "秘境"], "lat": 24.63, "lon": 121.40
    },
    {
        "name": "桃園四稜野溪", "region": "北部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8.5", "benefit": "極致色彩、冒險",
        "desc": "被譽為「七彩岩壁」，位於北橫深處，路徑濕滑難走，需拉繩攀岩。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 8, "diff_desc": "🔴 需專業裝備", 
        "tags": ["七彩岩壁", "高手限定", "防滑鞋必備"], "lat": 24.65, "lon": 121.42
    },
    {
        "name": "桃園羅浮溫泉", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 8.6", "benefit": "修復肌膚",
        "desc": "位於北橫公路，有免費泡腳池與付費大眾池，適合重機/單車族中途休息。", 
        "price_level": 1, "price_desc": "💲 百元 (大眾池)",
        "difficulty": 1, "diff_desc": "🟢 開車即達", 
        "tags": ["北橫中繼", "泰雅文化", "義興吊橋"], "lat": 24.78, "lon": 121.37
    },
     {
        "name": "宜蘭礁溪溫泉公園", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7.5", "benefit": "平原溫泉、交通便",
        "desc": "森林風呂裸湯非常有日本味，外圍有免費足湯。", 
        "price_level": 1, "price_desc": "💲 百元 (裸湯)",
        "difficulty": 1, "diff_desc": "🟢 火車可達", 
        "tags": ["高CP值", "免費足湯", "平地"], "lat": 24.83, "lon": 121.77
    },
    {
        "name": "宜蘭梵梵(芃芃)野溪", "region": "北部", "type": "鎂鈣離子碳酸泉", 
        "ph": "PH 6.6", "benefit": "生態觀察、戲水",
        "desc": "北台灣最親民的野溪溫泉，步行約 20 分鐘可達，適合野溪新手。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 3, "diff_desc": "🟡 需涉水步行", 
        "tags": ["野溪新手", "親子探險", "露營"], "lat": 24.60, "lon": 121.52
    },
    {
        "name": "宜蘭鳩之澤溫泉", "region": "北部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "舒暢筋骨",
        "desc": "位於太平山下，超大石頭湯屋，著名的淡藍色乳白泉水。", 
        "price_level": 1, "price_desc": "💲 百元 (大眾池)",
        "difficulty": 3, "diff_desc": "🟡 山路(易起霧)", 
        "tags": ["煮玉米", "藍色溫泉", "國家公園"], "lat": 24.53, "lon": 121.50
    },

    # ================= 中部 (7處) =================
    {
        "name": "苗栗泰安溫泉", "region": "中部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "美人湯、紓壓",
        "desc": "群山環繞，水質優良，知名電視劇《敗犬女王》取景地。", 
        "price_level": 3, "price_desc": "💲💲💲 頂級度假",
        "difficulty": 2, "diff_desc": "🟢 山路好走", 
        "tags": ["度假村", "環境清幽", "蜜月"], "lat": 24.47, "lon": 120.97
    },
    {
        "name": "台中谷關溫泉", "region": "中部", "type": "碳酸泉", 
        "ph": "PH 7.6", "benefit": "關節炎、腸胃",
        "desc": "中橫公路指標景點，明治天皇曾來過，有歷史感。", 
        "price_level": 2, "price_desc": "💲💲 飯店林立",
        "difficulty": 2, "diff_desc": "🟢 公車可達", 
        "tags": ["歷史悠久", "鱘龍魚餐", "健行"], "lat": 24.20, "lon": 121.00
    },
    {
        "name": "南投雲品/日月潭", "region": "中部", "type": "碳酸氫鈉泉", 
        "ph": "PH 8.6", "benefit": "極致放鬆、湖景",
        "desc": "日月潭第一泉，價格極高，但在房內看湖泡湯無價。", 
        "price_level": 3, "price_desc": "💲💲💲 奢華頂級",
        "difficulty": 1, "diff_desc": "🟢 全齡友善", 
        "tags": ["湖景", "五星級", "親子"], "lat": 23.87, "lon": 120.92
    },
    {
        "name": "南投東埔溫泉", "region": "中部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7.5", "benefit": "消除疲勞(登山後)",
        "desc": "位於玉山腳下，是登山客下山後的救贖，附近有彩虹瀑布。", 
        "price_level": 2, "price_desc": "💲💲 飯店/民宿",
        "difficulty": 3, "diff_desc": "🟡 山路較遠", 
        "tags": ["玉山登山口", "布農族", "梅花餐"], "lat": 23.56, "lon": 120.92
    },
    {
        "name": "南投廬山溫泉", "region": "中部", "type": "強鹼性碳酸氫鈉泉", 
        "ph": "PH 9", "benefit": "天下第一泉(舊稱)",
        "desc": "曾經的台灣第一泉，雖因地質問題沒落，但水質依然極佳，人少清幽。", 
        "price_level": 1, "price_desc": "💲 百元~千元",
        "difficulty": 3, "diff_desc": "🟡 山路蜿蜒", 
        "tags": ["懷舊", "水質極滑", "煮溫泉蛋"], "lat": 24.02, "lon": 121.18
    },
    {
        "name": "南投春陽溫泉", "region": "中部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7.5", "benefit": "賽德克文化",
        "desc": "就在廬山附近，但更原始、更安靜，許多露營客喜愛的私房點。", 
        "price_level": 1, "price_desc": "💲 百元/露營",
        "difficulty": 2, "diff_desc": "🟢 開車即達", 
        "tags": ["露營", "賽德克巴萊", "人少"], "lat": 24.02, "lon": 121.16
    },

    # ================= 南部 (6處) =================
    {
        "name": "台南關子嶺溫泉", "region": "南部", "type": "泥漿溫泉 (稀有)", 
        "ph": "PH 8", "benefit": "去角質、風濕",
        "desc": "世界三大泥漿溫泉之一，黑色泉水，泡完皮膚極滑。", 
        "price_level": 2, "price_desc": "💲💲 特色湯屋",
        "difficulty": 2, "diff_desc": "🟢 開車/公車", 
        "tags": ["世界稀有", "泥漿", "甕缸雞"], "lat": 23.33, "lon": 120.50
    },
    {
        "name": "高雄寶來溫泉", "region": "南部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7.2", "benefit": "軟化角質",
        "desc": "六龜山區，經歷風災後重生，賞梅花兼泡湯。", 
        "price_level": 2, "price_desc": "💲💲 露營/湯屋",
        "difficulty": 3, "diff_desc": "🟡 山路蜿蜒", 
        "tags": ["露營", "賞花", "泛舟"], "lat": 23.11, "lon": 120.70
    },
    {
        "name": "高雄不老溫泉", "region": "南部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7.5", "benefit": "回春、滑嫩",
        "desc": "六龜區的另一寶，傳說村民長壽而得名，水質滑膩感不輸關子嶺。", 
        "price_level": 1, "price_desc": "💲 百元/住宿",
        "difficulty": 3, "diff_desc": "🟡 山路蜿蜒", 
        "tags": ["長生不老", "平價", "在地推薦"], "lat": 23.06, "lon": 120.66
    },
    {
        "name": "屏東四重溪溫泉", "region": "南部", "type": "鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "促進循環",
        "desc": "國境之南，日治時期四大名湯之一，有免費公共足湯。", 
        "price_level": 1, "price_desc": "🆓 足湯/💲 百元",
        "difficulty": 2, "diff_desc": "🟢 車程較遠", 
        "tags": ["免費足湯", "日本親王", "落山風"], "lat": 22.09, "lon": 120.74
    },
    {
        "name": "屏東旭海溫泉", "region": "南部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7.3", "benefit": "放鬆身心",
        "desc": "位於阿朗壹古道終點，雖然偏遠但非常純淨，有種遺世獨立感。", 
        "price_level": 1, "price_desc": "💲 百元 (公共浴室)",
        "difficulty": 3, "diff_desc": "🟡 極遠(近台東)", 
        "tags": ["環島必停", "阿朗壹", "牡丹灣"], "lat": 22.19, "lon": 120.88
    },
    {
        "name": "屏東哈尤溪溫泉", "region": "南部", "type": "硫磺鹽泉", 
        "ph": "PH 6.5", "benefit": "視覺震撼",
        "desc": "【季節限定】需搭乘部落吉普車溯溪進入，七彩岩壁壯觀程度全台第一。", 
        "price_level": 2, "price_desc": "💲💲 部落導覽費",
        "difficulty": 4, "diff_desc": "🟡 吉普車接駁", 
        "tags": ["七彩岩壁", "枯水期限定", "需預約"], "lat": 22.76, "lon": 120.76
    },

    # ================= 東部 (10處) =================
    {
        "name": "宜蘭鳩之澤溫泉", "region": "東部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "舒暢筋骨",
        "desc": "位於太平山下，超大石頭湯屋，著名的淡藍色乳白泉水。", 
        "price_level": 1, "price_desc": "💲 百元 (大眾池)",
        "difficulty": 3, "diff_desc": "🟡 山路(易起霧)", 
        "tags": ["煮玉米", "藍色溫泉", "國家公園"], "lat": 24.53, "lon": 121.50
    },
    {
        "name": "花蓮瑞穗溫泉", "region": "東部", "type": "氯化物碳酸鹽泉", 
        "ph": "PH 6-7", "benefit": "傳說生男湯",
        "desc": "全台唯一的「黃金湯」，泉水富含鐵質，遇空氣變黃色。", 
        "price_level": 2, "price_desc": "💲💲 莊園/民宿",
        "difficulty": 2, "diff_desc": "🟢 火車+租車", 
        "tags": ["黃金湯", "生男湯", "平原"], "lat": 23.49, "lon": 121.35
    },
    {
        "name": "花蓮安通溫泉", "region": "東部", "type": "硫酸鹽氯化物泉", 
        "ph": "PH 8.8", "benefit": "皮膚外傷",
        "desc": "百年歷史的日式古蹟溫泉，有一股淡淡的瓦斯味(硫化氫)，水質極佳。", 
        "price_level": 1, "price_desc": "💲 百元/💲💲 湯屋",
        "difficulty": 2, "diff_desc": "🟢 玉長公路旁", 
        "tags": ["日式古蹟", "黑光溜滑", "花東縱谷"], "lat": 23.27, "lon": 121.34
    },
    {
        "name": "花蓮文山溫泉", "region": "東部", "type": "中性硫酸鹽泉", 
        "ph": "PH 6.5", "benefit": "太魯閣峽谷",
        "desc": "太魯閣國家公園內唯一的野溪溫泉，目前僅開放探勘，需注意落石。", 
        "price_level": 0, "price_desc": "🆓 風險自負",
        "difficulty": 5, "diff_desc": "🟠 峽谷探險", 
        "tags": ["太魯閣", "半封閉", "絕景"], "lat": 24.19, "lon": 121.48
    },
    {
        "name": "花蓮二子山溫泉", "region": "東部", "type": "中性碳酸泉", 
        "ph": "PH 6.9", "benefit": "極致野營",
        "desc": "野溪溫泉的終極目標之一，需步行單程 4-6 小時，需申請入山證。", 
        "price_level": 0, "price_desc": "🆓 野溪露營",
        "difficulty": 10, "diff_desc": "🔴 重裝溯溪", 
        "tags": ["特種部隊", "野營聖地", "需渡河"], "lat": 23.89, "lon": 121.36
    },
    {
        "name": "台東知本溫泉", "region": "東部", "type": "碳酸氫鈉泉", 
        "ph": "PH 8.4", "benefit": "美白、消除疲勞",
        "desc": "東部規模最大溫泉區，飯店設施完善，適合全家。", 
        "price_level": 2, "price_desc": "💲💲 飯店林立",
        "difficulty": 1, "diff_desc": "🟢 機場/火車", 
        "tags": ["煮溫泉蛋", "森林遊樂區", "老牌"], "lat": 22.69, "lon": 121.00
    },
    {
        "name": "台東紅葉野溪溫泉", "region": "東部", "type": "中性碳酸氫鈉泉", 
        "ph": "PH 6.8", "benefit": "野趣、棒球鄉",
        "desc": "位於紅葉少棒故鄉，河床旁挖掘出的天然湯池，需視水量而定。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 4, "diff_desc": "🟡 需步行下溪", 
        "tags": ["少棒故鄉", "野溪入門", "秋季限定"], "lat": 22.89, "lon": 121.06
    },
    {
        "name": "台東金崙溫泉", "region": "東部", "type": "弱鹼性碳酸氫鈉泉", 
        "ph": "PH 7-8", "benefit": "高CP值、看火車",
        "desc": "近年爆紅！泉水豐沛且價格親民，許多人專程搭火車來泡湯。", 
        "price_level": 1, "price_desc": "💲 百元 (超值)",
        "difficulty": 1, "diff_desc": "🟢 火車即達", 
        "tags": ["火車迷", "高CP值", "在地人最愛"], "lat": 22.53, "lon": 120.96
    },
    {
        "name": "台東霧鹿/六口溫泉", "region": "東部", "type": "硫酸鹽碳酸氫鈉泉", 
        "ph": "PH 7-8", "benefit": "峽谷景觀",
        "desc": "南橫公路旁的免費足湯，可煮溫泉蛋，看峽谷鬼斧神工。", 
        "price_level": 0, "price_desc": "🆓 路邊免費",
        "difficulty": 3, "diff_desc": "🟡 南橫公路", 
        "tags": ["煮溫泉蛋", "南橫絕景", "峽谷"], "lat": 23.17, "lon": 121.04
    },
    {
        "name": "台東栗松溫泉", "region": "東部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7", "benefit": "視覺震撼、冒險",
        "desc": "【全台最美野溪溫泉】岩壁翠綠如翡翠，枯水期限定(11-4月)，難度極高。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 9, "diff_desc": "🔴 攀岩/拉繩", 
        "tags": ["最美野溪", "體力活", "管制"], "lat": 23.19, "lon": 121.03
    },

    # ================= 離島 (1處) =================
    {
        "name": "綠島朝日溫泉", "region": "東部", "type": "硫磺鹽泉 (海水)", 
        "ph": "PH 7.5", "benefit": "世界級稀有",
        "desc": "【世界唯三】的海底溫泉！邊泡湯邊看太平洋日出，人生必去清單。", 
        "price_level": 1, "price_desc": "💲 門票制",
        "difficulty": 5, "diff_desc": "🟠 需搭船/飛機", 
        "tags": ["世界級", "看日出", "海水溫泉"], "lat": 22.63, "lon": 121.50
    }
]

# --- 🛑 Layer 2: Main Interface (Tabs) ---
st.title("♨️ 台灣全島溫泉地圖 Pro")
st.caption(f"共收錄 {len(data)} 處秘境 | 價格分級 | 泉質解析 | 特種部隊野溪")

# 建立分頁
tab1, tab2, tab3 = st.tabs(["📋 溫泉大百科", "🕵️ 智能篩選", "⚠️ 泡湯小知識"])

# --- TAB 1: Menu View (大清單模式) ---
with tab1:
    st.markdown(f"### 📋 全台精選 {len(data)} 處溫泉區一覽")
    
    # 轉換為 DataFrame 供展示
    df_view = pd.DataFrame(data)
    df_display = df_view[['region', 'name', 'price_desc', 'type', 'diff_desc']].copy()
    df_display.columns = ['地區', '名稱', '價格等級', '泉質', '難度']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=600 
    )

# --- TAB 2: Planner View (智能篩選) ---
with tab2:
    with st.expander("⚙️ 設定您的泡湯需求 (點擊收合)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_region = st.selectbox("📍 選擇地區", ["全部顯示", "北部", "中部", "南部", "東部"], index=0)
        with c2:
            # 價格過濾器
            budget_options = ["全部", "🆓 免費 (野溪/足湯)", "💲 百元 (大眾/平價)", "💲💲 千元 (湯屋/住宿)", "💲💲💲 奢華 (度假村)"]
            selected_budget = st.selectbox("💰 預算範圍", budget_options)

        # 難度/類型過濾
        pref_type = st.radio(
            "🛀 偏好類型", 
            ["不拘", "輕鬆抵達 (飯店/湯屋/大眾交通)", "野外冒險 (需步行/攀岩/溯溪)"], 
            horizontal=True
        )

    # Logic Engine
    def filter_springs(spot, u_region, u_budget, u_type):
        # 1. 地區篩選
        if u_region != "全部顯示" and spot['region'] != u_region:
            # 特別處理：綠島歸類在東部，但也需顯示
            if u_region == "東部" and spot['name'] == "綠島朝日溫泉":
                pass # 允許顯示
            elif spot['region'] != u_region:
                return False
            
        # 2. 預算篩選
        # price_level: 0=免費, 1=百元, 2=千元, 3=奢華
        if "免費" in u_budget and spot['price_level'] != 0: return False
        if "百元" in u_budget and spot['price_level'] != 1: return False
        if "千元" in u_budget and spot['price_level'] != 2: return False
        if "奢華" in u_budget and spot['price_level'] != 3: return False
        
        # 3. 類型/難度篩選
        # 輕鬆: difficulty <= 2 (開車/火車/公車)
        # 冒險: difficulty >= 3 (步行/溯溪/攀岩)
        if u_type == "輕鬆抵達 (飯店/湯屋/大眾交通)" and spot['difficulty'] >= 3: return False
        if u_type == "野外冒險 (需步行/攀岩/溯溪)" and spot['difficulty'] < 3: return False
        
        return True

    results = []
    for spot in data:
        if filter_springs(spot, selected_region, selected_budget, pref_type):
            results.append(spot)
            
    # 排序邏輯：優先顯示該篩選條件下，難度較低或較熱門的，
    # 但如果是野外冒險模式，則顯示難度高的
    if pref_type == "野外冒險 (需步行/攀岩/溯溪)":
         results.sort(key=lambda x: x['difficulty'], reverse=True) # 越難越前面
    else:
         results.sort(key=lambda x: x['price_level'], reverse=True) # 越貴越前面(預設)

    # Output Rendering
    if not results:
        st.warning("⚠️ 找不到符合條件的溫泉。建議：\n1. 切換「預算」範圍\n2. 放寬「地區」限制")
    else:
        st.markdown(f"### ✨ 推薦 {len(results)} 個最佳溫泉")
        
        for spot in results:
            # 樣式定義
            border_color = "#ffccbc"
            badge_html = ""
            
            # 特殊標籤邏輯
            if spot['difficulty'] >= 8:
                 badge_html = '<div class="wild-badge">🔥 特種部隊</div>'
                 border_color = "#5D4037" # 深色框
            elif spot['price_level'] == 0:
                badge_html = '<div class="free-badge">🆓 FREE</div>'
                border_color = "#C8E6C9" # 綠色框
            elif spot['price_level'] == 3:
                badge_html = '<div class="recommend-badge">👑 奢華精選</div>'
                border_color = "#F8BBD0" # 粉色框

            # 價格顏色 Class
            p_class = f"price-{spot['price_level']}"
            
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in spot['tags']])
            gmap = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
            
            html_str = ""
            html_str += f'<div class="mobile-card" style="border: 2px solid {border_color};">'
            html_str += f'{badge_html}'
            html_str += f'<div class="card-title">{spot["name"]} <span class="price-tag {p_class}">{spot["price_desc"]}</span></div>'
            html_str += f'<div class="card-meta" style="margin-bottom:8px;">'
            html_str += f'<span style="color:#555;">📍 {spot["region"]}</span> | '
            
            # 難度顏色
            diff_color = "#E65100"
            if spot['difficulty'] >= 5: diff_color = "#D32F2F" # 高難度紅色
            if spot['difficulty'] <= 1: diff_color = "#2E7D32" # 低難度綠色
            
            html_str += f'<span style="font-weight:bold; color:{diff_color};">🚶 {spot["diff_desc"]}</span>'
            html_str += f'</div>'
            
            html_str += f'<div style="color:#455a64; margin-bottom:10px;">{spot["desc"]}</div>'
            
            # --- ✨ 專業泉質區塊 ---
            html_str += f'<div class="spring-info-box">'
            html_str += f'<b>🧪 泉質：</b>{spot["type"]} ({spot["ph"]})<br>'
            html_str += f'<b>💪 功效：</b>{spot["benefit"]}'
            html_str += f'</div>'
            
            html_str += f'<div style="margin-top:10px;">{tags_html}</div>'
            html_str += f'<a href="{gmap}" target="_blank" class="nav-btn">📍 Google Maps 導航</a>'
            html_str += f'</div>'

            st.markdown(html_str, unsafe_allow_html=True)

# --- TAB 3: Knowledge (專業知識) ---
with tab3:
    st.markdown("""
    ### ⚠️ 溫泉達人須知
    
    #### 1. 泉質速查
    * **硫磺泉 (北投/陽明山/綠島)**：有臭蛋味或鹹味，軟化皮膚角質，止癢解毒。**皮膚敏感者慎入**。
    * **碳酸氫鈉泉 (烏來/礁溪/知本)**：俗稱「美人湯」，無色無味，泡完皮膚滑嫩。
    * **泥漿溫泉 (關子嶺)**：灰黑色，含礦物質，去角質效果極強。
    * **碳酸泉 (谷關/四重溪)**：氣泡泉，促進血液循環，對心臟負擔較小。

    #### 2. 野溪溫泉安全守則 (重要！)
    * **季節限定**：許多野溪溫泉（如栗松/梵梵/哈尤溪）僅在**枯水期（11月-4月）**適合前往。
    * **溪水暴漲**：山區午後雷陣雨可能導致溪水瞬間暴漲，見烏雲請立即撤退。
    * **裝備要求**：難度 5 以上建議穿著溯溪鞋；難度 8 以上（二子山/四稜）建議有嚮導帶領。
    * **無痕山林**：野溪多無垃圾桶，請務必**帶走所有垃圾**。
    
    #### 3. 泡湯禁忌
    * 飲酒後、過度疲勞、空腹或剛吃飽請勿泡湯。
    * 每次浸泡不超過 15 分鐘，起身要慢，以免姿態性低血壓暈倒。
    """)

