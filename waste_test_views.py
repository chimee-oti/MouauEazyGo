
class TestUpdateClassViewGet:
    def test_get_request_redirect(client):
        user = UserFactory()
        # RequestFactory().post(
        #     '/login/', data={'username': user.username, 'password': user.password})

        url = reverse('profile_update')
        request = RequestFactory().get(url, follow=False)
        request.user = AnonymousUser()
        response = views.update_profile.as_view()(request)

        assert response.status_code == 302, "should redirect"

    def test_get_request_with_login(client):
        user = UserFactory()
        RequestFactory().post(
            '/login/', data={'username': user.username, 'password': user.password})

        url = reverse('profile_update')
        request = RequestFactory().get(url, follow=False)
        request.user = user
        response = views.update_profile.as_view()(request)

        assert response.status_code == 200, "should work for logined in users"


new = Faker()
new_email = new.email()
new_username = new.user_name()
new_firstname = new.first_name()
new_lastname = new.last_name()
new_date_of_birth = new.date_of_birth()
new_image = factory.django.ImageField(filename="new_image.jpg")


class TestUpdateClientPost:
    def test_post_updates(client):
        user = UserFactory()
        RequestFactory().post(
            '/login/', data={'username': user.username, 'password': user.password})

        url = reverse('profile_update')

        data = {'email': new_email,
                'username': new_username,
                'firstname': new_firstname,
                'lastname': new_lastname,
                'date_of_birth': new_date_of_birth,
                'image': new_image}
        request = RequestFactory().post(url, data=data)
        request.user = user
        response = views.update_profile.as_view()(request)
        user = .user

        assert response.status_code == 302, "redirects to home"
        assert user.email == new_email
        assert user.username == new_username
        assert user.firstname == new_firstname
        assert user.lastname == new_lastname
        assert user.date_of_birth == new_date_of_birth
        assert user.image == new_image
