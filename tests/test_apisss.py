import os
import sys

import responses

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "narou_data_api"))
print(sys.path)
from narou_data_api.api import Novel, PvChp, PvDay, SumPvChp, SumPvDate, User, get_impression

# from models import Novel


@responses.activate
def test_get_data():
    responses.add(
        responses.GET,
        "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=123456",
        status=200,
        body='[{"allcount":1},{"userid":"123456","name":"test_user","novel_cnt":10,"review_cnt":1,"novel_length":1000000,"sum_global_point":12345}]',
        content_type="application/json",
    )
    responses.add(
        responses.GET,
        "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=654321",
        status=500,
        body="",
        content_type="application/json",
    )

    # can get data
    test = [
        {"allcount": 1},
        {
            "userid": "123456",
            "name": "test_user",
            "novel_cnt": 10,
            "review_cnt": 1,
            "novel_length": 1000000,
            "sum_global_point": 12345,
        },
    ]
    result = User.get_by_userid("123456")
    print(str(result))
    assert 1 == 2
    # assert result == test

    ## status_code != 200
    # test = []
    # url = "https://api.syosetu.com/userapi/api"
    # params = {"of":"u-n-nc-rc-nl-sg", "out":"json", "userid":"654321"}
    # result = get_data(url, params)
    # assert result == test


# @responses.activate
def test_get_user_by_userid():
    # responses.add(
    #    responses.GET,
    #    "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=123456",
    #    status=200,
    #    body='[{"allcount":1},{"userid":"123456","name":"test_user","novel_cnt":10,"review_cnt":1,"novel_length":1000000,"sum_global_point":12345}]',
    #    content_type="application/json"
    # )
    # responses.add(
    #    responses.GET,
    #    "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=654321",
    #    status=200,
    #    body='[{"allcount":0}]',
    #    content_type="application/json"
    # )
    ## exist data
    # userid="123456"
    # test1 = [{"userid":"123456","name":"test_user","novel_cnt":10,"review_cnt":1,"novel_length":1000000,"sum_global_point":12345}]
    # result = User.get_by_userid(userid)
    ##assert result == test1
    # print(dir(result))
    #
    ## not exist data
    # userid="654321"
    # test2 = []
    # result = User.get_by_userid(userid)
    userid = 767713
    result = User.get_by_userid(userid)
    print(result.ncodes)
    assert result == test2


def test_get_posted_date():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    data = novel.get_posted_date()
    print(data)
    data = novel.get_posted_date(is_str=True)
    print(data)
    assert 1 == 2


def test_get_titles():
    novel_data = {
        "title": "機巧技師の俺がロリっ娘に《こころ》を教えることになったんだが",
        "ncode": "N8425FD",
        "userid": 767713,
        "story": "「こいつに感情を教えてくれ」\n\nそんな依頼で凌也の元にやってきたのは、ラルという美少女だ。\n\nだけど戦闘人形な上にポンコツで常識がない。意味不明な行動ばかりして、凌也は毎日頭を抱えていた。\n\n「顔が近いんだが……」\n「興奮、した……？」\n「してたまるか！」\n\nラルと過ごすドタバタな日々。しかしほかの戦闘人形も現れ、だんだんと不穏な空気に……？\nある意味純粋なラルを通して、凌也も自分を見つめ直していく。\n果たして凌也はラルに感情を教えることができるのか！\n\n――――\n\n第４回書き出し祭り総合９位「生徒は無敵のアンドロイド～人嫌い機巧師の感情指南」改稿版です\n",
        "biggenre": 2,
        "genre": 202,
        "general_firstup": "2018-12-01 00:06:40",
        "general_lastup": "2019-02-01 08:00:00",
        "noveltype": 1,
        "end": 1,
        "general_all_no": 22,
        "length": 94712,
        "isstop": 1,
        "global_point": 114,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 2,
        "fav_novel_cnt": 24,
        "impression_cnt": 3,
        "review_cnt": 0,
        "all_point": 66,
        "all_hyoka_cnt": 7,
    }
    novel = Novel(novel_data)
    # novel_data = {'title': '呪われ少女は不幸になりたい', 'ncode': 'N0919GA', 'userid': 767713, 'story': '「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。', 'biggenre': 3, 'genre': 302, 'general_firstup': '2020-02-05 11:48:37', 'general_lastup': '2020-03-12 20:00:00', 'noveltype': 1, 'end': 0, 'general_all_no': 41, 'length': 192239, 'isstop': 0, 'global_point': 249, 'daily_point': 0, 'weekly_point': 0, 'monthly_point': 0, 'quarter_point': 0, 'yearly_point': 6, 'fav_novel_cnt': 44, 'impression_cnt': 8, 'review_cnt': 3, 'all_point': 161, 'all_hyoka_cnt': 17}
    # novel = Novel(novel_data)
    data1, data2 = novel.get_titles()
    print(data1)
    print(data2)
    assert 1 == 2


