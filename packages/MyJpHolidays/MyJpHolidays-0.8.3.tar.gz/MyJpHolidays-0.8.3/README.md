# MyJpHolidays20230412
a Python Library, you can get a combined list for Japan-Holidays


## 概要
　調べたい年からその年の祝日名の調べて一覧を複合配列にして返します<br>
 
##  詳細の説明<br>
このlibraryは、簡単使用を意識して作りました  

同じディレクトリに保存されている"configCTJH.ini"を直接、word、等で開いて編集することで  
ご自分に合ったオリジナルの休みを設定出来ます、初期設定では12/29-1/3になっております  
尚、一度このlibraryを実行すると無い場合は自動的にiniファイルが作成されます、それを編集して下さい  
 
vHoliday : object = MyJpHolidays.YearToHolidays(vYear)  

vYear 年の祝日の一覧が複合配列にされて返ってきます  
オリジナルの休みも含みます  
通し番号、日付、曜日、祝日名の複合配列です  
要素の数は、len(vHoliday) で求められます  
複合配列内の日付は、strです、datetimeではありません  
アクセスの仕方はデモを参考にして下さい   

## インストール方法  
pip install MyJpHolidays  

## デモプログラム<br>
https://github.com/Supper-Smille/MyJpHolidays20230412/blob/main/demo.py
 
    
