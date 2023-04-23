import calendar
import json
import os
import pickle
import re
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
from .config import (
    AGENT_HEADER,
    CACHE_DIR,
    PAYLOAD_NOVEL,
    PAYLOAD_USR,
    URL_NOVEL,
    URL_NOVEL_PAGE,
    URL_PVS,
    URL_PVS_PER_DAY,
    URL_USR,
)
from .utils import PV_MODE, ImpKind, BigGenre, SmallGenre


class GetDataMixin:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.get_date = datetime.now()

    @classmethod
    def get_data(cls, url=None, params={}):
        """apiから値を取得

        Args:
            url (str, optional): リクエスト先のURL. Defaults to None.
            params (dict, optional): apiに渡すデータ. Defaults to {}.

        Raises:
            Exception: apiにアクセスできないなどのエラー

        Returns:
            list: レスポンス。
        """
        url = url if url is not None else cls.api_url
        try:
            r = requests.get(url, params=params)

            if r.status_code != 200:
                raise Exception("can not get user data.")
            data = r.json(strict=False)
        except Exception:
            return []
        else:
            return data

    @classmethod
    def get_by_userid(cls, userid):
        """useridを使用してapiからデータを取得

        Args:
            userid (str): 使用するuserid

        Returns:
            list: 取得したデータ
        """
        params = pickle.loads(pickle.dumps(cls.payload_tmp))
        params["userid"] = userid
        data = cls.get_data(params=params)
        if len(data) >= 1 and int(data[0]["allcount"]) == 0:
            return []
        return data


class User(GetDataMixin):
    api_url = URL_USR
    payload_tmp = PAYLOAD_USR
    culc_columns = [
        "impression_cnt",
        "review_cnt",
        "daily_point",
        "weekly_point",
        "monthly_point",
        "quarter_point",
        "yearly_point",
    ]

    def __init__(self, data):
        super(User, self).__init__(data)

    @classmethod
    def get_by_userid(cls, userid):
        """useridを使用してapiからデータを取得し、クラスを作成

        Args:
            userid (str): 検索に使用するuserid

        Returns:
            User: 検索結果
        """
        data = super(User, cls).get_by_userid(userid)
        if len(data) > 0:
            obj = cls(data[1])
        else:
            obj = None
        return obj

    @property
    def ncodes(self):
        """ユーザーが所有する小説のncode一覧

        Returns:
            list: ncodeのリスト
        """
        params = {"of": "n", "out": "json", "userid": self.userid}
        ncodes = self.get_data(URL_NOVEL, params)[1:]
        return [d["ncode"] for d in ncodes]

    @property
    def novels(self):
        """ユーザーが所有する小説一覧

        Returns:
            list: Novelのリスト
        """
        userid = self.userid
        if not getattr(self, "_novels"):
            objs = Novel.get_by_userid(userid)
            self._novels = objs
        return self._novels

    def culc_data(self, novels=None):
        if novels is None:
            novels = self.novels
        for column in self.culc_columns:
            sums = sum([getattr(novel, column) for novel in novels])
            setattr(self, "sum_" + column, sums)

    def __str__(self):
        result = pickle.loads(pickle.dumps(self.__dict__))
        del result["get_date"]
        return json.dumps(result)