@responses.activate
def test_get_novels_by_userid():
    responses.add(
        responses.GET,
        "https://api.syosetu.com/novelapi/api?of=t-n-u-s-bg-g-gf-gl-nt-e-ga-l-i-gp-dp-wp-mp-qp-yp-f-imp-r-a-ah&out=json&userid=123456",
        status=200,
        body='[{"allcount":2},{"title":"novel1","ncode":"N1234GP","userid":123456,"story":"あらすじ１行目\nあらすじ2行目","biggenre":3,"genre":302,"general_firstup":"2022-01-10 10:01:11","general_lastup":"2022-01-11 11:11:11","noveltype":1,"end":0,"general_all_no":41,"length":190000,"isstop":0,"global_point":250,"daily_point":0,"weekly_point":0,"monthly_point":0,"quarter_point":0,"yearly_point":0,"fav_novel_cnt":44,"impression_cnt":8,"review_cnt":3,"all_point":161,"all_hyoka_cnt":17},{"title":"novel2","ncode":"N5678GP","userid":123456,"story":"あらすじ","biggenre":3,"genre":302,"general_firstup":"2022-01-10 10:01:11","general_lastup":"2022-01-11 11:11:11","noveltype":2,"end":0,"general_all_no":1,"length":1300,"isstop":0,"global_point":250,"daily_point":0,"weekly_point":0,"monthly_point":0,"quarter_point":0,"yearly_point":0,"fav_novel_cnt":44,"impression_cnt":8,"review_cnt":3,"all_point":161,"all_hyoka_cnt":17}]',
        content_type="application/json",
    )
    responses.add(
        responses.GET,
        "https://api.syosetu.com/novelapi/api?of=t-n-u-s-bg-g-gf-gl-nt-e-ga-l-i-gp-dp-wp-mp-qp-yp-f-imp-r-a-ah&out=json&userid=654321",
        status=200,
        body='[{"allcount":0}]',
        content_type="application/json",
    )
    # exist data
    userid = "123456"
    test1 = [
        {
            "title": "novel1",
            "ncode": "N1234GP",
            "userid": 123456,
            "story": "あらすじ１行目\nあらすじ2行目",
            "biggenre": 3,
            "genre": 302,
            "general_firstup": "2022-01-10 10:01:11",
            "general_lastup": "2022-01-11 11:11:11",
            "noveltype": 1,
            "end": 0,
            "general_all_no": 41,
            "length": 190000,
            "isstop": 0,
            "global_point": 250,
            "daily_point": 0,
            "weekly_point": 0,
            "monthly_point": 0,
            "quarter_point": 0,
            "yearly_point": 0,
            "fav_novel_cnt": 44,
            "impression_cnt": 8,
            "review_cnt": 3,
            "all_point": 161,
            "all_hyoka_cnt": 17,
        },
        {
            "title": "novel2",
            "ncode": "N5678GP",
            "userid": 123456,
            "story": "あらすじ",
            "biggenre": 3,
            "genre": 302,
            "general_firstup": "2022-01-10 10:01:11",
            "general_lastup": "2022-01-11 11:11:11",
            "noveltype": 2,
            "end": 0,
            "general_all_no": 1,
            "length": 1300,
            "isstop": 0,
            "global_point": 250,
            "daily_point": 0,
            "weekly_point": 0,
            "monthly_point": 0,
            "quarter_point": 0,
            "yearly_point": 0,
            "fav_novel_cnt": 44,
            "impression_cnt": 8,
            "review_cnt": 3,
            "all_point": 161,
            "all_hyoka_cnt": 17,
        },
    ]
    result = Novel.get_by_userid(userid)
    print(dir(result))
    assert result == test1

    # not exist data
    userid = "654321"
    test2 = []
    result = Novel.get_by_userid(userid)
    assert result == test2


