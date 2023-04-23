import os

# url for user_data api
URL_USR = "https://api.syosetu.com/userapi/api"

"""payload for user_data api
u:  userid           ユーザーID
n:  name             ユーザー名
nc: novel_cnt        小説投稿数
rc: review_cnt       レビュー投稿数
nl: novel_length     小説累計文字数。スペース、改行はカウントしない
sg: sum_global_point 総合評価ポイントの合計
"""
PAYLOAD_USR = {"of": "u-n-nc-rc-nl-sg", "out": "json"}

# url for novel_data api
URL_NOVEL = "https://api.syosetu.com/novelapi/api"

"""payload for novel_data api
t:   title               タイトル
n:   ncode               Nコード
u:   userid              ユーザーID
s:   story               あらすじ
bg:  biggenre            大ジャンル
g:   genre               ジャンル
gf:  general_firstup     初回掲載日(YYYY-MM-DD HH:MM:SS)
gl:  general_lastup      最終掲載日(YYYY-MM-DD HH:MM:SS)
nt:  noveltype           連載の場合は1, 短編の場合は2
e:   end                 短編と完結済み小説は0, 連載中は1
ga:  general_all_no      全掲載部数。短編は1
l:   length              小説文字数。スペース改行はカウントしない
i:   isstop              長期掲載停止中は1, それ以外は0
gp:  global_point        総合ポイント(=(ブックマーク数×2)+評価ポイント)
dp:  daily_point         日刊ポイント
wp:  weekly_point        週間ポイント
mp:  monthly_point       月間ポイント
qp:  quarter_point       四半期ポイント
yp:  yearly_point        年間ポイント
f:   fav_novel_cnt       ブックマーク数
imp: impression_cnt      感想数
r:   review_cnt          レビュー数
a:   all_point           評価ポイント
ah:  all_hyoka_cnt       評価者数
"""
PAYLOAD_NOVEL = {
    "of": "t-n-u-s-bg-g-gf-gl-nt-e-ga-l-i-gp-dp-wp-mp-qp-yp-f-imp-r-a-ah",
    "out": "json",
}


URL_PVS = "https://kasasagi.hinaproject.com/access/chapter/ncode/%s/?date=%s"

URL_PVS_PER_DAY = "https://kasasagi.hinaproject.com/access/dayunique/ncode/%s/?month=%s"

URL_NOVEL_PAGE = "https://ncode.syosetu.com/{ncode}/"


CACHE_DIR = os.path.join(os.path.dirname(__file__), "datas")
# CACHE_DIR = "/root/others/NarouDataAPI/datas"

AGENT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
}

TPL_DIR = os.path.join(os.path.dirname(__file__), "templates")
TPL_USER_INFO_OUTPUT = "user_info.tpl"
TPL_NOVEL_INFO_OUTPUT = "novel_info.tpl"
