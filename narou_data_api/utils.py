import os
from enum import Enum

from .config import TPL_DIR, TPL_NOVEL_INFO_OUTPUT, TPL_USER_INFO_OUTPUT



class BigGenre(Enum):
    LOVE = (1, "恋愛")
    FANTASY = (2, "ファンタジー")
    LITERATURE = (3, "文芸")
    SF = (4, "SF")
    OTHERS = (99, "その他")
    NONGENRE = (98, "ノンジャンル")

    def __init__(self, no: int, genre: str):
        self.no = no
        self.genre = genre

    def __str__(self):
        return self.genre

    def __int__(self):
        return self.no

    @classmethod
    def genre_genre(cls, no):
        for g in cls.__members__.values():
            if no == g.no:
                return g.genre

    @classmethod
    def genre_no(cls, genre):
        for g in cls.__members__.values():
            if genre == g.genre:
                return int(g)

    @classmethod
    def get_genre(cls, no):
        for g in cls.__members__.values():
            if no == g.no:
                return g


class SmallGenre(Enum):
    DIFFERENT_WORLD = (101, "異世界", BigGenre.LOVE)
    REAL_WORLD = (102, "現実世界", BigGenre.LOVE)
    HIGH_FANTASY = (201, "ハイファンタジー", BigGenre.FANTASY)
    LOW_FANTASY = (202, "ローファンタジー", BigGenre.FANTASY)
    JUNBUNGAKU = (301, "純文学", BigGenre.LITERATURE)
    HUMAN_DRAMA = (302, "ヒューマンドラマ", BigGenre.LITERATURE)
    HISTORY = (303, "歴史", BigGenre.LITERATURE)
    DETECTIVE = (304, "推理", BigGenre.LITERATURE)
    HORROR = (305, "ホラー", BigGenre.LITERATURE)
    ACTION = (306, "アクション", BigGenre.LITERATURE)
    COMEDY = (307, "コメディー", BigGenre.LITERATURE)
    VR_GAME = (401, "VRゲーム", BigGenre.SF)
    UNIVERSE = (402, "空想科学", BigGenre.SF)
    FANTASY_SCIENCE = (403, "宇宙", BigGenre.SF)
    PANIC = (404, "パニック", BigGenre.SF)
    FAIRY_TALE = (9901, "童話", BigGenre.OTHERS)
    POETRY = (9902, "詩", BigGenre.OTHERS)
    ESSAY = (9903, "エッセイ", BigGenre.OTHERS)
    REPLAY = (9904, "リプレイ", BigGenre.OTHERS)
    OTHERS = (9999, "その他", BigGenre.OTHERS)
    NON_GENRE = (9801, "ノンジャンル", BigGenre.NONGENRE)

    def __init__(self, no, genre, big_genre):
        self.no = no
        self.genre = genre
        self.big_genre = big_genre

    def __str__(self):
        return f"{self.genre}〔{self.big_genre}〕"

    def __int__(self):
        return self.no

    @classmethod
    def genre_name(cls, no):
        for g in cls.__members__.values():
            if no == g.no:
                return str(g)

    @classmethod
    def genre_no(cls, genre):
        for g in cls.__members__.values():
            if genre == g.genre:
                return int(g)

    @classmethod
    def get_genre(cls, no):
        for g in cls.__members__.values():
            if no == g.no:
                return g


class PV_MODE(Enum):
    SUM = (1, "total")
    PC = (2, "pc")
    PHONE = (2, "smp")

    def __init__(self, index: int, html):
        self.index = index
        self.html = html

    def __str__(self):
        return self.html

    def __int__(self):
        return self.index

    @classmethod
    def to_mode(cls, index):
        for m in cls.__members__.values():
            if index == m.index:
                return str(m)

    @classmethod
    def to_index(cls, html):
        for m in cls.__members__.values():
            if html == m.html:
                return int(m)


class ImpKind(Enum):
    GOOD = ("good", "良い点")
    BAD = ("bad", "気になる点")
    COMMENT = ("comment", "一言")

    def __init__(self, key, html):
        self.key = key
        self.html = html

    @classmethod
    def to_key(cls, html):
        for m in cls.__members__.values():
            if html == m.html:
                return m.key

    @classmethod
    def to_html(cls, key):
        for m in cls.__members__.values():
            if key == m.key:
                return m.html


def create_output(tpl_file, data, replace_list):
    tpl_path = os.path.join(TPL_DIR, tpl_file)
    content = str()
    with open(tpl_path, "r") as f:
        content = f.read()

    for key in replace_list:
        value = replace_list[key]
        if value in data:
            content = content.replace(key, str(data[value]))
        else:
            content = content.replace(key, "")
    return content


def output_user_info(user):
    data = user.__dict__
    replace_list = {
        "[userid]": "userid",
        "[name]": "name",
        "[novel_cnt]": "novel_cnt",
        "[review_cnt]": "review_cnt",
        "[novel_length]": "novel_length",
        "[sum_global_point]": "sum_global_point",
    }
    output = create_output(TPL_USER_INFO_OUTPUT, data, replace_list)

    return output


def output_novel_info(novel):
    replace_list = {
        "[title]": "title",
        "[userid]": "userid",
        "[url]": "url",
        "[ncode]": "ncode",
        "[story]": "story",
        "[biggenre]": "biggenre",
        "[genre]": "genre",
        "[firstup]": "firstup",
        "[lastup]": "lastup",
        "[novel_type]": "novel_type",
        "[is_end]": "is_end",
        "[general_all_no]": "general_all_no",
        "[length]": "length",
        "[is_stop]": "is_stop",
        "[global_point]": "global_point",
        "[fav_novel_cnt]": "fav_novel_cnt",
        "[impression_cnt]": "impression_cnt",
        "[review_cnt]": "review_cnt",
        "[all_point]": "all_point",
        "[all_hyoka_cnt]": "all_hyoka_cnt",
        "[all_hyoka_cnt]": "all_hyoka_cnt",
    }
    data = novel.data()
    print(data)
    output = create_output(TPL_NOVEL_INFO_OUTPUT, data, replace_list)

    return output
