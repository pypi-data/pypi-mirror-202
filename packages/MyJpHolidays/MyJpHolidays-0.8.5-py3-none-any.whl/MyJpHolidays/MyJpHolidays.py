# 更新日 2023.04.14
#
# MyJpHolidays	v0.8.5
#

import datetime
import re
import numpy as np
import configparser
import os

gOneDay : object
g1stDoFlag : bool = False

vConfigFileName : str = "configCTJH.ini"

#################################################################
def 秋分の日と春分の日の計算_new_2( v年 : int, v月: int ):
    # 更新日： 2023/2/28
    # マクロ作成日 : 2023/2/14
    # マクロ修正日 : 2023/2/14
    # 単独実行 : 不可
    # これがおすすめ！！！
    # 対応期間：    1980-2150年

    春分の日_day : int = 0
    秋分の日_day : int = 0
    vAns : int = 0
    vMsg : str = ""

    if (v月 == 3):
        if ((v年 >= 1980) & (v年 <= 2099)) :
            春分の日_day = int(20.8431 + 0.242194 * (v年 - 1980) - int((v年 - 1980) / 4))
        else:
            if ((v年 >= 2100) & (v年 <= 2150)) :
                春分の日_day = int(21.851 + 0.242194 * (v年 - 1980) - int((v年 - 1980) / 4))
            else:
                vMsg = "err !!! - 3 @秋分の日と春分の日の計算_new_2"
                print(vMsg)
        vAns = 春分の日_day
    
    if (v月 == 9):
        if ((v年 >= 1980) & (v年 <= 2099)) :
            秋分の日_day = int(23.2488 + 0.242194 * (v年 - 1980) - int((v年 - 1980) / 4))
        else:
            if ((v年 >= 2100) & (v年 <= 2150)) :
                秋分の日_day = int(24.2488 + 0.242194 * (v年 - 1980) - int((v年 - 1980) / 4))
            else:
                vMsg = "err !!! - 9 @秋分の日と春分の日の計算_new_2"
                print(vMsg)
        vAns = 秋分の日_day
        
    return vAns
    

#################################################################
def happyMonday_日にち計算(vYear : int, vMonth : int, vWeekNumOfMonday: int):
    vWeek : str = ["月", "火", "水", "木", "金", "土", "日"]
    vDay : int = 0
    vNum : int = 0
    vDate : datetime
    vAddNum : int = 0
    vDOW : int = 0
    vWeekName : str = ""

    vDay = 1
    vDate = datetime.datetime( year = vYear, month = vMonth, day = vDay )
    # 曜日を調べる
    vDOW = vDate.weekday()       # 月曜日 --> 0, 火曜日 -->1, 水曜日 -->2, , , ,       # 日曜=0～土曜=6
    vWeekName = vWeek[vDOW]

    if (vWeekName == "日"):
        vAddNum = 1
    elif (vWeekName == "月"):
        vAddNum = 0
    elif (vWeekName == "火"):
        vAddNum = 6
    elif (vWeekName == "水"):
        vAddNum = 5
    elif (vWeekName == "木"):
        vAddNum = 4
    elif (vWeekName == "金"):
        vAddNum = 3
    elif (vWeekName == "土"):
        vAddNum = 2
    vDay = vDay + vAddNum
    vDate = datetime.datetime( year = vYear, month = vMonth, day = vDay )

    vNum = 1
    while (vNum < vWeekNumOfMonday):            # while ((not vNum) == vWeekNumOfMonday):
        vDay = vDay + 7
        vDate = datetime.datetime( year = vYear, month = vMonth, day = vDay )
        vNum += 1

    return vDate


#################################################################
#
# 自分用の特別休暇の設定を加える    …   年末年始休み、等
#
# 割り切って設定します、yearは後に設定する
#
vConfigHoliday : str
ori_SYUKUJITSU_Name = []
ori_Date_1 = []
ori_Date_2 = []
ori_Month = []
ori_Day = []
vTemp_ori_SYUKUJITSU_Name : str = ""
vTemp_ori_Date_1 : str = ""
vTemp_ori_Month : int = 0
vTemp_ori_Day : int = 0
vINI_Path : str
vIsFileFlag : bool
vIniFileExistFlag : bool


# ファイルが存在するかを調べる
vINI_Path = './' + vConfigFileName
vIsFileFlag = os.path.isfile(vINI_Path)
if vIsFileFlag:
    vIniFileExistFlag = True
else:
    # ファイルが存在しない場合、新規にiniファイルを作成する
    with open(vConfigFileName, 'w') as f:
        # defaultの設定を書く
        f.writelines("[Original_Holidays]\n")
        f.writelines("01/01 = 年始休み4\n")
        f.writelines("01/02 = 年始休み5\n")
        f.writelines("01/03 = 年始休み6\n")
        f.writelines("12/29 = 年末休み1\n")
        f.writelines("12/30 = 年末休み2\n")
        f.writelines("12/31 = 年末休み3\n")
        vIniFileExistFlag = True
        pass

if (vIniFileExistFlag):
    ori = {}
    config : object = configparser.ConfigParser()    # パーサの生成
    config.read('configCTJH.ini')     #  INIファイルの読み込み
    if 'Original_Holidays' in config:

        ori = config['Original_Holidays']

        # 一覧の表示
        for vConfigHoliday in ori.keys():

            # オリジナル祝日ネームの(仮)登録
            vTemp_ori_SYUKUJITSU_Name = config['Original_Holidays'][vConfigHoliday]
            ori_SYUKUJITSU_Name.append(vTemp_ori_SYUKUJITSU_Name)
            
            # オリジナル祝日の日付の(仮)登録
            vTemp_ori_Date_1 = vConfigHoliday
            vTemp_ori_Month = int(re.findall('\d+', vConfigHoliday)[0])
            vTemp_ori_Day = int(re.findall('\d+', vConfigHoliday)[1])
            ori_Date_1.append(vTemp_ori_Date_1)
            ori_Month.append(vTemp_ori_Month)
            ori_Day.append(vTemp_ori_Day)



