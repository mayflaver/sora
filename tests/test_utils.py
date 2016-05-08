from nose.tools import assert_equal, assert_is
from sora.utils import Singleton


class TestSingleton(object):
    def setUp(self):
        self.singleton1 = Singleton()
        self.singleton2 = Singleton()

    def test_is_singleton(self):
        assert_is(self.singleton1, self.singleton2)
