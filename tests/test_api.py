
import responses
import json

from narou_data_api.api import (
    User
)
# .tox/c1/bin/pytest --cov=narou_data_api tests/test_api.py -vv -s --cov-branch --cov-report=term --basetemp=/root/others/narouDataAPI/.tox/c1/tmp

#class GetDataMixin:
#    def __init__(self, data):
#    def get_data(cls, url=None, params={}):
#    def get_by_userid(cls, userid):
#class User(GetDataMixin):
class TestUser:
#    def __init__(self, data):
#    def get_by_userid(cls, userid):
# .tox/c1/bin/pytest --cov=narou_data_api tests/test_api.py::TestUser::test_get_by_userid -vv -s --cov-branch --cov-report=term --basetemp=/root/others/narouDataAPI/.tox/c1/tmp
    @responses.activate
    def test_get_by_userid(self):
        # success get data
        responses.add(
            responses.GET,
            "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=123456",
            status=200,
            body='[{"allcount":1},{"userid":"123456","name":"test_user","novel_cnt":10,"review_cnt":1,"novel_length":1000000,"sum_global_point":12345}]',
            content_type="application/json",
        )
        result = User.get_by_userid("123456")
        assert result.name == "test_user"
        assert result.novel_cnt == 10
        
        # raise error
        responses.add(
            responses.GET,
            "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=654321",
            status=500,
            body="",
            content_type="application/json",
        )
        result = User.get_by_userid("654321")
        assert result == None
        
        # result is 0
        responses.add(
            responses.GET,
            "https://api.syosetu.com/userapi/api?of=u-n-nc-rc-nl-sg&out=json&userid=987654",
            status=200,
            body='[{"allcount":0}]',
            content_type="application/json",
        )
        result = User.get_by_userid("987654")
        assert result == None

#    def ncodes(self):
# .tox/c1/bin/pytest --cov=narou_data_api tests/test_api.py::TestUser::test_get_by_userid -vv -s --cov-branch --cov-report=term --basetemp=/root/others/narouDataAPI/.tox/c1/tmp
    @responses.activate
    def test_ncodes(self):
        responses.add(
            responses.GET,
            "https://api.syosetu.com/novelapi/api?of=n&out=json&userid=123456",
            status=200,
            body='[{"allcount":3},{"ncode":"N1234GA"},{"ncode":"N5678GB"},{"ncode":"N9876GV"}]',
            content_type="application/json"
        )
        user = User({"userid":"123456"})
        result = user.ncodes
        assert result == ["N1234GA","N5678GB","N9876GC"]

#    def novels(self):
    @responses.activate
    def test_novels(self):
        response_body=[
            {"allcount":3},
            {"title":"test_title1","ncode":"N1234GA","userid":"123456","story":"test_story1","biggenre":3,"genre":302,"general_firstup": "2020-02-05 11:48:37","general_lastup": "2020-03-12 20:00:00","noveltype": 1,"end": 0,"general_all_no": 41,"length": 192239,"isstop": 0,"global_point": 249,"daily_point": 0,"weekly_point": 0,"monthly_point": 0,"quarter_point": 0,"yearly_point": 6,"fav_novel_cnt": 44,"impression_cnt": 8,"review_cnt": 3,"all_point": 161,"all_hyoka_cnt": 17},
            {"title":"test_title2","ncode":"N5678GB","userid":"123456","story":"test_story2","biggenre":3,"genre":302,"general_firstup": "2020-02-05 11:48:37","general_lastup": "2020-03-12 20:00:00","noveltype": 1,"end": 0,"general_all_no": 41,"length": 192239,"isstop": 0,"global_point": 249,"daily_point": 0,"weekly_point": 0,"monthly_point": 0,"quarter_point": 0,"yearly_point": 6,"fav_novel_cnt": 44,"impression_cnt": 8,"review_cnt": 3,"all_point": 161,"all_hyoka_cnt": 17},
            {"title":"test_title3","ncode":"N9876GC","userid":"123456","story":"test_story3","biggenre":3,"genre":302,"general_firstup": "2020-02-05 11:48:37","general_lastup": "2020-03-12 20:00:00","noveltype": 1,"end": 0,"general_all_no": 41,"length": 192239,"isstop": 0,"global_point": 249,"daily_point": 0,"weekly_point": 0,"monthly_point": 0,"quarter_point": 0,"yearly_point": 6,"fav_novel_cnt": 44,"impression_cnt": 8,"review_cnt": 3,"all_point": 161,"all_hyoka_cnt": 17}
        ]
        responses.add(
            responses.GET,
            "https://api.syosetu.com/novelapi/api?of=t-n-u-s-bg-g-gf-gl-nt-e-ga-l-i-gp-dp-wp-mp-qp-yp-f-imp-r-a-ah&out=json&userid=123456",
            status=200,
            body=json.dumps(response_body)
        )
        user = User({"userid":"123456"})
        # not has _novels
        result = user.novels
        assert [r["title"] for r in result] == ["test_title1","test_title2","test_title3"]
        
        # has _novels
        result = user.novels
        assert [r["title"] for r in result] == ["test_title1","test_title2","test_title3"]
        
#    def culc_data(self, novels=None):
#    def __str__(self):
#class Novel(GetDataMixin):
#    def __init__(self, data):
#    def novel_type(self):
#    def is_end(self):
#    def is_stop(self):
#    def firstup_date(self):
#    def lastup_date(self):
#    def __str__(self):
#    def data(self, is_str=True, is_url=True):
#    def get_by_userid(cls, userid):
#    def get_novel(cls, ncode):
#    def get_novels(cls, ncodes):
#    def get_posted_date(self, is_str=False):
#    def get_titles(self):
#class PvMixin:
#    def __init__(self, novel, start_date=None, end_date=None, use_cache=True):
#    def set_date_range(self):
#    def get_cache_file(self, mode=None):
#    def get_cache_data(self, mode=None):
#    def save_cache_data(self, data, cache_file, mode=None):
#class PvChps(PvMixin):
#    def get_pv(self):
#    def get_pv_chp(self):
#class PvDay(PvMixin):
#    def _get_num(self, element, modes):
#    def get_pv(self, modes=[1]):
#class SumPvDate(PvChps, PvMixin):
#    def get_pv(self, data=None):
#class SumPvChp(PvChps, PvMixin):
#    def get_pv(self, data=None):
#class PvChp(PvChps, PvMixin):
#    def get_pv(self, chp, data=None):
#def get_impression(novel):