#################################################################
def Calc_Date_To_SYUKUJITSUMEI(vDate : datetime):
    #
    # 更新日：  2023/04/08
    # 
    
    # 開発方針の変更
    #
    # 祝日の元データの塊_1 : 年末年始休み以外の休み
    # 祝日の元データの塊_2 : 年末年始休みのみ
    #
    # 処理的には    塊_1の処理　→　塊_2の処理　をする流れ
    # これで、年末年始休みよりも普通の祝日が優先されるはず！

    # 令和以降に対応-2
    # 平成32年（2021年）に限り…
    #「海の日」は7月22日に、「体育の日（スポーツの日）」は7月23日に、「山の日」は8月8日・8月9日(振替休日)になります。
    # 平成3?年?月?日に公布

    # 令和以降に対応-1
    # 国民の祝日に関する法律（昭和２３年法律第１７８号）の特例について
    # 平成32年（2020年）に限り…
    #「海の日」は7月23日に、「体育の日（スポーツの日）」は7月24日に、「山の日」は8月10日になります。
    # 平成32年（2020年）以降、「体育の日」は「スポーツの日」になります。 平成30年6月20日に公布
    #
    # *********************************************
    # 祝日であるかを調べて、ある場合はその祝日の名前を返す。
    # *********************************************
    # 国民の祝日
    #
    # 元日：1月1日
    # 成人の日：1月15日   --> ～ 1999年
    # 成人の日：1月第2月曜日   --> 2000年～
    #
    # 建国記念の日：2月11日
    # 令和天皇誕生日：2月23日  --> 2020年～
    #
    # 春分の日: 春分日
    #
    # 昭和天皇誕生日：4月29日   --> 1948年～1988年
    # みどりの日：4月29日    --> 1989年～2006年
    # 昭和の日：4月29日   --> 2007年～
    # 憲法記念日：5月3日
    # みどりの日：5月4日    --> 2007年～
    # こどもの日：5月5日
    #
    # 海の日：7月20日  --> 1996年～2002年
    # 海の日：7月第3月曜日  --> 2003年～
    #
    # 山の日：  8月11日  --> 2015年～
    #
    # 敬老の日：9月15日     ～2002年
    # 敬老の日：9月第3月曜日
    # 秋分の日: 秋分日      9月xx日
    #
    # 体育の日：10月10日    1966～1999
    # 体育の日：10月第2月曜日   2000～
    #
    # 文化の日：11月3日
    # 勤労感謝の日：11月23日
    #
    # 天皇誕生日：12月23日  --> 1989-2018   2019年以降廃止
    #
    # **** 2019年だけ施行 **************************
    # 休日              ：4月30日
    # 天皇の即位の日    ：5月1日
    # 休日              ：5月2日
    # 即位礼正殿の儀    ：10月22日
    # **********************************************
    # *
    # **** 2020年だけ施行 **************************
    # 祝日の移動:
    # 海の日                    ⇒7月23日
    # (体育の日)スポーツの日    ⇒7月24日
    # 山の日                    ⇒8月10日
    # **********************************************
    # *
    # **** 2021年だけ施行 **************************
    # 祝日の移動:
    # 海の日                    ⇒7月22日
    # (体育の日)スポーツの日    ⇒7月23日
    # 山の日                    ⇒8月8日
    # **********************************************
    # 前後が祝日である平日は、国民の休日となり、休日となる。   国民の休日
    #
    # 2018年（平成30年）6月20日に国民の祝日に関する法律（祝日法、昭和23年7月20日法律第178号）が改正され、
    # 2020年（令和2年）1月1日に施行されたことで、体育の日が「スポーツの日」に変更された。
    #
    # '山の日（やまのひ）は、日本の国民の祝日の一つである。日付は8月11日。2016年（平成28年）1月1日施行の改正祝日法で新設された。


    # vSYUKUJITSU_HENKAN : object             # 今の所、他では使ってないはず！！！
    # gOneDay : object                        # 今の所、他では使ってないはず！！！

    global gOneDay
    global g1stDoFlag

    vY2019Flag : bool = False
    vY2020Flag : bool = False
    vY2021Flag : bool = False
    # weekdayメソッドでは、月曜日を 0、日曜日を 6 として、曜日を整数で返します。
    vWeek : str = ["月", "火", "水", "木", "金", "土", "日"]
    vYear : int = 0
    vMonth : int = 0
    vDay : int = 0
    vLeapYear_Flag : bool = False
    vOneDayStr = ""
    vOneYear = []
    vYOUBIOfOneYear = []
    vTSUITACHI_HAIRETSU_Num : int = [0] * 12
    vCounter : int = 0          # i の代わり
    vSubCounter : int = 0       # ii の代わり
    vAns : str = ""
    vNum : int
    vYear_1 : int
    vYear_2 : int
    vMonth_2 : int
    vSYUNBUN_day : int
    vSYUUBUN_day : int
    i : int
    #vD : datetime
    vSYUKUJITU_NO_HINICHI_date : datetime
    vSYUKUJITU_NO_HINICHI_str : str
    vTempDate_str : str
    vSOEJI_1 : int
    vSOEJI_2 : int
    vSOEJI : int
    vWeekNumOfMonday : int
    vATARI_HANTEI_2 : bool
    vDoPassFlag : bool
    dow_2 : int = 0
    vWeekName_2 : str = ""
    vKENSAKU_BI_str : str
    vDayNumOfYear : int = 0
    vNumMaxForSH : int = 0
    vNumMaxForSH_2 : int = 41

    vYear_1 = vDate.year


    # g1stDoFlag方式で行く！！！


    # うるう年の判断
    if (((vYear_1 % 4) == 0) and ((not (vYear_1 % 100)) == 0) or ((vYear_1 % 400) == 0)):
        vLeapYear_Flag = True
    else:
        vLeapYear_Flag = False

    if (vLeapYear_Flag):
        vDayNumOfYear = 366
    else:
        vDayNumOfYear = 365


    if (g1stDoFlag==False):

        # 年の判断
        if (vYear_1 == 2019):
            vY2019Flag = True
        else:
            vY2019Flag = False
        #
        if (vYear_1 == 2020):
            vY2020Flag = True
        else:
            vY2020Flag = False
        #
        if (vYear_1 == 2021):
            vY2021Flag = True
        else:
            vY2021Flag = False
 
 
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 祝日の定義の配列
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # tSYUKUJITSU :
        # string Name           #祝日名
        # long Month            #祝日…月
        # long Day              #祝日…日
        # bool HappeyMondayFlag #ハッピーマンデーを調べる
        # long HappeyMonday_Num #上記が第何週目かの指定
        # bool YearCheckFlag    #施行開始年度の指定がある
        # long Year             #その年度
        # long Year_2           #施行年度の終わりの方の年度
        # bool Y2019Flag       #休日、天皇の即位の日、休日、即位礼正殿の儀
        # bool Y2020Flag       #海の日、スポーツの日、山の日の移動あり
        # bool Y2021Flag       #海の日、スポーツの日、山の日の移動あり
        # bool Y2019NotFlag    #2019年に使わないもの
        # bool Y2020NotFlag    #2020年に使わないもの
        # bool Y2021NotFlag    #2021年に使わないもの

        # 複合データ型の定義（１）
        # U12:最大長12のUnicode文字列
        # i1:1バイト整数(=np.int8)
        # f2:半精度浮動小数点数(=np.float16)
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 前回までは…振替休日の取れる日数を３日までしか考えていなかった
        # 2024年は５日も振替休日のある年で、うまくいかない＞＜
        # これを修正する…
        # 猶予を10日に変更する
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        dtype_tSYUKUJITSU = [("Name","U20"),("Month","i1"),("Day","i1"),
            ("HappeyMondayFlag","b1"),("HappeyMonday_Num","i1"),
            ("YearCheckFlag","b1"),("Year","i4"),("Year_2","i4"),
            ("Y2019Flag","b1"),("Y2020Flag","b1"),("Y2021Flag","b1"),
            ("Y2019NotFlag","b1"),("Y2020NotFlag","b1"),("Y2021NotFlag","b1")]       # ここはいじらなくて良い！！！

        # 構造化配列を作成（１）

        vTemp_SYUKUJITSU_HENKAN_Name = []
        vTemp_SYUKUJITSU_HENKAN_Name = ["元旦", "成人の日", "成人の日", "建国記念の日", "令和天皇誕生日",
            "春分の日", "昭和天皇誕生日", "みどりの日", "昭和の日", "憲法記念日", "みどりの日", "こどもの日", "海の日", "海の日", "山の日",
            "敬老の日", "敬老の日", "秋分の日", "体育の日", "体育の日","文化の日","勤労感謝の日", "平成天皇誕生日",
            "休日", "天皇の即位の日", "休日", "即位礼正殿の儀", "海の日", "スポーツの日", "山の日", "海の日", "スポーツの日", "山の日",
            "スポーツの日", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]		# 数ok2
        vNumMaxForSH = len(vTemp_SYUKUJITSU_HENKAN_Name)
        vSYUKUJITSU_HENKAN = np.zeros(vNumMaxForSH, dtype = dtype_tSYUKUJITSU)

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 構造化配列へのデータの書き込み（１）
        #
        # MonthもDayも0ならそれは使ってないと判断しよ
        #        
        vSYUKUJITSU_HENKAN["Name"] = vTemp_SYUKUJITSU_HENKAN_Name
        #   5
        #   10
        #   8
        #   10
        #   1, 10, 6, -6
        #
        #   5 + 10 + 8 + 10 + 10 + 6 + 1 = 13 + 30 + 6 + 1 - 6 = 44

        vSYUKUJITSU_HENKAN["Month"] = [1, 1, 1, 2, 2, 
            3, 4, 4, 4, 5, 5, 5, 7, 7, 8,
            9, 9, 9, 10, 10, 11, 11, 12,
            4, 5, 5, 10, 7, 7, 8, 7, 7, 8,
            10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]											#ok2

        vSYUKUJITSU_HENKAN["Day"] =  [1, 15, 0, 11, 23, 
            0, 29, 29, 29, 3, 4, 5, 20, 0, 11,
            15, 0, 0, 10, 0, 3, 23, 23,
            30, 1, 2, 22, 23, 24, 10, 22, 23, 8,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]											#ok2

        vSYUKUJITSU_HENKAN["HappeyMondayFlag"] = [False, False, True, False, False, 
            False, False, False, False, False, False, False, False, True, False,
            False, True, False, False, True, False, False, False,
            False, False, False, False, False, False, False, False, False, False,
            True, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["HappeyMonday_Num"] = [0, 0, 2, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 3, 0,
            0, 3, 0, 0, 2, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   											#ok2

        vSYUKUJITSU_HENKAN["YearCheckFlag"] = [False, True, True, False, True, 
            False, True, True, True, False, True, False, True, True, True,
            True, True, False, True, True, False, False, True,
            True, True, True, True, True, True, True, True, True, True,
            True, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Year"] = [0, 0, 2000, 0, 2020, 
            0, 1948, 1989, 2007, 0, 2007, 0, 1996, 2003, 2016,
            0, 2003, 0, 1966, 2000, 0, 0, 1989,
            2019, 2019, 2019, 2019, 2020, 2020, 2020, 2021, 2021, 2021,
            2022, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   										#ok2

        vSYUKUJITSU_HENKAN["Year_2"] = [0, 1999, 0, 0, 0, 
            0, 1988, 2006, 0, 0, 0, 0, 2002, 0, 0,
            2002, 0, 0, 1999, 2019, 0, 0, 2018,
            2019, 2019, 2019, 2019, 2020, 2020, 2020, 2021, 2021, 2021,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   											#ok2

        vSYUKUJITSU_HENKAN["Y2019Flag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False,
            True, True, True, True, False, False, False, False, False, False, 
            False, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Y2020Flag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False,
            False, False, False, False, True, True, True, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Y2021Flag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, True, True, True,
            False, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Y2019NotFlag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, True, False, False,
            False, False, False, True, False, False, False, False,
            False, False, False, False, True, True, True, True, True, True,
            False, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Y2020NotFlag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, True, True, True,
            False, False, False, True, True, False, False, False,
            True, True, True, True, False, False, False, True, True, True,
            False, False, False, False, False, False, False, False, False, False, False]   #ok2

        vSYUKUJITSU_HENKAN["Y2021NotFlag"] = [False, False, False, False, False, 
            False, False, False, False, False, False, False, True, True, True,
            False, False, False, True, True, False, False, False,
            True, True, True, True, True, True, True, False, False, False,
            False, False, False, False, False, False, False, False, False, False, False]   #ok2



        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        #
        # Name が" "の物は使ってないと判断する
        # MonthもDayも0ならそれは使ってないと判断しよ   --> 国民の休日で使う予定
        #

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

        for vNum in range(0, vNumMaxForSH):
            if (vSYUKUJITSU_HENKAN["Name"][vNum] == "春分の日"):
                vSYUNBUN_day = 秋分の日と春分の日の計算_new_2(vYear_1, 3)
                vSYUKUJITSU_HENKAN["Day"][vNum] = vSYUNBUN_day
                #break

            if (vSYUKUJITSU_HENKAN["Name"][vNum] == "秋分の日"):
                vSYUUBUN_day = 秋分の日と春分の日の計算_new_2(vYear_1, 9)
                vSYUKUJITSU_HENKAN["Day"][vNum] = vSYUUBUN_day
                #break

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        ########  完成
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 曜日を書く
        #
        vYear = vDate.year
        vMonth = 1
        vDay = 1

        vSubCounter = 1     # ２番目からスタート、１番目は0で OK

        for vCounter in range(vDayNumOfYear):
            #   にしむくさむらい　---> ２・４・６・９・１１の月は少ない
            # 1月　31日
            # 2月　28日（うるう年の場合29日）
            # 3月　31日
            # 4月　30日
            # 5月　31日
            # 6月　30日
            # 7月　31日
            # 8月　31日
            # 9月　30日
            # 10月　31日
            # 11月　30日
            # 12月　31日
            
            vOneDayStr = str(vYear) + "/"
            if (vMonth < 10):
                vOneDayStr += "0" + str(vMonth) + "/"
            else:
                vOneDayStr += str(vMonth) + "/"
            if (vDay < 10):
                vOneDayStr += "0" + str(vDay)
            else:
                vOneDayStr += str(vDay)
 

            vOneYear.append(vOneDayStr)     # 日付を登録

            # 日にちを調べる…
            vDT_2 : datetime = datetime.datetime(year=vYear, month=vMonth, day=vDay)       # xx月x日を作る
            # 曜日を調べる
            dow_2 = vDT_2.weekday()       # 月曜日 --> 0, 火曜日 -->1, 水曜日 -->2, , , ,
            vWeekName_2 = vWeek[dow_2]
            vYOUBIOfOneYear.append(vWeekName_2)     # 曜日を登録


            # 次の日の計算
            #
            if (( vMonth == 1 ) or  ( vMonth == 3 ) or ( vMonth == 5 )
                or ( vMonth == 7 ) or ( vMonth == 8 ) or ( vMonth == 10 )
                or ( vMonth == 12 )):
                #
                # 31日まである月
                #
                if ( vDay == 31 ):
                    vDay = 1
                    if ( vMonth == 12 ):
                        vMonth = 1
                        vYear += 1
                    else:
                        vMonth += 1
                        vTSUITACHI_HAIRETSU_Num[ vSubCounter ] = vCounter + 1    # 毎月の１日の位置を登録
                        vSubCounter += 1
                else:
                    vDay += 1
                
            else:
                if ( vMonth == 2 ):
                    # 28日か29日
  
                    # うるう年の判断
                    if (((vYear % 4) == 0) and ((not (vYear % 100)) == 0) or ((vYear % 400) == 0)):
                        vLeapYear_Flag = True
                    else:
                        vLeapYear_Flag = False

                    if (vLeapYear_Flag ):
                        # 29日まである月
                        if ( vDay == 29 ):
                            vDay = 1
                            vMonth += 1
                            vTSUITACHI_HAIRETSU_Num[ vSubCounter ] = vCounter + 1    # 毎月の１日の位置を登録
                            vSubCounter += 1
                        else:
                            vDay += 1
                    else:
                        # 28日まである月
                        if ( vDay == 28 ):
                            vDay = 1
                            vMonth += 1
                            vTSUITACHI_HAIRETSU_Num[ vSubCounter ] = vCounter + 1    # 毎月の１日の位置を登録
                            vSubCounter += 1
                        else:
                            vDay += 1

                else:
                    if (( vMonth == 4 ) or  ( vMonth == 6 ) or ( vMonth == 9 )
                        or ( vMonth == 11 )):
                        #
                        # 30日まである月
                        #
                        if (vDay == 30):
                            vDay = 1
                            vMonth += 1
                            vTSUITACHI_HAIRETSU_Num[ vSubCounter ] = vCounter + 1    # 毎月の１日の位置を登録
                            vSubCounter += 1
                        else:
                            vDay += 1


        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # struct tOneDay :
        # long tNum                 #通し番号
        # DateTime tDate            #日付      -->     このままでは多分出来ないから、stringとして登録する
        # string tYOUBI             #曜日
        # bool tSYUKUJITSU_Flag     #祝日の時 true
        # string tSYUKUJITSU_Name   #祝日名

        # 複合データ型の定義（２）
        dtype_tOneDay = [("tNum","i2"),("tDate","U10"), ("tYOUBI","U2"), 
            ("tSYUKUJITSU_Flag","b1"),("tSYUKUJITSU_Name","U20")]

        # 複合配列の作成（２）
        gOneDay = np.zeros(vDayNumOfYear, dtype = dtype_tOneDay)


        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 構造化配列へのデータの書き込み（２）
        #
        gOneDay["tNum"] = [i for i in range(vDayNumOfYear)]
        gOneDay["tDate"] = vOneYear
        gOneDay["tYOUBI"] = vYOUBIOfOneYear
        gOneDay["tSYUKUJITSU_Flag"] = [False for i in range(vDayNumOfYear)]
        gOneDay["tSYUKUJITSU_Name"] = [" " for i in range(vDayNumOfYear)]

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # ここまでオッケー
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # ログファイルに書き込み_3
        #
        # 祝日の書き込み
        #

        for i in range(0, vNumMaxForSH):

            vDoPassFlag = False
            if (vY2019Flag):
                # 2019年の時
                if (vSYUKUJITSU_HENKAN["Y2019NotFlag"][i]):
                    # これをパスする
                    vDoPassFlag = True

            if (vY2020Flag):
                # 2020年の時
                if (vSYUKUJITSU_HENKAN["Y2020NotFlag"][i]):
                    # これをパスする
                    vDoPassFlag = True

            if (vY2021Flag):
                # 2021年の時
                if (vSYUKUJITSU_HENKAN["Y2021NotFlag"][i]):
                    # これをパスする
                    vDoPassFlag = True


            if (vDoPassFlag == False):
                vATARI_HANTEI_2 = False

                if (vSYUKUJITSU_HENKAN["YearCheckFlag"][i]):
                    #
                    # year check flag が立った時  --> yearチェックをする時
                    # --------------------------------------------------------------
                    
                    if ( vSYUKUJITSU_HENKAN["Year"][i] == 0 ):
                        if (not ( vSYUKUJITSU_HENKAN["Year_2"][i] == 0 )):

                            if ( vSYUKUJITSU_HENKAN["Year_2"][i] > 0 ):
                                
                                if ( vSYUKUJITSU_HENKAN["Year_2"][i] >= vYear_1 ):
                                    vATARI_HANTEI_2 = True

                    else:
                        if ( vSYUKUJITSU_HENKAN["Year"][i] > 0 ):
                            if ( vSYUKUJITSU_HENKAN["Year_2"][i] == 0 ):
                                if ( vSYUKUJITSU_HENKAN["Year"][i] <= vYear_1 ):
                                    vATARI_HANTEI_2 = True

                            else:
                                if ( vSYUKUJITSU_HENKAN["Year_2"][i] > 0 ):
                                    
                                    if ( vSYUKUJITSU_HENKAN["Year"][i] == vSYUKUJITSU_HENKAN["Year_2"][i]):
                                        if ( vSYUKUJITSU_HENKAN["Year"][i] == vYear_1 ):
                                            vATARI_HANTEI_2 = True

                                    if ( vSYUKUJITSU_HENKAN["Year"][i] < vSYUKUJITSU_HENKAN["Year_2"][i]):
                                        if ((vSYUKUJITSU_HENKAN["Year"][i] <= vYear_1) & (vYear_1 <= vSYUKUJITSU_HENKAN["Year_2"][i])):
                                            vATARI_HANTEI_2 = True

                                    if ( vSYUKUJITSU_HENKAN["Year"][i] > vSYUKUJITSU_HENKAN["Year_2"][i]):
                                        if ((vSYUKUJITSU_HENKAN["Year_2"][i] <= vYear_1) & (vYear_1 <= vSYUKUJITSU_HENKAN["Year"][i])):
                                            vATARI_HANTEI_2 = True

                    # --------------------------------------------------------------
                
                else:
                    #
                    # year CheckFlagが立ってない時  --> yearチェックをしない時
                    # --------------------------------------------------------------                
                    vATARI_HANTEI_2 = True
                    

                if (vATARI_HANTEI_2):
                    if (vSYUKUJITSU_HENKAN["HappeyMondayFlag"][i] == True):
                        vWeekNumOfMonday = vSYUKUJITSU_HENKAN["HappeyMonday_Num"][i]
                        vYear_2 = vYear_1
                        vMonth_2 = vSYUKUJITSU_HENKAN["Month"][i]

                        vSYUKUJITU_NO_HINICHI_date = happyMonday_日にち計算(vYear_2, vMonth_2, vWeekNumOfMonday)
                        vSYUKUJITU_NO_HINICHI_str = vSYUKUJITU_NO_HINICHI_date.strftime('%Y/%m/%d')     # これはこのままでOK    ex: 2023/01/05
                        vSYUKUJITSU_HENKAN["Day"][i] = vSYUKUJITU_NO_HINICHI_date.day
                        
                        vSOEJI_1 = int(vTSUITACHI_HAIRETSU_Num[  vSYUKUJITSU_HENKAN["Month"][i] - 1  ])
                        vSOEJI_2 = int(vSYUKUJITSU_HENKAN["Day"][i] - 1)
                        vSOEJI = vSOEJI_1 + vSOEJI_2
                        vTempDate_str = gOneDay["tDate"][vSOEJI]            # vTempDate_str

                        if (vSYUKUJITU_NO_HINICHI_str == vTempDate_str):
                            gOneDay["tSYUKUJITSU_Flag"][vSOEJI] = True
                            if (gOneDay["tSYUKUJITSU_Name"][vSOEJI] == " "):
                                gOneDay["tSYUKUJITSU_Name"][vSOEJI] = vSYUKUJITSU_HENKAN["Name"][i]

                    else:
                        # vSYUKUJITSU_HENKAN["HappeyMondayFlag"][i] == False
                        #
                        vJobPassFlag = False
                        if ((vSYUKUJITSU_HENKAN["Month"][i] == 0) or (vSYUKUJITSU_HENKAN["Day"][i] == 0)):
                            #
                            # この場合は未使用と判断する！！！
                            #
                            vJobPassFlag = True


                        # ０の時はエラーになって変換が出来ないので対策を考える！！！
                        if (vJobPassFlag==False):
                                
                            vSYUKUJITU_NO_HINICHI_str = str(vYear_1) + "/"
                            if (vSYUKUJITSU_HENKAN["Month"][i] < 10):
                                vSYUKUJITU_NO_HINICHI_str += "0" + str(vSYUKUJITSU_HENKAN["Month"][i]) + "/"
                            else:
                                vSYUKUJITU_NO_HINICHI_str += str(vSYUKUJITSU_HENKAN["Month"][i]) + "/"
                            if (vSYUKUJITSU_HENKAN["Day"][i] < 10):
                                vSYUKUJITU_NO_HINICHI_str += "0" + str(vSYUKUJITSU_HENKAN["Day"][i])
                            else:
                                vSYUKUJITU_NO_HINICHI_str += str(vSYUKUJITSU_HENKAN["Day"][i])
                            # 文字列からdatetimeへの変換
                            vSYUKUJITU_NO_HINICHI_date = datetime.datetime.strptime(vSYUKUJITU_NO_HINICHI_str, '%Y/%m/%d')


                            vSOEJI_1 = int(vTSUITACHI_HAIRETSU_Num[  vSYUKUJITSU_HENKAN["Month"][i] - 1  ])
                            vSOEJI_2 = int(vSYUKUJITSU_HENKAN["Day"][i] - 1)
                            vSOEJI = vSOEJI_1 + vSOEJI_2

                        
                            vTempDate_str = gOneDay["tDate"][vSOEJI]

                            if (vSYUKUJITU_NO_HINICHI_str == vTempDate_str):
                                gOneDay["tSYUKUJITSU_Flag"][vSOEJI] = True
                                if (gOneDay["tSYUKUJITSU_Name"][vSOEJI] == " "):
                                    gOneDay["tSYUKUJITSU_Name"][vSOEJI] = vSYUKUJITSU_HENKAN["Name"][i]



        # ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
        #
        # このままの状態でBug取りをする
        
        #def Calc_国民の休日(vDate : datetime, vSYUKUJITSU_HENKAN, gOneDay):
        # 国民の休日を調べる
        # 前後が祝日である平日は、国民の休日となり、休日となる。
        # 1985年12月27日に祝日法が改正され、導入されたものである。

        vDate_middle_KOKUMIN : datetime
        vDate_middle_str_KOKUMIN : str
        vFlag_KOKUMIN : bool
        vYear_KOKUMIN : int
        vMonth_KOKUMIN : int
        vDay_KOKUMIN : int
        i_KOKUMIN : int = 0
        i_break_KOKUMIN : int = 0
        vSYUKUJITSU_Name_before_KOKUMIN : str
        vSYUKUJITSU_Name_middle_KOKUMIN : str
        vSYUKUJITSU_Name_after_KOKUMIN : str
        vCheck_HEIJITSU_Flag_KOKUMIN : bool
        vCheck_HEIJITSU_KOKUMIN : int

        # 1985年12月27日以降か？			比較対象の日にちは期限日以降か？
        #
        # 固定変数は全部大文字で書く習わしがある！！！
        #
        C_YEAR_KIGEN_KOKUMIN : int = 1985           # 期限の年            
        C_MONTH_KIGEN_KOKUMIN : int = 12            # 期限の月
        C_DAY_KIGEN_KOKUMIN = 27                    # 期限の日
        #
        vYear_KOKUMIN = vDate.year					# 比較対象の年
        vMonth_KOKUMIN = vDate.month				# 比較対象の月
        vDay_KOKUMIN = vDate.day                    # 比較対象の日


        if (vYear_KOKUMIN > C_YEAR_KIGEN_KOKUMIN):
            vFlag_KOKUMIN = True
        else:
            # vYear_KOKUMIN <= C_YEAR_KIGEN_KOKUMIN
            #
            if (vYear_KOKUMIN == C_YEAR_KIGEN_KOKUMIN):
                if (vMonth_KOKUMIN > C_MONTH_KIGEN_KOKUMIN):
                    vFlag_KOKUMIN = True
                else:
                    # vMonth_KOKUMIN <= C_MONTH_KIGEN_KOKUMIN
                    #
                    if (vMonth_KOKUMIN == C_MONTH_KIGEN_KOKUMIN):
                        if (vDay_KOKUMIN > C_DAY_KIGEN_KOKUMIN):
                            vFlag_KOKUMIN = True
                        else:
                            # vDay_KOKUMIN <= C_DAY_KIGEN_KOKUMIN
                            #
                            if (vDay_KOKUMIN == C_DAY_KIGEN_KOKUMIN):
                                vFlag_KOKUMIN = True
                            else:
                                # vDay_KOKUMIN < C_DAY_KIGEN_KOKUMIN
                                vFlag_KOKUMIN = False
                    else:
                        # vMonth_KOKUMIN < C_MONTH_KIGEN_KOKUMIN
                        vFlag_KOKUMIN = False
            else:
                # vYear_KOKUMIN < C_YEAR_KIGEN_KOKUMIN
                vFlag_KOKUMIN = False
            

        if (vFlag_KOKUMIN):
            #  1985年12月27日以降の場合…国民の休日を考慮する

            #  ログファイルに書き込み_1 … 空の所を探す              vNumMaxForSH_2
            for i_KOKUMIN in range(0, vNumMaxForSH_2):
                if (vSYUKUJITSU_HENKAN["Name"][i_KOKUMIN] == " "):
                    i_break_KOKUMIN = i_KOKUMIN
                    break
            
            # 国民の休日を書く
            vSYUKUJITSU_Name_before_KOKUMIN = ""
            vSYUKUJITSU_Name_middle_KOKUMIN = ""
            vSYUKUJITSU_Name_after_KOKUMIN = ""

            for i_KOKUMIN in range(0, vDayNumOfYear - 2):
                vDate_middle_str_KOKUMIN = gOneDay["tDate"][i_KOKUMIN + 1]          # 日付のstr
                vDate_middle_KOKUMIN = datetime.datetime.strptime(vDate_middle_str_KOKUMIN, "%Y/%m/%d")     # 文字列からdatetimeへの変換

                vSYUKUJITSU_Name_before_KOKUMIN = gOneDay["tSYUKUJITSU_Name"][i_KOKUMIN]
                vSYUKUJITSU_Name_middle_KOKUMIN = gOneDay["tSYUKUJITSU_Name"][i_KOKUMIN + 1]
                vSYUKUJITSU_Name_after_KOKUMIN = gOneDay["tSYUKUJITSU_Name"][i_KOKUMIN + 2]

                # 日曜日と祝日の日に関心があるから…
                #
                vCheck_HEIJITSU_Flag_KOKUMIN = False
                vCheck_HEIJITSU_KOKUMIN = vDate_middle_KOKUMIN.weekday()        # 月曜日 --> 0, 火曜日 -->1, 水曜日 -->2, , , , 日曜日 -->6

                if (vCheck_HEIJITSU_KOKUMIN == 6):      # 日曜日の時
                    vCheck_HEIJITSU_Flag_KOKUMIN = False
                else:                                   # その他の時
                    vCheck_HEIJITSU_Flag_KOKUMIN = True

                #その日が平日なら法則が成立するから…
                #
                if ( (not (vSYUKUJITSU_Name_before_KOKUMIN == " ")) and (vSYUKUJITSU_Name_middle_KOKUMIN == " ") and (not (vSYUKUJITSU_Name_after_KOKUMIN == " "))):
                    
                    if ( vCheck_HEIJITSU_Flag_KOKUMIN ):
                        # この時だけ、国民の休日になれる可能性がある！！！

                        vSYUKUJITSU_HENKAN["Name"][i_break_KOKUMIN] = "国民の休日"
                        vSYUKUJITSU_HENKAN["Month"][i_break_KOKUMIN] = vDate_middle_KOKUMIN.month
                        vSYUKUJITSU_HENKAN["Day"][i_break_KOKUMIN] = vDate_middle_KOKUMIN.day
                        vSYUKUJITSU_HENKAN["YearCheckFlag"][i_break_KOKUMIN] = True
                        vSYUKUJITSU_HENKAN["Year"][i_break_KOKUMIN] = 1985
                        vSYUKUJITSU_HENKAN["Year_2"][i_break_KOKUMIN] = 0
                        vSYUKUJITSU_HENKAN["HappeyMondayFlag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["HappeyMonday_Num"][i_break_KOKUMIN] = 0
                        vSYUKUJITSU_HENKAN["Y2019Flag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["Y2020Flag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["Y2021Flag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["Y2019NotFlag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["Y2020NotFlag"][i_break_KOKUMIN] = False
                        vSYUKUJITSU_HENKAN["Y2021NotFlag"][i_break_KOKUMIN] = False
                        i_break_KOKUMIN += 1

                        gOneDay["tSYUKUJITSU_Flag"][i_KOKUMIN + 1] = True
                        gOneDay["tSYUKUJITSU_Name"][i_KOKUMIN + 1] = "国民の休日";

                        vNumMaxForSH = i_break_KOKUMIN
                    

        # ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
        # Private Sub calc_振り替え休日(ByVal vDate As Date, ByRef vSYUKUJITSU_HENKAN() As tSYUKUJITSU, ByRef gOneDay() As tOneDay, ByRef oLog As Log)
                        
        # 更新日：2023/03/02
        #
        # 振り替え休日も考慮している。
        # 1973年～施行
        #
        #   連休が重なった時の振替休日にも対応した … ex: H27/5/3-6

        # weekdayメソッドでは、月曜日を 0、日曜日を 6 として、曜日を整数で返します。
        vWeek_FURIKAEKYUJITSU : str = ["月", "火", "水", "木", "金", "土", "日"]
        vWeek_FURIKAEKYUJITSU : str
        vSYUKUJITU_Name_FURIKAEKYUJITSU : str
        vFlag_FURIKAEKYUJITSU : bool
        vYear_FURIKAEKYUJITSU : int
        vMonth_FURIKAEKYUJITSU : int
        vDay_FURIKAEKYUJITSU : int
        i_FURIKAEKYUJITSU : int = 0
        i_save_FURIKAEKYUJITSU : int
        n_FURIKAEKYUJITSU : int
        nn_FURIKAEKYUJITSU : int
        nn_save_FURIKAEKYUJITSU : int
        vYOUBI_Name_FURIKAEKYUJITSU : str
        vN_For_RENKYUU_start_day_FURIKAEKYUJITSU : int
        vExitFlag_FURIKAEKYUJITSU : bool
        vTempDate_FURIKAEKYUJITSU : datetime
        vTemp_YOUBI_Name_FURIKAEKYUJITSU : str
        vTemp_SYUKUJITU_Name_FURIKAEKYUJITSU : str
        vTempDate_str_FURIKAEKYUJITSU : str
        vDate_FURIKAEKYUJITSU : datetime
        vWeekdayNum_FURIKAEKYUJITSU : int
        vFlag_1_FURIKAEKYUJITSU : bool
        vFlag_2_FURIKAEKYUJITSU : bool
        vFlag_3_FURIKAEKYUJITSU : bool

        # 1973年4月29日以降か？                比較対象の日にちは期限日以降か？
        #
        C_Year_KIGEN_FURIKAEKYUJITSU : int = 1973        # 期限の年
        C_Month_KIGEN_FURIKAEKYUJITSU : int = 4         # 期限の月
        C_Day_KIGEN_FURIKAEKYUJITSU : int = 29           # 期限の日
        #
        vYear_FURIKAEKYUJITSU = vDate.year                     # 比較対象の年
        vMonth_FURIKAEKYUJITSU = vDate.month                   # 比較対象の月
        vDay_FURIKAEKYUJITSU = vDate.day                       # 比較対象の日


        if (vYear_FURIKAEKYUJITSU > C_Year_KIGEN_FURIKAEKYUJITSU):
            vFlag_FURIKAEKYUJITSU = True
        else:
            # vYear_FURIKAEKYUJITSU <= C_Year_KIGEN_FURIKAEKYUJITSU
            #
            if (vYear_FURIKAEKYUJITSU == C_Year_KIGEN_FURIKAEKYUJITSU):
                if (vMonth_FURIKAEKYUJITSU > C_Month_KIGEN_FURIKAEKYUJITSU):
                    vFlag_FURIKAEKYUJITSU = True
                else:
                    # vMonth_FURIKAEKYUJITSU <= C_Month_KIGEN_FURIKAEKYUJITSU
                    #
                    if (vMonth_FURIKAEKYUJITSU == C_Month_KIGEN_FURIKAEKYUJITSU):
                        if (vDay_FURIKAEKYUJITSU > C_Day_KIGEN_FURIKAEKYUJITSU):
                            vFlag_FURIKAEKYUJITSU = True
                        else:
                            # vDay_FURIKAEKYUJITSU <= C_Day_KIGEN_FURIKAEKYUJITSU
                            #
                            if (vDay_FURIKAEKYUJITSU == C_Day_KIGEN_FURIKAEKYUJITSU):
                                vFlag_FURIKAEKYUJITSU = True
                            else:
                                # vDay_FURIKAEKYUJITSU < C_Day_KIGEN_FURIKAEKYUJITSU
                                vFlag_FURIKAEKYUJITSU = False
                    else:
                        # vMonth_FURIKAEKYUJITSU < C_Month_KIGEN_FURIKAEKYUJITSU
                        vFlag_FURIKAEKYUJITSU = False
            else:
                # vYear_FURIKAEKYUJITSU < C_Year_KIGEN_FURIKAEKYUJITSU
                vFlag_FURIKAEKYUJITSU = False
        

        if (vFlag_FURIKAEKYUJITSU == True):
            # ログファイルに書き込み_1 … 空の所を探す
            for i_FURIKAEKYUJITSU in range(0, vNumMaxForSH):
                if (vSYUKUJITSU_HENKAN["Name"][i_FURIKAEKYUJITSU] == " "):
                    break
            i_save_FURIKAEKYUJITSU = i_FURIKAEKYUJITSU


            # １年間の振休を調べる
            for n_FURIKAEKYUJITSU in range(0, vDayNumOfYear):

                # その日のデータを調べる
                vTempDate_str_FURIKAEKYUJITSU = gOneDay["tDate"][n_FURIKAEKYUJITSU]         # 日付のstr


                vDate_FURIKAEKYUJITSU = datetime.datetime.strptime(vTempDate_str_FURIKAEKYUJITSU, "%Y/%m/%d")     # 文字列からdatetimeへの変換
                vWeekdayNum_FURIKAEKYUJITSU = vDate_FURIKAEKYUJITSU.weekday()        # 月曜日 --> 0, 火曜日 -->1, 水曜日 -->2, , , , 日曜日 -->6
                vYOUBI_Name_FURIKAEKYUJITSU = vWeek_FURIKAEKYUJITSU[vWeekdayNum_FURIKAEKYUJITSU]
                vSYUKUJITU_Name_FURIKAEKYUJITSU = gOneDay["tSYUKUJITSU_Name"][n_FURIKAEKYUJITSU]
                
                #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                # if (vYOUBI_Name_FURIKAEKYUJITSU == "日") and (vSYUKUJITU_Name_FURIKAEKYUJITSU == (not " ")):
                #
                vFlag_1_FURIKAEKYUJITSU = True if (vYOUBI_Name_FURIKAEKYUJITSU == "日") else False
                vFlag_2_FURIKAEKYUJITSU = False if (vSYUKUJITU_Name_FURIKAEKYUJITSU == " ") else True
                if (vFlag_1_FURIKAEKYUJITSU == True) and (vFlag_2_FURIKAEKYUJITSU == True):
                #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
                
                    vN_For_RENKYUU_start_day_FURIKAEKYUJITSU = n_FURIKAEKYUJITSU        # 連休の始まりの日

                    #
                    # 小ループへ突入する
                    #
                    vExitFlag_FURIKAEKYUJITSU = False
                    nn_FURIKAEKYUJITSU = vN_For_RENKYUU_start_day_FURIKAEKYUJITSU + 1       # その次の日
                    nn_save_FURIKAEKYUJITSU = 0


                    while ((vExitFlag_FURIKAEKYUJITSU == False) and (nn_FURIKAEKYUJITSU < vDayNumOfYear)):

                        vTempDate_str_FURIKAEKYUJITSU = gOneDay["tDate"][nn_FURIKAEKYUJITSU]         # 日付のstr
                        vTempDate_FURIKAEKYUJITSU = datetime.datetime.strptime(vTempDate_str_FURIKAEKYUJITSU, "%Y/%m/%d")     # 文字列からdatetimeへの変換
                        vTemp_YOUBI_Name_FURIKAEKYUJITSU = gOneDay["tYOUBI"][nn_FURIKAEKYUJITSU]
                        vTemp_SYUKUJITU_Name_FURIKAEKYUJITSU = gOneDay["tSYUKUJITSU_Name"][nn_FURIKAEKYUJITSU]

                        # ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                        if (vTemp_SYUKUJITU_Name_FURIKAEKYUJITSU == " "):
                            vFlag_3_FURIKAEKYUJITSU = False
                        else:
                            vFlag_3_FURIKAEKYUJITSU = True
                        if (vFlag_3_FURIKAEKYUJITSU):           # 何か書かれている時は…
                        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

                            vExitFlag_FURIKAEKYUJITSU = False

                            nn_FURIKAEKYUJITSU += 1

                        else:
                            vExitFlag_FURIKAEKYUJITSU = True
                            nn_save_FURIKAEKYUJITSU = nn_FURIKAEKYUJITSU            # この日が振替休日になる

                            gOneDay["tSYUKUJITSU_Flag"][nn_save_FURIKAEKYUJITSU] = True
                            gOneDay["tSYUKUJITSU_Name"][nn_save_FURIKAEKYUJITSU] = "振り替え休日"

                            vSYUKUJITSU_HENKAN["Name"][i_save_FURIKAEKYUJITSU] = "振り替え休日"
                            vSYUKUJITSU_HENKAN["Month"][i_save_FURIKAEKYUJITSU] = vTempDate_FURIKAEKYUJITSU.month
                            vSYUKUJITSU_HENKAN["Day"][i_save_FURIKAEKYUJITSU] = vTempDate_FURIKAEKYUJITSU.day
                            vSYUKUJITSU_HENKAN["YearCheckFlag"][i_save_FURIKAEKYUJITSU] = False
                            vSYUKUJITSU_HENKAN["Year"][i_save_FURIKAEKYUJITSU] = 0
                            vSYUKUJITSU_HENKAN["Year_2"][i_save_FURIKAEKYUJITSU] = 0
                            vSYUKUJITSU_HENKAN["HappeyMondayFlag"][i_save_FURIKAEKYUJITSU] = False
                            vSYUKUJITSU_HENKAN["HappeyMonday_Num"][i_save_FURIKAEKYUJITSU] = 0

                            i_save_FURIKAEKYUJITSU += 1
                            vNumMaxForSH = i_save_FURIKAEKYUJITSU + 1
                            n_FURIKAEKYUJITSU = nn_FURIKAEKYUJITSU + 1



		# ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
		# private void Calc_オリジナルの休み(DateTime vDate_OriginalHoliday, ref tSYUKUJITSU[] vSYUKUJITSU_HENKAN, ref tOneDay[] gOneDay, ref NewLog oLog, int vWriteType) {
		# 年末年始の休日も考慮している。
        #
        # 自分用の特別休暇の設定を加える    …   年末年始休み、等
        #
        i_OriginalHoliday : int


        # yearの設定をする
        vConfigYear : int = vYear_1
        
        # 年号を足します
        vMax_ConfigHolidays = len(ori_SYUKUJITSU_Name)
        ori_Date_2 = []
        for i in range(vMax_ConfigHolidays):
            vTemp_ori_Date_1 = ori_Date_1[i]
            vTemp_ori_Date_2 = str(vConfigYear) + "/" + vTemp_ori_Date_1
            ori_Date_2.append(vTemp_ori_Date_2)


        # vSYUKUJITSU_HENKAN["Name"][i]　には追加はしないでおく



        # オリジナルの休みを書く
        for i_OriginalHoliday in range(0, vDayNumOfYear):        # 1年間のループ
            vTempDate_str_OriginalHoliday = gOneDay["tDate"][i_OriginalHoliday]         # 日付のstr
            for m_OriginalHoliday in range(vMax_ConfigHolidays):     # オリジナル休暇の日数分のループ
                if (vTempDate_str_OriginalHoliday == ori_Date_2[m_OriginalHoliday]):
                    # 休み発見！！！
                    vTemp_Current_Name : str = gOneDay["tSYUKUJITSU_Name"][i_OriginalHoliday]
                    # スペースのみか？　( ＝　空欄か？ )
                    if (vTemp_Current_Name == " "):
                        gOneDay["tSYUKUJITSU_Name"][i_OriginalHoliday] = ori_SYUKUJITSU_Name[m_OriginalHoliday]


        # ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

        # print("data 作成 終わり")
        g1stDoFlag = True
        

    # １年間の配列から検索日を探す
    vKENSAKU_BI_str = vDate.strftime("%Y/%m/%d")
    for i  in range(0, vDayNumOfYear):
        vTempDate_str = str(gOneDay["tDate"][i])
        if (vTempDate_str == vKENSAKU_BI_str):
            vAns = gOneDay["tSYUKUJITSU_Name"][i]
            break

    return vAns



#################################################################
def YearToHolidays( vYear : int, vZeroOptionFlag : bool = False):
	#
	# vYear		        :	祝日を調べる年
    # vZeroOptionFlag   :   日付の数字が一桁の時に前の０を付けるかの選択
	#
	# 戻り値	        :	その年の祝日の配列（全て）
	# 				        自分の年末年始休みも混みです
	#

    global g1stDoFlag
    
    i : int = 0
    vDD_Max : int = 0
    vTempDate_str : str
    vTempDate : datetime
    vSYUKUJITSU_MEI_test : str = ""
    vMonth : int
    # weekdayメソッドでは、月曜日を 0、日曜日を 6 として、曜日を整数で返します。
    vWeek_Test : str = ["月", "火", "水", "木", "金", "土", "日"]
    vHoliday_Num_List = []
    vHoliday_Date_List = []
    vHoliday_YOUBI_List = []
    vHoliday_SYUKUJITSU_Name_List = []
    vHoliday : object
    tDate_TempStr_test : str
    vYOUBI_Name_test : str = ""
    ii_test : int = 0
    vLeapYear_Flag : bool = False


    # うるう年の判断
    if (((vYear % 4) == 0) and ((not (vYear % 100)) == 0) or ((vYear % 400) == 0)):
        vLeapYear_Flag = True
    else:
        vLeapYear_Flag = False


    for vMonth in range(1, 13):

        # g1stDoFlag方式で行く！！！
        g1stDoFlag = False

        
        #     にしむくさむらい　---> ２・４・６・９・１１の月は少ない
        #     2月　28日（うるう年の場合29日）

        vDD_Max = 0
        if (vMonth == 1):
            vDD_Max = 31
        elif (vMonth == 2):
            if (vLeapYear_Flag):
                vDD_Max = 29
            else:
                vDD_Max = 28
        elif (vMonth == 3):
            vDD_Max = 31
        elif (vMonth == 4):
            vDD_Max = 30
        elif (vMonth == 5):
            vDD_Max = 31
        elif (vMonth == 6):
            vDD_Max = 30
        elif (vMonth == 7):
            vDD_Max = 31
        elif (vMonth == 8):
            vDD_Max = 31
        elif (vMonth == 9):
            vDD_Max = 30
        elif (vMonth == 10):
            vDD_Max = 31
        elif (vMonth == 11):
            vDD_Max = 30
        elif (vMonth == 12):
            vDD_Max = 31

        for i in range(1, vDD_Max + 1):
            vTempDate_str = str(vYear) + "/" + str(vMonth) + "/" + str(i)         # 日付のstr
            vTempDate = datetime.datetime.strptime(vTempDate_str, "%Y/%m/%d")     # 文字列からdatetimeへの変換
            vWeekdayNum_Test = vTempDate.weekday()        # 月曜日 --> 0, 火曜日 -->1, 水曜日 -->2, , , , 日曜日 -->6
            vYOUBI_Name_test = vWeek_Test[vWeekdayNum_Test]

            vSYUKUJITSU_MEI_test = Calc_Date_To_SYUKUJITSUMEI(vTempDate)

            if (not (vSYUKUJITSU_MEI_test == " ")):
            	# その日が祝日ならば、、、
                
                #############################################################################
                # tDate_TempStr_test = str(vYear) + "/" + str(vMonth) + "/" + str(i)
                #
                tDate_TempStr_test = str(vYear) + "/"

                if (vZeroOptionFlag):
                    if (vMonth >= 10):
                        # 10以上の時
                        tDate_TempStr_test += str(vMonth) + "/"
                    else:
                        # 10未満の時
                        tDate_TempStr_test += "0" + str(vMonth) + "/"
                else:
                    tDate_TempStr_test += str(vMonth) + "/"

                if (vZeroOptionFlag):
                    if (i >= 10):
                        # 10以上の時
                        tDate_TempStr_test += str(i)
                    else:
                        # 10未満の時
                        tDate_TempStr_test += "0" + str(i)
                else:
                    tDate_TempStr_test += str(i)
                #############################################################################

                vHoliday_Num_List.append(ii_test)
                vHoliday_Date_List.append(tDate_TempStr_test)
                vHoliday_YOUBI_List.append(vYOUBI_Name_test)
                vHoliday_SYUKUJITSU_Name_List.append(vSYUKUJITSU_MEI_test)
                ii_test += 1

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 複合データ型の定義（３）
        # tDate は、stringとして登録する
        dtype_vHoliday = [("tNum","i2"),("tDate","U10"),("tYOUBI","U2"),("tSYUKUJITSU_Name","U20")]

        # 複合配列の作成（３）
        vHoliday = np.zeros(ii_test, dtype = dtype_vHoliday)

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # 複合配列へのデータの書き込み（３）
        vHoliday["tNum"] = vHoliday_Num_List
        vHoliday["tDate"] = vHoliday_Date_List
        vHoliday["tYOUBI"] = vHoliday_YOUBI_List
        vHoliday["tSYUKUJITSU_Name"] = vHoliday_SYUKUJITSU_Name_List

        # vHoliday 完成！！！

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
			

    return  vHoliday

