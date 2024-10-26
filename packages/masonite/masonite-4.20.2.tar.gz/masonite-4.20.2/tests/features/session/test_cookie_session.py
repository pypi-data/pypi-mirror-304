from tests import TestCase


class TestCookieSession(TestCase):
    def test_can_start_session(self):
        request = self.make_request()
        session = self.application.make("session")
        request.cookie("s_hello", "test")
        session.start("cookie")
        self.assertEqual(session.get("hello"), "test")

    def test_can_get_session_dict(self):
        request = self.make_request()
        session = self.application.make("session")
        request.cookie("s_hello", '{"hello": "test"}')
        session.start("cookie")
        self.assertEqual(type(session.get("hello")), dict)

    def test_can_set_and_get_session_dict(self):
        request = self.make_request()
        session = self.application.make("session")
        session.start("cookie")
        session.set("key1", {"hello": "test"})
        self.assertEqual(type(session.get("key1")), dict)
        self.assertEqual(session.get("key1")["hello"], "test")

    def test_can_set_and_get_session(self):
        self.make_request()
        session = self.application.make("session")
        session.start("cookie")
        session.set("key1", "test1")
        self.assertEqual(session.get("key1"), "test1")

    def test_can_increment_and_decrement_session(self):
        self.make_request()
        session = self.application.make("session")
        session.start("cookie")
        session.set("key1", "1")
        session.set("key5", "5")
        session.increment("key1")
        session.decrement("key5")
        self.assertEqual(session.get("key1"), "2")
        self.assertEqual(session.get("key5"), "4")

    def test_can_save_session(self):
        self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        session.start("cookie")
        session.set("key1", "test1")

        self.assertEqual(response.cookie("s_key1"), "test1")

    def test_can_delete_session(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        request.cookie("s_key", "test")
        session.start("cookie")

        self.assertEqual(session.get("key"), "test")

        session.delete("key")
        self.assertEqual(session.get("key"), None)

        self.assertEqual(response.cookie("s_key"), None)
        self.assertTrue("s_key" in response.cookie_jar.deleted_cookies)

    def test_can_pull_session(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        request.cookie("s_key", "test")
        session.start("cookie")

        self.assertEqual(session.get("key"), "test")

        key = session.pull("key")
        self.assertEqual(key, "test")
        self.assertEqual(session.get("key"), None)
        self.assertEqual(response.cookie("s_key"), None)
        self.assertTrue("s_key" in response.cookie_jar.deleted_cookies)

    def test_can_flush_session(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        request.cookie("s_key", "test")
        session.start("cookie")

        self.assertEqual(session.get("key"), "test")

        session.flush()
        self.assertEqual(session.get("key"), None)
        self.assertEqual(response.cookie("s_key"), None)
        self.assertTrue("s_key" in response.cookie_jar.deleted_cookies)

    def test_can_flash(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        session.start("cookie")
        session.flash("key", "test")
        self.assertEqual(session.get("key"), "test")
        self.assertEqual(session.get("key"), None)
        self.assertEqual(response.cookie("f_key"), None)

    def test_flash_two_keys_does_not_duplicate_data(self):
        request = self.make_request()
        response = self.make_response()
        session = self.application.make("session")
        session.start("cookie")
        session.flash("key", "test")
        session.flash("key2", "test2")

        self.assertTrue(session.has("key"))
        self.assertTrue(session.has("key2"))
        self.assertTrue(response.cookie_jar.exists("f_key"))
        self.assertTrue(response.cookie_jar.exists("f_key2"))

        self.assertEqual(session.get("key"), "test")

        self.assertFalse(session.has("key"))
        self.assertTrue(session.has("key2"))
        self.assertFalse(response.cookie_jar.exists("f_key"))
        self.assertTrue(response.cookie_jar.exists("f_key2"))