class Novel(GetDataMixin):
    api_url = URL_NOVEL
    payload_tmp = PAYLOAD_NOVEL

    def __init__(self, data):
        super(Novel, self).__init__(data)
        self.firstup = datetime.strptime(self.general_firstup, "%Y-%m-%d %H:%M:%S")
        self.lastup = datetime.strptime(self.general_lastup, "%Y-%m-%d %H:%M:%S")
        self.biggenre = BigGenre.get_genre(int(self.biggenre))
        self.genre = SmallGenre.get_genre(int(self.genre))
        self.average_hyoka = round(float(self.all_point) / float(self.all_hyoka_cnt))

    @property
    def novel_type(self):
        if self.noveltype == 1:
            return "連載"
        elif self.noveltype == 2:
            return "短編"

    @property
    def is_end(self):
        if self.end == 0 and self.noveltype == 1:
            return "完結済み"
        elif self.end == 0 and self.noveltype == 2:
            return "短編"
        elif self.end == 1 and self.noveltype == 1:
            return "連載中"
        elif self.end == 1 and self.noveltype == 2:
            return "短編"

    @property
    def is_stop(self):
        if self.isstop == 1:
            return "長期連載停止中"
        else:
            return "連載中"

    @property
    def firstup_date(self):
        return self.firstup.strftime("%Y-%m-%d")

    @property
    def lastup_date(self):
        return self.lastup.strftime("%Y-%m-%d")

    def __str__(self):
        return self.__dict__

    def data(self, is_str=True, is_url=True):
        data = dict(
            title=self.title,
            ncode=self.ncode,
            userid=str(self.userid) if is_str else self.userid,
            story=self.story,
            biggenre=str(self.biggenre) if is_str else self.biggenre,
            genre=str(self.genre) if is_str else self.genre,
            firstup=self.general_firstup if is_str else self.firstup,
            lastup=self.general_lastup if is_str else self.lastup,
            novel_type=self.novel_type if is_str else self.noveltype,
            is_end=self.is_end if is_str else self.end,
            general_all_no=str(self.general_all_no) if is_str else self.general_all_no,
            length=str(self.length) if is_str else self.length,
            is_stop=self.is_stop if is_str else self.isstop,
            global_point=str(self.global_point) if is_str else self.global_point,
            fav_novel_cnt=str(self.fav_novel_cnt) if is_str else self.fav_novel_cnt,
            impression_cnt=str(self.impression_cnt) if is_str else self.impression_cnt,
            review_cnt=str(self.review_cnt) if is_str else self.review_cnt,
            all_point=str(self.all_point) if is_str else self.all_point,
            all_hyoka_cnt=str(self.all_hyoka_cnt) if is_str else self.all_hyoka_cnt,
            average_hyoka=str(self.average_hyoka) if is_str else self.average_hyoka,
        )
        if is_url:
            data["url"] = URL_NOVEL_PAGE.format(ncode=self.ncode)
        return data

    @classmethod
    def get_by_userid(cls, userid):
        data = super(Novel, cls).get_by_userid(userid)
        objs = list()
        for d in data[1:]:
            objs.append(cls(d))
        return objs

    @classmethod
    def get_novel(cls, ncode):
        params = pickle.loads(pickle.dumps(cls.payload_tmp))
        params["ncode"] = ncode.lower()
        data = cls.get_data(params=params)
        if len(data) >= 1 and int(data[0]["allcount"]) == 0:
            return None
        obj = cls(data[1])
        return obj

    @classmethod
    def get_novels(cls, ncodes):
        novels = list()
        for ncode in ncodes:
            novels.append(cls.get_novel(ncode))
        return novels

    def get_posted_date(self, is_str=False):
        r = requests.get(
            URL_NOVEL_PAGE.format(ncode=self.ncode.lower()), headers=AGENT_HEADER
        )
        html = BeautifulSoup(r.content, "html.parser")
        chp_box = html.find("div", class_="index_box")
        chps = chp_box.find_all("dl", class_="novel_sublist2")
        data = {}
        for i, chp in enumerate(chps):
            update = chp.find("dt", class_="long_update")
            span = update.find("span")
            if span is None:
                update_ = update.text.replace("\n", "")
                update_date = (
                    update_ if is_str else datetime.strptime(update_, "%Y/%m/%d %H:%M")
                )
                revision_date = None
            else:
                update_ = update.text.replace("\n", "").replace("（改）", "")
                update_date = (
                    update_ if is_str else datetime.strptime(update_, "%Y/%m/%d %H:%M")
                )
                revision = span.attrs["title"].replace(" 改稿", "")
                revision_date = (
                    revision
                    if is_str
                    else datetime.strptime(revision, "%Y/%m/%d %H:%M")
                )

            data[str(i + 1)] = {"update": update_date, "revision": revision_date}
        return data

    def get_titles(self):
        if hasattr(self, "titles") and hasattr(self, "chapter_set"):
            return self.titles, self.chapter_set
        r = requests.get(
            URL_NOVEL_PAGE.format(ncode=self.ncode.lower()), headers=AGENT_HEADER
        )
        html = BeautifulSoup(r.content, "html.parser")
        chp_box = html.find("div", class_="index_box")
        data = dict()
        chp_data = dict()
        chp_cnt = 1
        chapter_title = ""
        chips = chp_box.find_all(class_=["novel_sublist2", "chapter_title"])
        for child in chips:
            if child.attrs["class"][0] == "chapter_title":
                chapter_title = child.text
                chp_data[chapter_title] = list()
            elif child.attrs["class"][0] == "novel_sublist2":
                subtitle = child.find("a").text
                if chapter_title:
                    chp_data[chapter_title].append(chp_cnt)
                data[chp_cnt] = subtitle
                chp_cnt += 1
        self.titles = data
        self.chapter_set = chp_data
        return data, chp_data


