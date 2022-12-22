from rest_framework.test import APITestCase
from rooms.models import Amenity
from users.models import User


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/rooms/amenities/"

    def setUp(self) -> None:
        # Set amenities
        Amenity.objects.create(name=self.NAME, description=self.DESC)

        # Set staff user
        user = User.objects.create(username="staffuser")
        user.set_password("1234")
        user.is_staff = True
        user.save()
        self.staff_user = user

    def test_get_amenites(self):
        response = self.client.get(self.URL)
        data = response.json()
        MESSAGE = "GET amenities fail: "
        self.assertEqual(
            response.status_code,
            200,
            MESSAGE + "status code",
        )
        self.assertIsInstance(
            data,
            list,
            MESSAGE + "get amenities",
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
            MESSAGE + "get 'name' property of amenities",
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
            MESSAGE + "get 'description' property of amenities",
        )

    def test_post_amenities_forbidden(self):

        POST_MESSAGE = "POST amenites fail: "

        res = self.client.post(self.URL)
        self.assertEqual(
            res.status_code,
            403,
            POST_MESSAGE + "user (not staff) is not forbidden",
        )

    def test_post_amenities(self):
        NAME_POST = "New Name"
        DESC_POST = "New Description"
        POST_MESSAGE = "POST amenities fail: "

        self.client.force_login(self.staff_user)

        res = self.client.post(
            self.URL,
            {"name": NAME_POST, "description": DESC_POST},
        )
        data = res.json()

        self.assertEqual(
            res.status_code,
            201,
            POST_MESSAGE + "wrong status code",
        )
        self.assertIn(
            "name",
            data,
            "no 'name' property",
        )
        self.assertIn(
            "description",
            data,
            "no 'description' property",
        )


class TestAmenityDetail(APITestCase):
    URL = "/rooms/amenities/"

    def setUp(self):
        Amenity.objects.create(name="New Amenity", description="New Description")

        user = User.objects.create(username="username")
        user.set_password("1234")
        user.is_staff = True
        user.save()
        self.staff_user = user

    def test_amenity_not_found(self):
        response = self.client.get(self.URL + "2")

        self.assertEqual(
            response.status_code,
            404,
            "GET amenity fail: should be not found",
        )

    def test_get_amenity(self):
        MESSAGE = "Get amenity fail: "
        res = self.client.get(self.URL + "1")
        data = res.json()

        self.assertEqual(
            res.status_code,
            200,
            MESSAGE + "wrong status code",
        )
        self.assertIn(
            "name",
            data,
            MESSAGE + "no 'name' property",
        )
        self.assertIn(
            "description",
            data,
            MESSAGE + "no 'description' property",
        )

    def test_put_amenity(self):
        MESSAGE = "Put amenity fail: "

        # permission check
        res = self.client.put(self.URL + "1")
        self.assertEqual(res.status_code, 403, MESSAGE + "wrong status code")

        self.client.force_login(self.staff_user)

        res = self.client.put(self.URL + "1")
        data = res.json()

        self.assertEqual(
            res.status_code,
            200,
            MESSAGE + "wrong status code",
        )
        self.assertIn(
            "name",
            data,
            MESSAGE + "no 'name' property",
        )
        self.assertIn(
            "description",
            data,
            MESSAGE + "no 'description' property",
        )

    def test_delete_amenity(self):
        MESSAGE = "DELETE amenity fail: "

        # permission check
        res = self.client.put(self.URL + "1")
        self.assertEqual(res.status_code, 403, MESSAGE + "wrong status code")

        #
        self.client.force_login(self.staff_user)

        self.assertEqual(
            res.status_code,
            204,
            "delete amenity",
        )
