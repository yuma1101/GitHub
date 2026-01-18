# 必要なライブラリのインポート
import datetime         # 日付と時間を扱うためのライブラリ
import pandas as pd     # データ分析や操作を行うためのライブラリ
import streamlit as st  # Webアプリケーションを作成するためのライブラリ
import yfinance as yf   # Yahoo Financeから金融データを取得するためのライブラリ
import func             # カスタム関数が定義されている外部ファイル

# Webアプリのタイトルを設定
st.title("キノファイナンス教室")
# サイドバーにテキスト入力フィールドを追加（銘柄検索用）
search = st.sidebar.text_input('【銘柄検索】', '')
# 銘柄コードを含むCSVファイルを読み込み
stock_code = pd.read_csv("stock_codes.csv").astype('str')
# サイドバーに銘柄コードのデータフレームを表示（検索に基づいてフィルタリング）
st.sidebar.dataframe(stock_code[(stock_code['銘柄名'].str.contains(search)) | (stock_code['コード'].str.contains(search))], height = 150)
# サイドバーにテキスト入力フィールドを追加（銘柄コード入力用）
ticker = st.sidebar.text_input("銘柄コードを入力", '^N225')
if ticker.isdigit():
    ticker = ticker + '.T'
else:
    ticker

# 期間の取得（開始日と終了日）
start = st.sidebar.date_input("始まり", value=datetime.date(2002, 10, 1), min_value=datetime.date(1970, 1, 1))
end = st.sidebar.date_input("終わり", value=datetime.date.today())
# Yahoo Financeから株価データをダウンロード
symbol = yf.download(ticker, start, end, rounding=True)

# 「株価情報」のチェックボックスを表示
if st.checkbox("株価情報"):
    try:
        # ラジオボタンで表示する情報の種類を選択
        purpose = ["株価情報", "チャート", "シャープレシオ"]
        num = st.radio('確認したい情報をチェック', purpose, horizontal=True)

        # "株価情報"が選択された場合、株価のデータフレームを表示
        if num == purpose[0]:
            st.dataframe(symbol, 0, height=200)

        # "チャート"が選択された場合、株価チャートを表示
        if num == purpose[1]:
            fig = func.graph(symbol)  # funcモジュールのgraph関数を使用してチャートを生成
            st.pyplot(fig)            # Streamlitでチャートを表示

        # "シャープレシオ"が選択された場合、シャープレシオの計算と表示
        if num == purpose[2]:
            tickers = {ticker: ticker, '日経平均': '^N225'}  # ティッカーと市場指数の辞書を定義
            g_bonds = st.number_input('国債利回り(%)', 0.1, 0.9, 0.5) / 100  # 国債利回りの入力
            market_profit = st.number_input('マーケット利回り（%）', 2.0, 9.0, 4.5) / 100  # マーケット利回りの入力
            sharp = func.sharp_ratio(tickers, start, end, g_bonds, market_profit)  # シャープレシオの計算
            st.write(f"シャープレシオ(年間)は{sharp}です")  # 計算されたシャープレシオを表示
    except:
        st.write('この銘柄情報はありません')

# 「統計情報」のチェックボックスを表示
if st.checkbox('統計情報'):
    # 統計情報の種類をリストとして定義
    purpose = ['年', '四半期', '月', '週', '曜日', '日', '年初からの経過日数']
    # ラジオボタンを使って統計情報の種類を選択
    num = st.radio('過去の統計を確認', purpose, horizontal=True)
    # 選択した統計情報の計算を行う関数を呼び出し
    statistics = func.statistics(symbol)
    # 計算された統計情報をデータフレームとして表示
    st.dataframe(statistics[purpose.index(num)])

# 「分足csvの取得」のチェックボックスを表示
if st.checkbox('分足csvの取得'):
    # 分足の種類をリストとして定義
    mt = [1, 2, 5, 15, 30, 60, 90]
    # ドロップダウンメニューで分足の種類を選択
    num = st.selectbox('取得したい分足を選択', mt, index=0)
    # 選択した分足のデータを取得する関数を呼び出し
    kobetu = func.minutes(ticker, num)
    # 取得したデータをデータフレームとして表示
    st.dataframe(kobetu)
    # データフレームをCSV形式で出力し、ダウンロードリンクを生成
    csv = kobetu.to_csv(index=False)
    st.download_button('Download', data=csv, file_name=f"{ticker}_{num}min.csv")