class PvMixin:
    def __init__(self, novel, start_date=None, end_date=None, use_cache=True):
        self.novel = novel
        self.start_date = start_date
        self.end_date = end_date
        self.use_cache = use_cache

    def set_date_range(self):
        if self.start_date is None:
            startdt = self.novel.firstup
        else:
            startdt = datetime.strptime(self.start_date, "%Y-%m-%d")
        if self.end_date is None:
            enddt = datetime.now() + timedelta(days=-2)
        else:
            enddt = datetime.strptime(self.end_date, "%Y-%m-%d")
        days_num = (enddt - startdt).days + 1
        return startdt, enddt, days_num

    def get_cache_file(self, mode=None):
        if mode is None:
            filename = "{mode}_{ncode}".format(mode=self.mode, ncode=self.novel.ncode)
        else:
            filename = "{mode}_{ncode}".format(mode=mode, ncode=self.novel.ncode)
        for curDir, dirs, files in os.walk(CACHE_DIR):
            for file in files:
                if filename in file:
                    return file
        return None

    def get_cache_data(self, mode=None):
        data = dict()
        cache_file = ""
        if self.use_cache:
            cache_file = self.get_cache_file(mode)
            if cache_file:
                with open(os.path.join(CACHE_DIR, cache_file), "rb") as f:
                    data = pickle.load(f)
        return data, cache_file

    def save_cache_data(self, data, cache_file, mode=None):
        if self.use_cache:
            if mode is None:
                filename = "{mode}_{ncode}_{date}.bin".format(
                    mode=self.mode,
                    ncode=self.novel.ncode,
                    date=datetime.now().strftime("%Y%m%d_%H%M%S"),
                )
            else:
                filename = "{mode}_{ncode}_{date}.bin".format(
                    mode=mode,
                    ncode=self.novel.ncode,
                    date=datetime.now().strftime("%Y%m%d_%H%M%S"),
                )
            filename = os.path.join(CACHE_DIR, filename)
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            if cache_file:
                os.remove(os.path.join(CACHE_DIR, cache_file))


class PvChps(PvMixin):
    mode = "pv_chp"

    def get_pv(self):
        """_summary_
        各日付における各話のPV
        例：
            {"2020-03-10":{1:1,2:1,3:1}}
            2020-03-10での1話のPVは1,2話のPVは1,3話のPVは1
            データがない話はPV0とする
            最後のPVがない話についてはデータなし
            9話まで投稿されている状態で1:1,2:1,5:1,6:1であった場合、
            {1:1,2:1,3:0,4:0,5:1,6:1}となり7,8,9話のデータはない

        """
        pv_date, cache_file = self.get_cache_data()
        startdt, enddt, days_num = self.set_date_range()

        date_list = [startdt + timedelta(days=x) for x in range(days_num)]
        for date_ in date_list:
            date_str = date_.strftime("%Y-%m-%d")
            if date_str not in pv_date:
                html_pvs = requests.get(URL_PVS % (self.novel.ncode, date_str))
                soup = BeautifulSoup(html_pvs.content, "html.parser")

                pv_chp = dict()

                last_chp = 0
                pvss = soup.find(id="chapter_graph").find("ul").find_all("li")
                for pv in pvss:
                    text = pv.text.split(":")
                    chp = int(re.findall("第(.*)部分", text[0])[0])
                    num = int(re.findall("(.*)人", text[1])[0])
                    not_data_chps = {i: 0 for i in range(last_chp + 1, chp)}
                    pv_chp.update(not_data_chps)
                    pv_chp[chp] = num
                    last_chp = chp

                pv_date[date_str] = pv_chp

        self.save_cache_data(pv_date, cache_file)
        data = {
            date.strftime("%Y-%m-%d"): pv_date[date.strftime("%Y-%m-%d")]
            for date in date_list
        }
        self.data = data
        return data

    def get_pv_chp(self):
        """各話における各日付のPVを取得
        例：
            {1: [1,2,3,4,5],2:[1,2,3,4,5]}
            キーが話、値はPVのリスト
            それぞれの日付はdaysを参照
        : returns
            {dict} {chp:[pv..]}の形式のPVデータ
            {list} 日付のリスト
        """
        if hasattr(self, "data") is False:
            data = self.get_pv()
        else:
            data = self.data
        num_novels = max([len(chps) for chps in data.values()])
        days = list(data.keys())
        pvs = {
            chp: [data[day][chp] if chp in data[day] else 0 for day in days]
            for chp in range(1, num_novels + 1)
        }
        return pvs, days