def test_get_novel():
    ncode = "N0919GA"
    result = Novel.get_novel(ncode)
    print(result.title)
    print(dir(result))


def test_get_pv_per_chp():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = PvChp().get_pv(
        novel, start_date="2020-03-16", end_date="2020-03-18", use_cache=False
    )
    print(result)
    assert result == {
        "2020-03-16": {
            1: 1,
            2: 1,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 1,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1,
            21: 1,
            22: 1,
            23: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            28: 1,
            29: 1,
            30: 1,
            31: 2,
            32: 1,
            33: 1,
            34: 1,
            35: 1,
            36: 1,
            37: 1,
            38: 1,
            39: 1,
            40: 2,
            41: 2,
        },
        "2020-03-17": {
            1: 4,
            2: 5,
            3: 4,
            4: 3,
            5: 3,
            6: 4,
            7: 4,
            8: 4,
            9: 4,
            10: 4,
            11: 4,
            12: 4,
            13: 3,
            14: 3,
            15: 3,
            16: 3,
            17: 3,
            18: 3,
            19: 3,
            20: 3,
            21: 3,
            22: 3,
            23: 3,
            24: 3,
            25: 3,
            26: 3,
            27: 3,
            28: 3,
            29: 3,
            30: 3,
            31: 4,
            32: 3,
            33: 3,
            34: 3,
            35: 3,
            36: 3,
            37: 3,
            38: 3,
            39: 4,
            40: 6,
            41: 7,
        },
        "2020-03-18": {
            1: 3,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1,
            21: 1,
            22: 1,
            23: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            28: 1,
            29: 1,
            30: 1,
            31: 1,
            32: 1,
            33: 1,
            34: 1,
            35: 1,
            36: 1,
            37: 1,
            38: 1,
            39: 1,
            40: 1,
            41: 1,
        },
    }


