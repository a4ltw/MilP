#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
軍事詞彙生成腳本
生成500個額外的軍事術語添加到詞彙庫
"""

import json
from datetime import date

# 通用軍事術語 (80個)
general_terms = [
    # 作戰相關
    ("戰鬥", "Combat", "", "combat", 1),
    ("戰役", "Campaign", "", "combat", 1),
    ("戰爭", "War", "", "combat", 1),
    ("和平", "Peace", "", "status", 1),
    ("停火", "Ceasefire", "", "status", 2),
    ("休戰", "Truce", "", "status", 2),
    ("投降", "Surrender", "", "action", 1),
    ("撤退", "Retreat", "", "action", 1),
    ("前進", "Advance", "", "action", 1),
    ("佔領", "Occupy", "", "action", 1),

    # 軍階 (繼續)
    ("准將", "Brigadier General", "BG", "rank", 2),
    ("軍士長", "Master Sergeant", "MSG", "rank", 2),
    ("士官", "Non-commissioned Officer", "NCO", "rank", 2),
    ("士兵", "Soldier", "", "rank", 1),
    ("新兵", "Recruit", "", "rank", 1),
    ("老兵", "Veteran", "", "rank", 1),
    ("預備役", "Reserve", "", "status", 2),
    ("現役", "Active Duty", "", "status", 2),

    # 組織單位
    ("軍隊", "Military", "", "organization", 1),
    ("部隊", "Troops", "", "organization", 1),
    ("軍團", "Corps", "", "organization", 2),
    ("師", "Division", "DIV", "organization", 1),
    ("旅", "Brigade", "BDE", "organization", 1),
    ("團", "Regiment", "REG", "organization", 1),
    ("營", "Battalion", "BN", "organization", 1),
    ("連", "Company", "CO", "organization", 1),
    ("排", "Platoon", "PLT", "organization", 1),
    ("班", "Squad", "SQ", "organization", 1),
    ("小隊", "Team", "", "organization", 1),
    ("分隊", "Section", "", "organization", 1),

    # 戰術概念
    ("進攻", "Offensive", "OFF", "tactical", 1),
    ("防禦", "Defensive", "DEF", "tactical", 1),
    ("反攻", "Counterattack", "", "tactical", 2),
    ("突襲", "Assault", "", "tactical", 1),
    ("圍攻", "Siege", "", "tactical", 2),
    ("封鎖", "Blockade", "", "tactical", 2),
    ("包圍", "Encirclement", "", "tactical", 2),
    ("突破", "Breakthrough", "", "tactical", 2),
    ("側翼", "Flank", "", "tactical", 2),
    ("前線", "Frontline", "", "position", 1),
    ("後方", "Rear", "", "position", 1),
    ("據點", "Stronghold", "", "position", 2),
    ("陣線", "Front", "", "position", 1),

    # 武器和裝備
    ("武器", "Weapon", "", "equipment", 1),
    ("裝備", "Equipment", "EQUIP", "equipment", 1),
    ("彈藥", "Ammunition", "AMMO", "supply", 1),
    ("補給", "Supply", "", "supply", 1),
    ("燃料", "Fuel", "", "supply", 1),
    ("糧食", "Rations", "", "supply", 1),
    ("醫療", "Medical", "MED", "support", 1),
    ("維修", "Maintenance", "MAINT", "support", 1),
    ("運輸", "Transport", "", "support", 1),

    # 通訊和情報
    ("通訊", "Communication", "COMM", "support", 1),
    ("無線電", "Radio", "", "equipment", 1),
    ("訊號", "Signal", "SIG", "communication", 1),
    ("密碼", "Code", "", "communication", 2),
    ("加密", "Encryption", "", "communication", 2),
    ("監視", "Surveillance", "", "information", 2),
    ("間諜", "Spy", "", "information", 2),
    ("特務", "Agent", "", "information", 2),
    ("偵查", "Scouting", "", "information", 1),

    # 指揮和控制
    ("指揮", "Command", "CMD", "command", 1),
    ("控制", "Control", "CTRL", "command", 1),
    ("命令", "Order", "", "command", 1),
    ("指示", "Instruction", "", "command", 1),
    ("報告", "Report", "", "communication", 1),
    ("警報", "Alert", "", "status", 1),
    ("警戒", "Watch", "", "status", 1),
    ("哨兵", "Sentry", "", "personnel", 1),
    ("崗哨", "Post", "", "position", 1),

    # 訓練和演習
    ("訓練", "Training", "", "activity", 1),
    ("演習", "Exercise", "EX", "activity", 1),
    ("操練", "Drill", "", "activity", 1),
    ("演練", "Practice", "", "activity", 1),
    ("模擬", "Simulation", "SIM", "activity", 2),

    # 其他
    ("任務", "Mission", "", "operation", 1),
    ("目標", "Target", "TGT", "tactical", 1),
    ("敵人", "Enemy", "", "status", 1),
    ("友軍", "Friendly Forces", "", "status", 1),
    ("盟友", "Ally", "", "status", 1),
]

# 陸軍術語 (140個)
army_terms = [
    # 兵種
    ("砲兵", "Artillery", "ART", "unit", 1),
    ("工兵", "Engineer", "ENG", "unit", 1),
    ("通信兵", "Signal Corps", "SIG", "unit", 2),
    ("醫療兵", "Medic", "", "personnel", 1),
    ("狙擊手", "Sniper", "", "personnel", 2),
    ("偵察兵", "Scout", "", "personnel", 1),
    ("傘兵", "Paratrooper", "PARA", "unit", 2),
    ("空降兵", "Airborne", "", "unit", 2),
    ("特種部隊", "Special Forces", "SF", "unit", 2),
    ("突擊隊", "Commando", "", "unit", 2),
    ("遊騎兵", "Ranger", "", "unit", 2),
    ("憲兵", "Military Police", "MP", "unit", 1),

    # 裝甲車輛
    ("主戰坦克", "Main Battle Tank", "MBT", "vehicle", 2),
    ("輕型坦克", "Light Tank", "", "vehicle", 2),
    ("重型坦克", "Heavy Tank", "", "vehicle", 2),
    ("步兵戰車", "Infantry Fighting Vehicle", "IFV", "vehicle", 2),
    ("裝甲車", "Armored Vehicle", "AV", "vehicle", 1),
    ("自走砲", "Self-Propelled Artillery", "SPA", "vehicle", 2),
    ("防空車", "Anti-Aircraft Vehicle", "AAV", "vehicle", 2),
    ("運兵車", "Troop Carrier", "", "vehicle", 1),
    ("吉普車", "Jeep", "", "vehicle", 1),
    ("卡車", "Truck", "", "vehicle", 1),
    ("補給車", "Supply Vehicle", "", "vehicle", 1),
    ("救護車", "Ambulance", "", "vehicle", 1),
    ("指揮車", "Command Vehicle", "", "vehicle", 2),
    ("掃雷車", "Mine Clearing Vehicle", "", "vehicle", 2),
    ("工程車", "Engineering Vehicle", "", "vehicle", 2),
    ("橋樑車", "Bridge Layer", "", "vehicle", 2),

    # 火砲
    ("野戰砲", "Field Artillery", "FA", "weapon", 2),
    ("加農砲", "Cannon", "", "weapon", 2),
    ("火箭砲", "Rocket Artillery", "RA", "weapon", 2),
    ("多管火箭", "Multiple Rocket Launcher", "MRL", "weapon", 2),
    ("反坦克砲", "Anti-Tank Gun", "ATG", "weapon", 2),
    ("高射砲", "Anti-Aircraft Gun", "AAG", "weapon", 2),
    ("迫擊砲", "Mortar", "", "weapon", 1),

    # 輕武器
    ("突擊步槍", "Assault Rifle", "AR", "weapon", 1),
    ("狙擊槍", "Sniper Rifle", "", "weapon", 2),
    ("霰彈槍", "Shotgun", "", "weapon", 1),
    ("衝鋒槍", "Submachine Gun", "SMG", "weapon", 2),
    ("手槍", "Pistol", "", "weapon", 1),
    ("左輪手槍", "Revolver", "", "weapon", 1),
    ("輕機槍", "Light Machine Gun", "LMG", "weapon", 2),
    ("重機槍", "Heavy Machine Gun", "HMG", "weapon", 2),
    ("反器材步槍", "Anti-Materiel Rifle", "AMR", "weapon", 2),

    # 爆裂物
    ("地雷", "Landmine", "", "weapon", 1),
    ("反坦克地雷", "Anti-Tank Mine", "ATM", "weapon", 2),
    ("反人員地雷", "Anti-Personnel Mine", "APM", "weapon", 2),
    ("詭雷", "Booby Trap", "", "weapon", 2),
    ("炸藥", "Explosive", "", "weapon", 1),
    ("C4炸藥", "C4", "", "weapon", 2),
    ("手榴彈", "Hand Grenade", "", "weapon", 1),
    ("煙霧彈", "Smoke Grenade", "", "weapon", 1),
    ("閃光彈", "Flashbang", "", "weapon", 2),
    ("催淚彈", "Tear Gas", "", "weapon", 2),

    # 飛彈和火箭
    ("反坦克飛彈", "Anti-Tank Missile", "ATM", "weapon", 2),
    ("肩射飛彈", "Shoulder-Fired Missile", "", "weapon", 2),
    ("火箭筒", "Rocket Launcher", "RL", "weapon", 1),
    ("火箭彈", "Rocket", "", "weapon", 1),
    ("彈道飛彈", "Ballistic Missile", "BM", "weapon", 2),
    ("巡弋飛彈", "Cruise Missile", "CM", "weapon", 2),
    ("防空飛彈", "Surface-to-Air Missile", "SAM", "weapon", 2),

    # 防護裝備
    ("頭盔", "Helmet", "", "equipment", 1),
    ("防彈背心", "Body Armor", "", "equipment", 1),
    ("防彈衣", "Bulletproof Vest", "", "equipment", 1),
    ("防毒面具", "Gas Mask", "", "equipment", 1),
    ("護目鏡", "Goggles", "", "equipment", 1),
    ("戰術背心", "Tactical Vest", "", "equipment", 2),

    # 裝備和配件
    ("瞄準鏡", "Scope", "", "equipment", 1),
    ("夜視鏡", "Night Vision", "NV", "equipment", 2),
    ("熱像儀", "Thermal Imager", "", "equipment", 2),
    ("望遠鏡", "Binoculars", "", "equipment", 1),
    ("指北針", "Compass", "", "equipment", 1),
    ("地圖", "Map", "", "equipment", 1),
    ("刺刀", "Bayonet", "", "weapon", 1),
    ("匕首", "Dagger", "", "weapon", 1),
    ("軍刀", "Sword", "", "weapon", 1),
    ("彈匣", "Magazine", "MAG", "equipment", 1),
    ("彈藥帶", "Ammunition Belt", "", "equipment", 1),
    ("背包", "Backpack", "", "equipment", 1),
    ("水壺", "Canteen", "", "equipment", 1),
    ("急救包", "First Aid Kit", "", "equipment", 1),
    ("睡袋", "Sleeping Bag", "", "equipment", 1),
    ("帳篷", "Tent", "", "equipment", 1),

    # 陣地和工事
    ("碉堡", "Pillbox", "", "fortification", 2),
    ("掩體", "Bunker", "", "fortification", 1),
    ("戰壕", "Trench", "", "fortification", 1),
    ("壕溝", "Foxhole", "", "fortification", 2),
    ("防禦工事", "Fortification", "", "fortification", 2),
    ("障礙物", "Obstacle", "", "fortification", 1),
    ("鐵絲網", "Barbed Wire", "", "fortification", 1),
    ("路障", "Roadblock", "", "fortification", 1),
    ("檢查哨", "Checkpoint", "", "position", 1),
    ("觀察哨", "Observation Post", "OP", "position", 2),
    ("前哨", "Outpost", "", "position", 1),
    ("基地", "Base", "", "position", 1),
    ("營地", "Camp", "", "position", 1),
    ("兵營", "Barracks", "", "facility", 1),
    ("倉庫", "Depot", "", "facility", 1),
    ("軍火庫", "Arsenal", "", "facility", 2),

    # 戰術動作
    ("衝鋒", "Charge", "", "tactical", 1),
    ("掃蕩", "Sweep", "", "tactical", 2),
    ("清剿", "Mop-up", "", "tactical", 2),
    ("搜索", "Search", "", "tactical", 1),
    ("追擊", "Pursuit", "", "tactical", 2),
    ("伏擊", "Ambush", "", "tactical", 2),
    ("奇襲", "Surprise Attack", "", "tactical", 2),
    ("佯攻", "Feint", "", "tactical", 2),
    ("誘敵", "Lure", "", "tactical", 2),
    ("迂迴", "Flanking Maneuver", "", "tactical", 2),
    ("滲透", "Infiltration", "", "tactical", 2),
    ("突擊", "Raid", "", "tactical", 1),
    ("強攻", "Storm", "", "tactical", 2),
    ("登陸", "Landing", "", "operation", 1),
    ("空降", "Airdrop", "", "operation", 2),
    ("撤離", "Extraction", "", "operation", 2),

    # 作戰狀態
    ("警戒", "Alert", "", "status", 1),
    ("待命", "Standby", "", "status", 1),
    ("就緒", "Ready", "", "status", 1),
    ("戰備", "Combat Ready", "", "status", 2),
    ("備戰", "Prepare for War", "", "status", 2),
    ("動員", "Mobilization", "", "status", 2),
    ("集結", "Assembly", "", "status", 1),
    ("展開", "Deployment", "", "status", 1),
]

# 海軍術語 (140個)
navy_terms = [
    # 艦艇類型
    ("戰艦", "Battleship", "BB", "vessel", 2),
    ("航空母艦", "Aircraft Carrier", "CV", "vessel", 1),
    ("巡洋艦", "Cruiser", "CG", "vessel", 1),
    ("驅逐艦", "Destroyer", "DD", "vessel", 1),
    ("護衛艦", "Frigate", "FF", "vessel", 1),
    ("巡防艦", "Corvette", "", "vessel", 2),
    ("潛艇", "Submarine", "SS", "vessel", 1),
    ("核潛艇", "Nuclear Submarine", "SSN", "vessel", 2),
    ("攻擊潛艇", "Attack Submarine", "SSN", "vessel", 2),
    ("彈道飛彈潛艇", "Ballistic Missile Submarine", "SSBN", "vessel", 2),
    ("登陸艦", "Landing Ship", "LST", "vessel", 2),
    ("兩棲突擊艦", "Amphibious Assault Ship", "LHA", "vessel", 2),
    ("補給艦", "Supply Ship", "", "vessel", 1),
    ("油輪", "Tanker", "", "vessel", 1),
    ("運輸艦", "Transport Ship", "", "vessel", 1),
    ("醫療艦", "Hospital Ship", "", "vessel", 2),
    ("掃雷艦", "Minesweeper", "", "vessel", 2),
    ("快艇", "Fast Attack Craft", "FAC", "vessel", 2),
    ("巡邏艇", "Patrol Boat", "PB", "vessel", 1),
    ("魚雷艇", "Torpedo Boat", "", "vessel", 2),
    ("飛彈艇", "Missile Boat", "", "vessel", 2),
    ("氣墊船", "Hovercraft", "", "vessel", 2),
    ("登陸艇", "Landing Craft", "", "vessel", 1),

    # 艦載武器
    ("艦砲", "Naval Gun", "", "weapon", 1),
    ("主砲", "Main Gun", "", "weapon", 1),
    ("副砲", "Secondary Gun", "", "weapon", 2),
    ("防空砲", "Anti-Aircraft Gun", "AAG", "weapon", 2),
    ("近防砲", "Close-In Weapon System", "CIWS", "weapon", 2),
    ("魚雷", "Torpedo", "", "weapon", 1),
    ("深水炸彈", "Depth Charge", "", "weapon", 2),
    ("水雷", "Naval Mine", "", "weapon", 2),
    ("反艦飛彈", "Anti-Ship Missile", "ASM", "weapon", 2),
    ("對地飛彈", "Land Attack Missile", "", "weapon", 2),
    ("防空飛彈", "Surface-to-Air Missile", "SAM", "weapon", 2),
    ("反潛飛彈", "Anti-Submarine Missile", "ASM", "weapon", 2),
    ("巡弋飛彈", "Cruise Missile", "CM", "weapon", 2),
    ("魚叉飛彈", "Harpoon Missile", "", "weapon", 2),
    ("戰斧飛彈", "Tomahawk Missile", "", "weapon", 2),

    # 艦載機
    ("艦載戰鬥機", "Carrier Fighter", "", "aircraft", 2),
    ("反潛機", "Anti-Submarine Aircraft", "ASW", "aircraft", 2),
    ("預警機", "Early Warning Aircraft", "AEW", "aircraft", 2),
    ("電戰機", "Electronic Warfare Aircraft", "EW", "aircraft", 2),
    ("運輸機", "Transport Aircraft", "", "aircraft", 1),
    ("直升機", "Helicopter", "HELO", "aircraft", 1),
    ("反潛直升機", "Anti-Submarine Helicopter", "", "aircraft", 2),
    ("搜救直升機", "Search and Rescue Helicopter", "SAR", "aircraft", 2),

    # 艦上設施和系統
    ("艦橋", "Bridge", "", "facility", 1),
    ("駕駛台", "Wheelhouse", "", "facility", 2),
    ("指揮中心", "Combat Information Center", "CIC", "facility", 2),
    ("甲板", "Deck", "", "facility", 1),
    ("飛行甲板", "Flight Deck", "", "facility", 2),
    ("機庫", "Hangar", "", "facility", 1),
    ("船艙", "Cabin", "", "facility", 1),
    ("彈藥庫", "Magazine", "", "facility", 2),
    ("引擎室", "Engine Room", "", "facility", 1),
    ("鍋爐室", "Boiler Room", "", "facility", 2),
    ("雷達室", "Radar Room", "", "facility", 2),
    ("通訊室", "Radio Room", "", "facility", 1),
    ("醫務室", "Sick Bay", "", "facility", 1),
    ("餐廳", "Mess Hall", "", "facility", 1),

    # 聲納和探測
    ("聲納", "Sonar", "", "equipment", 1),
    ("主動聲納", "Active Sonar", "", "equipment", 2),
    ("被動聲納", "Passive Sonar", "", "equipment", 2),
    ("拖曳聲納", "Towed Sonar", "", "equipment", 2),
    ("聲納浮標", "Sonobuoy", "", "equipment", 2),
    ("雷達", "Radar", "", "equipment", 1),
    ("搜索雷達", "Search Radar", "", "equipment", 2),
    ("火控雷達", "Fire Control Radar", "FCR", "equipment", 2),
    ("導航雷達", "Navigation Radar", "", "equipment", 1),
    ("電子戰系統", "Electronic Warfare System", "EW", "equipment", 2),
    ("對抗措施", "Countermeasures", "", "equipment", 2),
    ("干擾器", "Jammer", "", "equipment", 2),
    ("誘餌", "Decoy", "", "equipment", 2),
    ("煙幕", "Smoke Screen", "", "tactical", 1),

    # 船員
    ("艦長", "Captain", "CAPT", "rank", 1),
    ("大副", "Executive Officer", "XO", "rank", 2),
    ("輪機長", "Chief Engineer", "", "rank", 2),
    ("砲術長", "Gunnery Officer", "", "rank", 2),
    ("航海長", "Navigator", "", "rank", 2),
    ("通信官", "Communication Officer", "", "rank", 2),
    ("醫官", "Medical Officer", "", "rank", 2),
    ("水手", "Sailor", "", "rank", 1),
    ("艦員", "Crew", "", "rank", 1),
    ("舵手", "Helmsman", "", "personnel", 1),
    ("砲手", "Gunner", "", "personnel", 1),
    ("雷達兵", "Radar Operator", "", "personnel", 2),
    ("聲納兵", "Sonar Operator", "", "personnel", 2),

    # 海軍作戰
    ("海戰", "Naval Battle", "", "combat", 1),
    ("海上封鎖", "Naval Blockade", "", "operation", 2),
    ("護航", "Convoy", "", "operation", 1),
    ("巡航", "Patrol", "", "operation", 1),
    ("搜索", "Search", "", "operation", 1),
    ("救援", "Rescue", "", "operation", 1),
    ("反潛", "Anti-Submarine Warfare", "ASW", "operation", 2),
    ("反艦", "Anti-Ship Warfare", "ASW", "operation", 2),
    ("防空", "Air Defense", "AD", "operation", 1),
    ("水雷戰", "Mine Warfare", "", "operation", 2),
    ("掃雷", "Minesweeping", "", "operation", 2),
    ("佈雷", "Mining", "", "operation", 2),
    ("兩棲作戰", "Amphibious Operation", "AMPH OP", "operation", 2),
    ("登陸作戰", "Amphibious Assault", "", "operation", 2),
    ("艦砲射擊", "Naval Gunfire Support", "NGS", "operation", 2),

    # 航海術語
    ("啟航", "Sail", "", "navigation", 1),
    ("航行", "Navigation", "NAV", "navigation", 1),
    ("停泊", "Berth", "", "navigation", 1),
    ("錨定", "Anchor", "", "navigation", 1),
    ("拋錨", "Drop Anchor", "", "navigation", 1),
    ("起錨", "Weigh Anchor", "", "navigation", 1),
    ("靠港", "Dock", "", "navigation", 1),
    ("離港", "Depart", "", "navigation", 1),
    ("航向", "Course", "", "navigation", 1),
    ("航速", "Speed", "", "navigation", 1),
    ("航道", "Channel", "", "navigation", 1),
    ("海圖", "Chart", "", "navigation", 1),
    ("經度", "Longitude", "", "navigation", 2),
    ("緯度", "Latitude", "", "navigation", 2),
    ("海流", "Current", "", "navigation", 1),
    ("潮汐", "Tide", "", "navigation", 1),
    ("風浪", "Wave", "", "navigation", 1),
    ("風向", "Wind Direction", "", "navigation", 1),
    ("風速", "Wind Speed", "", "navigation", 1),

    # 船體結構
    ("船首", "Bow", "", "structure", 1),
    ("船尾", "Stern", "", "structure", 1),
    ("船舷", "Hull", "", "structure", 1),
    ("左舷", "Port", "", "structure", 1),
    ("右舷", "Starboard", "", "structure", 1),
    ("龍骨", "Keel", "", "structure", 2),
    ("螺旋槳", "Propeller", "", "structure", 1),
    ("舵", "Rudder", "", "structure", 1),
    ("錨", "Anchor", "", "structure", 1),
    ("煙囪", "Funnel", "", "structure", 1),
    ("桅杆", "Mast", "", "structure", 1),
    ("救生艇", "Lifeboat", "", "equipment", 1),
    ("救生筏", "Life Raft", "", "equipment", 1),
    ("救生衣", "Life Jacket", "", "equipment", 1),
]

# 空軍術語 (140個)
airforce_terms = [
    # 飛機類型
    ("戰鬥機", "Fighter", "", "aircraft", 1),
    ("攔截機", "Interceptor", "", "aircraft", 2),
    ("戰鬥轟炸機", "Fighter-Bomber", "", "aircraft", 2),
    ("轟炸機", "Bomber", "", "aircraft", 1),
    ("戰略轟炸機", "Strategic Bomber", "", "aircraft", 2),
    ("戰術轟炸機", "Tactical Bomber", "", "aircraft", 2),
    ("攻擊機", "Attack Aircraft", "", "aircraft", 2),
    ("對地攻擊機", "Ground Attack Aircraft", "", "aircraft", 2),
    ("偵察機", "Reconnaissance Aircraft", "RECON", "aircraft", 2),
    ("預警機", "Airborne Early Warning", "AEW", "aircraft", 2),
    ("電子戰機", "Electronic Warfare Aircraft", "EW", "aircraft", 2),
    ("運輸機", "Transport Aircraft", "", "aircraft", 1),
    ("空中加油機", "Tanker Aircraft", "", "aircraft", 2),
    ("教練機", "Trainer", "", "aircraft", 1),
    ("無人機", "Unmanned Aerial Vehicle", "UAV", "aircraft", 2),
    ("無人戰鬥機", "Unmanned Combat Aerial Vehicle", "UCAV", "aircraft", 2),
    ("隱形戰機", "Stealth Fighter", "", "aircraft", 2),
    ("多用途戰機", "Multirole Fighter", "", "aircraft", 2),
    ("噴射機", "Jet", "", "aircraft", 1),
    ("螺旋槳飛機", "Propeller Aircraft", "", "aircraft", 1),

    # 直升機
    ("攻擊直升機", "Attack Helicopter", "", "aircraft", 2),
    ("運輸直升機", "Transport Helicopter", "", "aircraft", 1),
    ("偵察直升機", "Reconnaissance Helicopter", "", "aircraft", 2),
    ("搜救直升機", "Search and Rescue Helicopter", "SAR", "aircraft", 2),
    ("反潛直升機", "Anti-Submarine Helicopter", "", "aircraft", 2),
    ("武裝直升機", "Gunship", "", "aircraft", 2),

    # 飛彈
    ("空對空飛彈", "Air-to-Air Missile", "AAM", "weapon", 2),
    ("空對地飛彈", "Air-to-Ground Missile", "AGM", "weapon", 2),
    ("空對艦飛彈", "Air-to-Ship Missile", "ASM", "weapon", 2),
    ("反輻射飛彈", "Anti-Radiation Missile", "ARM", "weapon", 2),
    ("紅外線飛彈", "Infrared Missile", "IR", "weapon", 2),
    ("雷達導引飛彈", "Radar-Guided Missile", "", "weapon", 2),
    ("短程飛彈", "Short-Range Missile", "", "weapon", 2),
    ("中程飛彈", "Medium-Range Missile", "", "weapon", 2),
    ("長程飛彈", "Long-Range Missile", "", "weapon", 2),
    ("巡弋飛彈", "Cruise Missile", "CM", "weapon", 2),

    # 炸彈
    ("炸彈", "Bomb", "", "weapon", 1),
    ("自由落體炸彈", "Free-Fall Bomb", "", "weapon", 2),
    ("精確導引炸彈", "Precision-Guided Bomb", "PGM", "weapon", 2),
    ("雷射導引炸彈", "Laser-Guided Bomb", "LGB", "weapon", 2),
    ("GPS導引炸彈", "GPS-Guided Bomb", "", "weapon", 2),
    ("集束炸彈", "Cluster Bomb", "", "weapon", 2),
    ("燃燒彈", "Incendiary Bomb", "", "weapon", 2),
    ("核彈", "Nuclear Bomb", "", "weapon", 2),
    ("氫彈", "Hydrogen Bomb", "", "weapon", 2),
    ("深水炸彈", "Depth Charge", "", "weapon", 2),

    # 機砲和機槍
    ("機砲", "Cannon", "", "weapon", 1),
    ("機槍", "Machine Gun", "MG", "weapon", 1),
    ("機關槍", "Autocannon", "", "weapon", 2),
    ("迴旋機砲", "Rotary Cannon", "", "weapon", 2),

    # 火箭
    ("火箭彈", "Rocket", "", "weapon", 1),
    ("空對地火箭", "Air-to-Ground Rocket", "", "weapon", 2),
    ("火箭發射器", "Rocket Pod", "", "weapon", 2),

    # 飛行系統
    ("引擎", "Engine", "", "system", 1),
    ("噴射引擎", "Jet Engine", "", "system", 2),
    ("渦輪引擎", "Turbine", "", "system", 2),
    ("推進器", "Thruster", "", "system", 2),
    ("機翼", "Wing", "", "system", 1),
    ("機身", "Fuselage", "", "system", 2),
    ("機尾", "Tail", "", "system", 1),
    ("垂直尾翼", "Vertical Stabilizer", "", "system", 2),
    ("水平尾翼", "Horizontal Stabilizer", "", "system", 2),
    ("副翼", "Aileron", "", "system", 2),
    ("升降舵", "Elevator", "", "system", 2),
    ("方向舵", "Rudder", "", "system", 2),
    ("襟翼", "Flap", "", "system", 2),
    ("起落架", "Landing Gear", "", "system", 2),
    ("駕駛艙", "Cockpit", "", "system", 1),
    ("座艙", "Canopy", "", "system", 2),
    ("彈射座椅", "Ejection Seat", "", "system", 2),

    # 航電系統
    ("雷達", "Radar", "", "system", 1),
    ("火控雷達", "Fire Control Radar", "FCR", "system", 2),
    ("搜索雷達", "Search Radar", "", "system", 2),
    ("地形跟蹤雷達", "Terrain-Following Radar", "TFR", "system", 2),
    ("電子戰系統", "Electronic Warfare System", "EW", "system", 2),
    ("雷達警告接收器", "Radar Warning Receiver", "RWR", "system", 2),
    ("干擾器", "Jammer", "", "system", 2),
    ("誘餌發射器", "Chaff Dispenser", "", "system", 2),
    ("紅外線誘餌", "Flare", "", "system", 2),
    ("瞄準系統", "Targeting System", "", "system", 2),
    ("頭盔瞄準具", "Helmet-Mounted Sight", "HMS", "system", 2),
    ("抬頭顯示器", "Head-Up Display", "HUD", "system", 2),
    ("多功能顯示器", "Multi-Function Display", "MFD", "system", 2),
    ("導航系統", "Navigation System", "", "system", 1),
    ("GPS", "Global Positioning System", "GPS", "system", 1),
    ("慣性導航", "Inertial Navigation", "INS", "system", 2),
    ("自動駕駛", "Autopilot", "", "system", 2),

    # 飛行員和機組
    ("飛行員", "Pilot", "", "personnel", 1),
    ("王牌飛行員", "Ace", "", "personnel", 2),
    ("副駕駛", "Co-Pilot", "", "personnel", 1),
    ("導航員", "Navigator", "", "personnel", 2),
    ("武器官", "Weapon System Officer", "WSO", "personnel", 2),
    ("機組人員", "Aircrew", "", "personnel", 1),
    ("地勤人員", "Ground Crew", "", "personnel", 1),
    ("維修人員", "Maintenance Crew", "", "personnel", 1),

    # 飛行操作
    ("起飛", "Takeoff", "", "operation", 1),
    ("降落", "Landing", "", "operation", 1),
    ("著陸", "Touch Down", "", "operation", 1),
    ("盤旋", "Circle", "", "operation", 1),
    ("爬升", "Climb", "", "operation", 1),
    ("俯衝", "Dive", "", "operation", 1),
    ("滾轉", "Roll", "", "operation", 2),
    ("迴轉", "Turn", "", "operation", 1),
    ("迴避", "Evade", "", "operation", 2),
    ("追擊", "Pursuit", "", "operation", 2),
    ("纏鬥", "Dogfight", "", "operation", 2),
    ("空中加油", "Aerial Refueling", "AAR", "operation", 2),
    ("編隊飛行", "Formation Flight", "", "operation", 2),
    ("巡航", "Cruise", "", "operation", 1),
    ("巡邏", "Patrol", "", "operation", 1),
    ("偵察", "Reconnaissance", "RECON", "operation", 2),
    ("轟炸", "Bombing", "", "operation", 1),
    ("投彈", "Bomb Drop", "", "operation", 1),
    ("掃射", "Strafe", "", "operation", 2),
    ("空襲", "Air Strike", "", "operation", 1),
    ("空中支援", "Air Support", "AS", "operation", 1),
    ("近距空中支援", "Close Air Support", "CAS", "operation", 2),
    ("空中攔截", "Air Intercept", "AI", "operation", 2),
    ("空中優勢", "Air Superiority", "", "tactical", 2),
    ("制空權", "Air Supremacy", "", "tactical", 2),

    # 飛行參數
    ("高度", "Altitude", "", "parameter", 1),
    ("速度", "Speed", "", "parameter", 1),
    ("音速", "Speed of Sound", "", "parameter", 2),
    ("超音速", "Supersonic", "", "parameter", 2),
    ("亞音速", "Subsonic", "", "parameter", 2),
    ("馬赫", "Mach", "", "parameter", 2),
    ("航程", "Range", "", "parameter", 1),
    ("續航力", "Endurance", "", "parameter", 2),
    ("升限", "Ceiling", "", "parameter", 2),
    ("爬升率", "Rate of Climb", "", "parameter", 2),
    ("G力", "G-Force", "", "parameter", 2),

    # 機場設施
    ("機場", "Airfield", "", "facility", 1),
    ("空軍基地", "Air Base", "", "facility", 1),
    ("跑道", "Runway", "RWY", "facility", 1),
    ("滑行道", "Taxiway", "", "facility", 2),
    ("停機坪", "Apron", "", "facility", 2),
    ("機庫", "Hangar", "", "facility", 1),
    ("塔台", "Control Tower", "", "facility", 1),
    ("航管", "Air Traffic Control", "ATC", "facility", 2),
]


def generate_vocabulary_json():
    """生成完整的詞彙 JSON"""

    # 讀取現有詞彙
    with open('/home/user/MilP/data/vocabulary.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_vocab = data['vocabulary']

    # 生成新詞彙
    new_vocab = []

    # 通用術語
    for idx, (ch, en, abbr, subcat, diff) in enumerate(general_terms, start=31):
        new_vocab.append({
            "id": f"gen{idx:03d}",
            "chinese": ch,
            "english": en,
            "abbreviation": abbr,
            "category": "general",
            "subcategory": subcat,
            "difficulty": diff,
            "examples": {
                "chinese": f"{ch}在軍事作戰中很重要。",
                "english": f"{en} is important in military operations."
            }
        })

    # 陸軍術語
    for idx, (ch, en, abbr, subcat, diff) in enumerate(army_terms, start=21):
        new_vocab.append({
            "id": f"army{idx:03d}",
            "chinese": ch,
            "english": en,
            "abbreviation": abbr,
            "category": "army",
            "subcategory": subcat,
            "difficulty": diff,
            "examples": {
                "chinese": f"{ch}是陸軍的重要裝備。",
                "english": f"{en} is important equipment for the army."
            }
        })

    # 海軍術語
    for idx, (ch, en, abbr, subcat, diff) in enumerate(navy_terms, start=21):
        new_vocab.append({
            "id": f"navy{idx:03d}",
            "chinese": ch,
            "english": en,
            "abbreviation": abbr,
            "category": "navy",
            "subcategory": subcat,
            "difficulty": diff,
            "examples": {
                "chinese": f"{ch}在海戰中發揮重要作用。",
                "english": f"{en} plays an important role in naval warfare."
            }
        })

    # 空軍術語
    for idx, (ch, en, abbr, subcat, diff) in enumerate(airforce_terms, start=21):
        new_vocab.append({
            "id": f"air{idx:03d}",
            "chinese": ch,
            "english": en,
            "abbreviation": abbr,
            "category": "airforce",
            "subcategory": subcat,
            "difficulty": diff,
            "examples": {
                "chinese": f"{ch}是現代空戰的關鍵。",
                "english": f"{en} is key to modern air combat."
            }
        })

    # 合併詞彙
    all_vocab = existing_vocab + new_vocab

    # 更新 metadata
    result = {
        "metadata": {
            "version": "2.0.0",
            "lastUpdated": str(date.today()),
            "totalTerms": len(all_vocab),
            "categories": ["general", "army", "navy", "airforce"]
        },
        "vocabulary": all_vocab
    }

    return result


if __name__ == "__main__":
    print("生成軍事詞彙資料庫...")
    vocab_data = generate_vocabulary_json()

    # 輸出到檔案
    output_file = '/home/user/MilP/data/vocabulary.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 完成！總共 {vocab_data['metadata']['totalTerms']} 個詞彙")
    print(f"✓ 檔案已儲存到: {output_file}")
