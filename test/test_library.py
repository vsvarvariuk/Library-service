from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


from library.models import Book, Borrowing


class NonAuthenticateUser(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_access_for_books_not_authenticate_user(self):
        res = self.client.get(reverse("library:book-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_not_authenticate_user_cant_see_borrowings(self):
        res = self.client.get(reverse("library:borrowing-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticateUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="testuser@gmail.com", password="testuser12345"
        )
        self.client.force_authenticate(user=self.user)

    def create_book(self):
        return Book.objects.create(
            title="Testtitle",
            author="Testauthor",
            cover="Hardcover",
            inventory=5,
            daily_free=1.5,
        )

    def create_borrowing(self, book=None, expected_return_date=None):
        if book is None:
            book = self.create_book()
        if expected_return_date is None:
            expected_return_date = date(2025, 4, 15)
        return Borrowing.objects.create(
            expected_return_date=expected_return_date, book=book, user=self.user
        )

    def test_borrowings_list_and_detail_is_allow(self):
        borrowing = self.create_borrowing()
        res = self.client.get(reverse("library:borrowing-list"))
        res_2 = self.client.get(
            reverse("library:borrowing-detail", args=[borrowing.id])
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)

    def test_can_create_borrowing(self):
        book = self.create_book()
        data = {"book": book.id, "expected_return_date": "2025-04-12"}
        res = self.client.post(reverse("library:borrowing-list"), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_patch_and_put_not_allow(self):
        borrowing = self.create_borrowing()
        data = {"expected_return_date": "2025-04-30"}
        res = self.client.patch(
            reverse("library:borrowing-detail", args=[borrowing.id]), data
        )
        res_2 = self.client.put(
            reverse("library:borrowing-detail", args=[borrowing.id]), data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="email@gmail.com", password="test12345", is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def create_book(self):
        return Book.objects.create(
            title="Testtitle",
            author="Testauthor",
            cover="Hardcover",
            inventory=5,
            daily_free=1.5,
        )

    def create_borrowing(self, book=None, expected_return_date=None):
        if book is None:
            book = self.create_book()
        if expected_return_date is None:
            expected_return_date = date(2025, 4, 15)
        return Borrowing.objects.create(
            expected_return_date=expected_return_date, book=book, user=self.user
        )

    def test_post_is_allow(self):
        data = {
            "title": "Test",
            "author": "author",
            "cover": "HARD",
            "inventory": 5,
            "daily_free": 1.5,
        }
        res = self.client.post(reverse("library:book-list"), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Test")

    def test_patch_is_allow(self):
        book = self.create_book()
        data = {"title": "Harry Potter"}
        res = self.client.patch(reverse("library:book-detail", args=[book.id]), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Harry Potter")

    def test_put_is_allow(self):
        book = self.create_book()
        data = {
            "title": "Test",
            "author": "author",
            "cover": "HARD",
            "inventory": 5,
            "daily_free": 1.5,
        }
        res = self.client.put(reverse("library:book-detail", args=[book.id]), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Test")

    def test_admin_can_delete(self):
        book = self.create_book()
        res = self.client.delete(reverse("library:book-detail", args=[book.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_borrowing_by_user(self):
        book_2 = Book.objects.create(
            title="Harry", cover="Hardcover", author="Jack", inventory=5, daily_free=1.5
        )
        borrowing_1 = self.create_borrowing()

        user_2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="Jack",
            last_name="Morgan",
        )
        borrowing_2 = Borrowing.objects.create(
            expected_return_date=date(2025, 4, 16), book=book_2, user=user_2
        )

        res = self.client.get(reverse("library:borrowing-list"), {"user": "Ja"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["user"], "Jack Morgan")

    def test_filter_borrowings_by_is_active(self):
        book_2 = Book.objects.create(
            title="Potter",
            cover="Hardcover",
            author="Jack",
            inventory=5,
            daily_free=1.5,
        )
        borrowing_1 = self.create_borrowing()

        user_2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="Jack",
            last_name="Morgan",
        )
        borrowing_2 = Borrowing.objects.create(
            expected_return_date=date(2025, 4, 16), book=book_2, user=user_2
        )
        data = {"actual_return_date": date.today()}
        self.client.patch(
            reverse("library:borrowing-return", args=[borrowing_1.id]), data
        )
        res = self.client.get(reverse("library:borrowing-list"), {"is_active": "true"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["user"], "Jack Morgan")