class PvDay(PvMixin):
    mode = "pv_day"

    def _get_num(self, element, modes):
        result = dict()
        trs = element.find_all("tr")
        for tr in trs:
            data = tr.find("td", attrs={"class": "item"})
            if data:
                mode = tr.find("td", attrs={"class": "graph"}).div.div["class"][0]
                if PV_MODE.to_index(mode) in modes:
                    result[mode] = int(re.findall("(.*)人", data.text)[0])
        return result

    def get_pv(self, modes=[1]):
        """合計PVを取得
        例:
            {"2020-03-10": {"total":31,"pc": 12, "smp": 19}}
            2020-03-10の合計PVはPCからが12, スマホからが19, 合計で31

        : argument
            modes -- {list} 取得するpvの種類
                1: total, 2: pc, 3: smartphone
                totalとpcを取得-> [1,2]
                totalを取得 -> [1]
                total, pc, smartphoneを取得 -> [1,2,3]
        : return
            {dict} -- {date:{mode:pv}}の形式のPVデータ
        """
        pv, cache_file = self.get_cache_data()
        startdt, enddt, days_num = self.set_date_range()

        date_list = [startdt + timedelta(days=x) for x in range(days_num)]
        month_list = list()
        for date_ in date_list:
            if date_.strftime("%Y%m") not in month_list:
                month_list.append(date_.strftime("%Y%m"))

        # pv = dict()
        for date_ in month_list:
            html_pvs = requests.get(URL_PVS_PER_DAY % (self.novel.ncode.lower(), date_))
            s_day = BeautifulSoup(html_pvs.content, "html.parser")
            # 各日付
            pvss = s_day.find_all("table", class_="access_per_day")

            ym = datetime.strptime(date_, "%Y%m")

            # 今見ている月の最終日
            month_last = date(
                ym.year, ym.month, calendar.monthrange(ym.year, ym.month)[1]
            ).day
            # スタートと今見ている月が同じとき
            if (ym.year == startdt.year) & (ym.month == startdt.month):
                start_day = startdt.day
            else:
                start_day = 1
            start_day_ = start_day

            for pvs in pvss:
                day_ = datetime.strptime(pvs.find(class_="day").text, "%Y年%m月%d日")
                day = day_.strftime("%Y-%m-%d")
                # 最終日の次の日だったら終わり
                if (
                    (ym.year == enddt.year)
                    & (ym.month == enddt.month)
                    & (day_.day == enddt.day + 1)
                ):
                    break
                if startdt > day_:
                    continue
                if day not in pv:
                    # pv_ = int(re.findall("(.*)人",pvs.find_all("td", class_ = "item")[-1].text)[0].replace(",",""))
                    pv_ = self._get_num(pvs, modes)
                    for i in range(start_day_, int(day.split("-")[2])):
                        day__ = datetime(ym.year, ym.month, i).strftime("%Y-%m-%d")
                        pv[day__] = {PV_MODE.to_mode(mode): 0 for mode in modes}
                    pv[day] = pv_

                start_day_ = int(day.split("-")[2]) + 1

            if (int(enddt.year) == int(ym.year)) and (
                int(enddt.month) == int(ym.month)
            ):
                for i in range(start_day_, enddt.day + 1):
                    date_ = (
                        str(enddt.year)
                        + "-"
                        + str(enddt.month).zfill(2)
                        + "-"
                        + str(i).zfill(2)
                    )
                    pv[date_] = {PV_MODE.to_mode(mode): 0 for mode in modes}

            else:
                # その月の最終ｐｖ確認日から月の最終日までを0にする
                for i in range(start_day_ + 1, month_last + 1):
                    date_ = (
                        str(ym.year)
                        + "-"
                        + str(ym.month).zfill(2)
                        + "-"
                        + str(i).zfill(2)
                    )
                    if (
                        ym.year == enddt.year
                        and ym.month == enddt.month
                        and i == enddt.day
                    ):
                        break
                    pv[date_] = {PV_MODE.to_mode(mode): 0 for mode in modes}

        pv = dict(sorted(pv.items()))

        self.save_cache_data(pv, cache_file)
        data = {
            date.strftime("%Y-%m-%d"): pv[date.strftime("%Y-%m-%d")]
            for date in date_list
        }
        self.data = data
        return data