def test_get_pv_per_day():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = PvDay().get_pv(
        novel, start_date="2020-03-10", end_date="2020-05-01", use_cache=True
    )
    test = {
        "2020-03-10": {"total": 31},
        "2020-03-11": {"total": 47},
        "2020-03-12": {"total": 119},
        "2020-03-13": {"total": 114},
        "2020-03-14": {"total": 29},
        "2020-03-15": {"total": 10},
        "2020-03-16": {"total": 14},
        "2020-03-17": {"total": 19},
        "2020-03-18": {"total": 7},
        "2020-03-19": {"total": 4},
        "2020-03-20": {"total": 2},
        "2020-03-21": {"total": 9},
        "2020-03-22": {"total": 10},
        "2020-03-23": {"total": 5},
        "2020-03-24": {"total": 3},
        "2020-03-25": {"total": 4},
        "2020-03-26": {"total": 5},
        "2020-03-27": {"total": 3},
        "2020-03-28": {"total": 3},
        "2020-03-29": {"total": 1},
        "2020-03-30": {"total": 3},
        "2020-03-31": {"total": 5},
        "2020-04-01": {"total": 3},
        "2020-04-02": {"total": 3},
        "2020-04-03": {"total": 2},
        "2020-04-04": {"total": 4},
        "2020-04-05": {"total": 2},
        "2020-04-06": {"total": 2},
        "2020-04-07": {"total": 2},
        "2020-04-08": {"total": 1},
        "2020-04-09": {"total": 0},
        "2020-04-10": {"total": 3},
        "2020-04-11": {"total": 2},
        "2020-04-12": {"total": 7},
        "2020-04-13": {"total": 1},
        "2020-04-14": {"total": 2},
        "2020-04-15": {"total": 0},
        "2020-04-16": {"total": 3},
        "2020-04-17": {"total": 0},
        "2020-04-18": {"total": 2},
        "2020-04-19": {"total": 2},
        "2020-04-20": {"total": 0},
        "2020-04-21": {"total": 0},
        "2020-04-22": {"total": 0},
        "2020-04-23": {"total": 9},
        "2020-04-24": {"total": 0},
        "2020-04-25": {"total": 0},
        "2020-04-26": {"total": 2},
        "2020-04-27": {"total": 2},
        "2020-04-28": {"total": 4},
        "2020-04-29": {"total": 2},
        "2020-04-30": {"total": 4},
        "2020-05-01": {"total": 2},
    }
    assert result == test


def test_sum_pv():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = SumPvDate(
        novel, start_date="2020-03-10", end_date="2020-05-01", use_cache=True
    ).get_pv()
    print(result)
    assert 1 == 2


def test_sum_pv_chp():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = SumPvChp(
        novel, start_date="2020-03-10", end_date="2020-05-01", use_cache=True
    ).get_pv()
    print(result)
    assert 1 == 2


def test_pv_chp_date():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = PvChp(
        novel, start_date="2020-03-10", end_date="2020-05-01", use_cache=False
    ).get_pv()
    print(result)
    assert 1 == 2


def test_get_impression():
    novel_data = {
        "title": "呪われ少女は不幸になりたい",
        "ncode": "N0919GA",
        "userid": 767713,
        "story": "「私、幸せになると死ぬ呪いにかかってるの」\n\n\u3000それは下校中に恋人から告げられた意味不明な言葉。どうせ本当のことではないと結論付けた俺は冗談として流すが、なら証明してあげると言われ彼女と口付けを交わす。\n\n\u3000上気した顔。どこか恥ずかしそうな笑い声。そして次の瞬間。\n\n「私今、幸せよ」\n\n\u3000──そう言った彼女は、落ちてきた鉄骨に串刺しにされた。\n\n\u3000これは彼女の物語。\n\u3000幸せになると死に、翌日生き返る。そんな異常を日常として受け入れている彼女が、呪いを解こうとする俺とぶつかり合いながらも向き合う物語である。\n\n\n2/10は0時、8時、12時、20時更新、それ以降は毎日7時に更新していきます。完結までの41話、全て書き上がっております。\n\n肥前文俊先生主催、「書き出し祭り」提出作品の連載版です。",
        "biggenre": 3,
        "genre": 302,
        "general_firstup": "2020-02-05 11:48:37",
        "general_lastup": "2020-03-12 20:00:00",
        "noveltype": 1,
        "end": 0,
        "general_all_no": 41,
        "length": 192239,
        "isstop": 0,
        "global_point": 249,
        "daily_point": 0,
        "weekly_point": 0,
        "monthly_point": 0,
        "quarter_point": 0,
        "yearly_point": 6,
        "fav_novel_cnt": 44,
        "impression_cnt": 8,
        "review_cnt": 3,
        "all_point": 161,
        "all_hyoka_cnt": 17,
    }
    novel = Novel(novel_data)
    result = get_impression(novel)
    print(result)
    assert 1 == 2