class SumPvDate(PvChps, PvMixin):
    def get_pv(self, data=None):
        """日付ごとのすべての話の合計PV(各日のトータルPVではない)
        例:
            {2020-03-10:79, 2020-03-11: 62, 2020-03-21: 52}
            2020-03-10の合計PVが79, 2020-03-11は62...

        :argument
            data -- {dict} pvデータ
        :return
            {dict}: {date: pv}の形式のpvデータ
        """
        if data is None:
            if hasattr(self, "data"):
                data = self.data
            else:
                data = super().get_pv()
        pvs_date = {d: sum(list(ps.values())) for d, ps in data.items()}
        return pvs_date


class SumPvChp(PvChps, PvMixin):
    def get_pv(self, data=None):
        """各話の合計PVを返す
        例:
            {1:79, 2: 62, 3: 52}
            1話の期間中の合計PVが79, 2話は62...
        : argument
            data -- {dict} pvデータ
        : return
            {dict}: {chp: pv}の形式のpvデータ
        """
        if data is None:
            if hasattr(self, "data"):
                data = self.data
            else:
                data = super().get_pv()
        num_novels = max([len(chps) for chps in data.values()])
        sum_pv = [0 for _ in range(num_novels)]

        for pvs in data.values():
            for novel, pv in enumerate(pvs):
                sum_pv[novel] += pvs[pv]
        chp = list(range(1, num_novels + 1))
        result = dict(zip(chp, sum_pv))
        return result


class PvChp(PvChps, PvMixin):
    def get_pv(self, chp, data=None):
        if data is None:
            if hasattr(self, "data"):
                data = self.data
            else:
                data = super().get_pv()

        pvs = {d: pv[chp] for d, pv in data.items()}

        return pvs


def get_impression(novel):
    num_imp = novel.impression_cnt
    pages = (num_imp - 1) // 10 + 1
    r = requests.get(
        URL_NOVEL_PAGE.format(ncode=novel.ncode.lower()), headers=AGENT_HEADER
    )
    html = BeautifulSoup(r.content, "html.parser")
    impression_url = (
        html.find(id="novel_header")
        .find(id="head_nav")
        .find_all("li")[2]
        .find("a")
        .get("href")
    )

    imp_list = list()

    for page in range(1, pages + 1):
        url = impression_url + "/?p=" + str(page)
        html = requests.get(url, headers=AGENT_HEADER)
        bs = BeautifulSoup(html.content, "html.parser")
        content = bs.find(id="contents_main")
        impressions = content.find_all("div", class_="waku")
        for impression in impressions:
            sender = (
                impression.find("div", class_="comment_info")
                .find_all("div")[0]
                .find("a")
                .text
            )
            if not sender == "":
                idx = 4
            else:
                idx = 3

            date = (
                impression.find("div", class_="comment_info")
                .find_all("div")[0]
                .get_text(",")
                .split(",")[idx]
                .strip()
            )
            date = datetime.strptime(date.replace(" ", ""), "%Y年%m月%d日%H時%M分").strftime(
                "%Y-%m-%d"
            )

            no_cnt = impression.find("div", class_="box_novelno")
            if no_cnt is None:
                no = -1
            else:
                no = int(
                    re.findall(
                        "第(.*)部分",
                        no_cnt.find("span", class_="no_posted_impression").text,
                    )[0]
                )

            imp = dict(
                sender=sender, no=no, date=date, good=None, bad=None, comment=None
            )
            comment_kind_html = impression.find_all("div", class_="comment_h2")
            comment_kind = [i.text for i in comment_kind_html]
            comment_all = impression.find_all("div", class_="comment")
            for i in range(len(comment_kind)):
                imp[ImpKind.to_key(comment_kind[i])] = comment_all[i].text
            imp_list.append(imp)
    return imp_list
