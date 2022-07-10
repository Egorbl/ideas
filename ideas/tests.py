import json
import requests

BASE_URL = "http://localhost:8000/api/"

token_user = '6c02fcb3ee90fb7cdc6b62489b2038907e3d5f2f'
token_admin = '16141661ccac74a5d4e0fdff389ef0f9f8dfd8fe'
invalid_token = '123'
nonexistant_token = '8d03d68a7c54c45290a7f8838236a8282061f25a'

register_200 = [
    {
        'data': {
            'email': 'user_1@mail.ru',
            'username': 'user_1',
            'password': '1234567',
            'password2': '1234567'
        }
    }
]

register_400 = [
    # 1. no_email
    {
        'data': {
            'username': 'user_2',
            'password': '1234567',
            'password2': '1234567'
        }
    },
    # 2. no_username
    {
        'data': {
            'email': 'user_2@mail.ru',
            'password': '1234567',
            'password2': '1234567'
        }
    },
    # 3. no_password1
    {
        'data': {
            'email': 'user_2@mail.ru',
            'username': 'user_2',
            'password2': '1234567'
        }
    },
    # 4. no_password2
    {
        'data': {
            'email': 'user_2@mail.ru',
            'username': 'user_2',
            'password': '1234567'
        }
    },
    # 5. invalid email
    {
        'data': {
            'email': 'user_2@mail',
            'username': 'user_2',
            'password': '1234567',
            'password2': '1234567'
        }
    },
    # 6. password1 != password2
    {
        'data': {
            'email': 'user_2@mail.ru',
            'username': 'user_2',
            'password': '1234567',
            'password2': '12345678'
        }
    },
    # 7. User is already exists
    {
        'data': {
            'email': 'user_3@mail.ru',
            'username': 'user_1',
            'password': '1234567',
            'password': '1234567'
        }
    },
    # 8. Email is already related to user
    {
        'data': {
            'email': 'user_1@mail.ru',
            'username': 'user_3',
            'password': '1234567',
            'password': '1234567'
        }
    }
]

login_200 = [
    {
        'data': {
            'username': 'user_1@mail.ru',
            'password': '1234567'
        }
    }
]

login_400 = [
    # 1. no such user
    {
        'data': {
            'username': 'user_3@mail.ru',
            'password': '1234567'
        }
    },
    # 2. invalid password
    {
        'data': {
            'username': 'user_1@mail.ru',
            'password': '123456'
        }
    },
    # 3. No password field
    {
        'data': {
            'username': 'user_1@mail.ru'
        }
    }
]

tags_200 = [
    {
        'token': token_admin,
        'data': {
            'name': 'C++'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag2'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag3'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag4'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag5'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag6'
        }
    },
    {
        'token': token_admin,
        'data': {
            'name': 'Tag7'
        }
    }
]

tags_400 = [
    # 1. no name
    {
        'token': token_admin,
        'data': {
        }
    },
    # 2. user is not admin
    {
        'token': token_user,
        'data': {
            'name': 'Something5'
        }
    },
    # 3. name already exists
    {
        'token': token_admin,
        'data': {
            'name': 'C++'
        }
    },
    # 4. name is null
    {
        'token': token_admin,
        'data': {
            'name': None
        }
    },
    #  5. no user token
    {
        'data': {
            'name': 'lalala'
        }
    },
    # 6. Invalid token
    {
        'token': invalid_token,
        'data': {
            'name': 'Smth11'
        }
    },
    # 7. Token does not exist
    {
        'token': nonexistant_token,
        'data': {
            'name': 'Smth12'
        }
    }
]

# tag: None, only_my: None, category: None, new_or_popular: 'new', only_actual: True
# required: id, category, title, content. Optional: tags
ideas_post_200 = [
    # 1. Default user
    {
        'token': token_user,
        'data': {
            'id': '00000001-e80b-12d3-a456-426614174000',
            'category': 'programming',
            'title': 'Site1',
            'content': 'Making site 1',
            'tags': [1, 2]
        }
    },
    # 2. Admin user
    {
        'token': token_admin,
        'data': {
            'id': '00000002-e80b-12d3-a456-426614174000',
            'category': 'programming',
            'title': 'Site2',
            'content': 'Making site 2',
            'tags': [1, 2, 3]
        }
    },
    # 3. No tags
    {
        'token': token_user,
        'data': {
            'id': '00000003-e80b-12d3-a456-426614174000',
            'category': 'science',
            'title': 'Site3',
            'content': 'Making site 3'
        }
    },
    # 4. Same title
    {
        'token': token_user,
        'data': {
            'id': '00000004-e80b-12d3-a456-426614174000',
            'category': 'science',
            'title': 'Site3',
            'content': 'Making another site 3',
            'tags': [4, 5]
        }
    },
    # 5.
    {
        'token': token_user,
        'data': {
            'id': '00000005-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 1',
            'content': 'Art 1',
            'tags': [4, 5, 6]
        }
    },
]
ideas_post_400 = [
    # 1. No category
    {
        'token': token_user,
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'title': 'Art 2',
            'content': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
    # 2. No title
    {
        'token': token_user,
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'category': 'art',
            'content': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
    # 3. No content
    {
        'token': token_user,
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
    # 4. No tag for some tag id
    {
        'token': token_user,
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 2',
            'content': 'Art 2',
            'tags': [4, 5, 6, 22]
        }
    },
    # 5. User is not authenticated
    {
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 2',
            'content': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
    # 6. Wrong token
    {
        'token': invalid_token,
        'data': {
            'id': '00000006-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 2',
            'content': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
    # 7. Id already exists
    {
        'token': token_user,
        'data': {
            'id': '00000001-e80b-12d3-a456-426614174000',
            'category': 'art',
            'title': 'Art 2',
            'content': 'Art 2',
            'tags': [4, 5, 6]
        }
    },
]

comment_post_200 = [
    # 1. Admin user
    # {
    #     "token": token_admin,
    #     "id_path": "00000001-e80b-12d3-a456-426614174000",
    #     "data": {
    #         "id": "00000001-e80b-12d3-a456-426614173000",
    #         "content": "Your post is very good!"
    #     }
    # },
    # 2. Default user
    {
        "token": token_user,
        "id_path": "00000001-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000002-e80b-12d3-a456-426614173000",
            "content": "Your post is very good!!!!!!!!!!!!!!!!!"
        }
    },
    {
        "token": token_user,
        "id_path": "00000001-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000003-e80b-12d3-a456-426614173000",
            "content": "Your post is very bad!!!!!!!!!!!!!!!!!"
        }
    },
    {
        "token": token_user,
        "id_path": "00000002-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000004-e80b-12d3-a456-426614173000",
            "content": "Nice"
        }
    },
    {
        "token": token_user,
        "id_path": "00000003-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000005-e80b-12d3-a456-426614173000",
            "content": "Your post ..!!!!!"
        }
    },
]

comments_post_400 = [
    # 1. No token
    {
        "id_path": "00000001-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000006-e80b-12d3-a456-426614173000",
            "content": "Your post ..!!!!!"
        }
    },
    # 2. Invalid token
    {
        "token": invalid_token,
        "id_path": "00000001-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000006-e80b-12d3-a456-426614173000",
            "content": "Your post ..!!!!!"
        }
    },
    # 3. Invalid idea uuid
    {
        "token": token_user,
        "id_path": "00000001-e80b-12d3-a456",
        "data": {
            "id": "00000006-e80b-12d3-a456-426614173000",
            "content": "Your post ..!!!!!"
        }
    },
    # 4. Idea uuid does not exists
    {
        "token": token_user,
        "id_path": "00000001-e80b-12d3-a466-426614174000",
        "data": {
            "id": "00000006-e80b-12d3-a456-426614173000",
            "content": "Your post ..!!!!!"
        }
    },
    # 5. No content
    {
        "token": token_user,
        "id_path": "00000001-e80b-12d3-a456-426614174000",
        "data": {
            "id": "00000006-e80b-12d3-a456-426614173000"
        }
    },
]

likes_post_200 = [
    {
        'token': token_admin,
        'id_path': '00000001-e80b-12d3-a456-426614174000',
        'data': {
            'id': '00000001-e80b-12d3-a300-426614174000'
        }
    },
    {
        'token': token_user,
        'id_path': '00000001-e80b-12d3-a456-426614174000',
        'data': {
            'id': '00000002-e80b-12d3-a300-426614174000'
        }
    }
]

ideas_patch_200 = [
    {
        'token': token_user,
        'id_path': '00000001-e80b-12d3-a456-426614174000',
        'data': {}
    },
    {
        'token': token_user,
        'id_path': '00000005-e80b-12d3-a456-426614174000',
        'data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    }
]

ideas_patch_400 = [
    # 1. Invalid token
    {
        'token': invalid_token,
        'id_path': '00000004-e80b-12d3-a456-426614174000',
        'data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    },
    # 2. Request user is not owner
    {
        'token': token_admin,
        'id_path': '00000004-e80b-12d3-a456-426614174000',
        '   data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    },
    # 3. User is not authenticated
    {
        'id_path': '00000004-e80b-12d3-a456-426614174000',
        'data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    },
    # 4. Invalid id_path
    {
        'token': token_user,
        'id_path': '00000004-e80b-12d3-a456',
        'data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    },
    # 5. Not existing id_path
    {
        'token': token_user,
        'id_path': '00000004-e80b-12d3-a456-426614174123',
        'data': {
            'content': "I would like to make a perfect programm!",
            'is_actual': False
        }
    },
    # 7. content is null
    {
        'token': token_user,
        'id_path': '00000004-e80b-12d3-a456-426614174000',
        'data': {
            'content': None,
            'is_actual': False
        }
    }
]

comments_patch_200 = [
    {
        "token": token_user,
        "id_path": "00000002-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Your post is very good!!!!!!!!!!!!!!!!!PATCH"
        }
    },
    {
        "token": token_user,
        "id_path": "00000003-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Your post is very bad!!!!!!!!!!!!!!!!!PATCH"
        }
    },
    {
        "token": token_user,
        "id_path": "00000004-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Nice.PATCH"
        }
    },
]

comments_patch_400 = [
    # 1. No token
    {
        "id_path": "00000004-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Nice.PATCH. ERROR"
        }
    },
    # 2. Token is not valid
    {
        "token": invalid_token,
        "id_path": "00000004-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Nice.PATCH. ERROR"
        }
    },
    # 3. Token is not exist
    {
        "token": nonexistant_token,
        "id_path": "00000004-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Nice.PATCH. ERROR"
        }
    },
    # 4. User is not owner
    {
        "token": token_admin,
        "id_path": "00000004-e80b-12d3-a456-426614173000",
        "data": {
            "content": "Nice.PATCH. ERROR"
        }
    },
]

delete_idea_200 = [
    {
        "token": token_user,
        'id_path': '00000005-e80b-12d3-a456-426614174000',
    }
]

delete_idea_400 = [
    # 1. No token
    {
        'id_path': '00000003-e80b-12d3-a456-426614174000',
    },
    # 2. Invalid token
    {
        "token": invalid_token,
        'id_path': '00000003-e80b-12d3-a456-426614174000',
    },
    # 3. User is not owner
    {
        "token": token_user,
        'id_path': '00000002-e80b-12d3-a456-426614174000',
    },
    # 4. No such idea id
    {
        "token": token_user,
        'id_path': '00000005-e80b-12d3-a456-426614174000',
    }
]

delete_comment_200 = [
    {
        "token": token_user,
        "id_path": "00000003-e80b-12d3-a456-426614173000",
    }
]

delete_comment_400 = [
    # 1. No token
    {
        "id_path": "00000002-e80b-12d3-a456-426614173000"
    },
    # 2. Invalid token
    {
        "token": invalid_token,
        "id_path": "00000002-e80b-12d3-a456-426614173000"
    },
    # 3. User is not owner
    {
        "token": token_admin,
        "id_path": "00000002-e80b-12d3-a456-426614173000"
    },
    # 4. Comment is not exist
    {
        "token": token_user,
        "id_path": "00000002-e80c-12d3-a456-426614173000"
    },
    # 5. Incorrect uuid
    {
        "token": token_user,
        "id_path": "00000002-e80b-12d3-a456-4266141730001233444"
    },
]

delete_like_200 = [
    {
        'token': token_user,
        'id_path': '00000002-e80b-12d3-a300-426614174000',
    }
]

delete_like_400 = [
    # 1. No token
    {
        'id_path': '00000001-e80b-12d3-a300-426614174000',
    },
    # 2. Invalid token
    {
        'token': invalid_token,
        'id_path': '00000001-e80b-12d3-a300-426614174000',
    },
    # 3. User is not owner
    {
        'token': token_admin,
        'id_path': '00000001-e80b-12d3-a300-426614174000',
    },
    # 4. No like with that uuid
    {
        'token': token_user,
        'id_path': '00000001-e80b-12d3-a300-426614174011',
    },
    # 5. Incorrect uuid
    {
        'token': token_user,
        'id_path': '00000001-e80b-12d3-a300-4266141740001111111111',
    }
]

methods = {
    'get': requests.get,
    'post': requests.post,
    'delete': requests.delete,
    'patch': requests.patch
}


def test_url(
    path, request_method_name, expected_statuses, test_name,
    data=None, query_params=None, compare_with=None, error_message=None,
    second_part_path=None
):
    print(f'Starting {test_name}')
    url = BASE_URL + path

    data = data or [{}]

    for test_element in data:
        id_path = test_element.get('id_path')
        current_url = url
        if id_path:
            current_url += id_path

        if second_part_path:
            current_url += second_part_path

        print(f'Sending request to {current_url}')
        token = test_element.get('token')
        test_element = test_element.get('data')
        request_method = methods[request_method_name]
        headers = {}
        if request_method_name == 'post':
            print(f'Testing {test_element}')

        if token:
            headers['Authorization'] = f'Token {token}'

        response = request_method(
            current_url, json=test_element, params=query_params, headers=headers)
        try:
            print(response.json())
        except:
            pass

        assert response.status_code in expected_statuses, \
            f'Error: {error_message}. Status {response.status_code}'

        if compare_with is not None:
            response_data = json.loads(response.json())
            assert response_data == compare_with

    print(f'{test_name}: passed')


def main():
    # test_url('register/', 'post', [200], 'Register 200',
    #          data=register_200, error_message='Expected status 200')

    # test_url('register/', 'post', [400], 'Register 400',
    #          data=register_400, error_message='Expected status 400')

    # test_url('login/', 'post', [200], 'Login 200', data=login_200,
    #          error_message="Expected status 200")

    # test_url('login/', 'post', [400], 'Login 400', data=login_400,
    #          error_message='Expected status 400')

    # test_url('tags/', 'post', [200], 'Tag post 200',
    #          data=tags_200, error_message="Expected status 200")

    # test_url('tags/', 'post', [400, 401, 403], 'Tag post 400',
    #          data=tags_400, error_message="Expected status 400, 401 or 403")

    # test_url('ideas/', 'post', [200], 'Ideas post 200',
    #          ideas_post_200, error_message='Expected status 200')

    # test_url('ideas/', 'post', [400, 401], 'Idea post 400',
    #          data=ideas_post_400, error_message="Expected status 400 or 401")

    # test_url('ideas/', 'post', [200], 'Comments post 200', data=comment_post_200, error_message="Expected status 200",
    #          second_part_path='/comments/')

    # test_url('ideas/', 'post', [400, 401, 404], 'Comments post 400',
    #          data=comments_post_400, error_message="Expected status 400, 401, 404", second_part_path='/comments/')

    # test_url('publication/', 'post', [200], 'Likes post 200', data=likes_post_200,
    #          error_message='Expected status 200', second_part_path='/likes/')

    # test_url('ideas/', 'patch', [200], 'Ideas updating 200', data=ideas_patch_200,
    #          error_message='Expected response 200', second_part_path='/')

    # test_url('ideas/', 'patch', [400, 401, 403, 404], 'Ideas updating 400', data=ideas_patch_400,
    #          error_message='Expected response 400, 401, 403 or 404', second_part_path='/')

    # test_url('comments/', 'patch', [200], 'Comments updating 200',
    #          data=comments_patch_200, error_message='Expected status 200', second_part_path='/')

    # test_url('comments/', 'patch', [400, 401, 403, 404], 'Comments updating 400',
    #          data=comments_patch_400, error_message='Expected status 400', second_part_path='/')

    # test_url('ideas/', 'delete', [200], 'Idea delete 200', data=delete_idea_200,
    #          error_message='Expected status 200', second_part_path='/')

    # test_url('ideas/', 'delete', [400, 401, 403, 404], 'Idea delete 400', data=delete_idea_400,
    #          error_message='Expected status 400', second_part_path='/')

    # test_url('comments/', 'delete', [200], 'Comment delete 200', data=delete_comment_200,
    #          error_message='Expected status 200', second_part_path='/')

    # test_url('comments/', 'delete', [400, 401, 403, 404], 'Comment delete 400', data=delete_comment_400,
    #          error_message='Expected status 400', second_part_path='/')

    # test_url('likes/', 'delete', [200], 'Like delete 200', data=delete_like_200,
    #          error_message='Expected status 200', second_part_path='/')

    test_url('likes/', 'delete', [400, 401, 403, 404], 'Like delete 400', data=delete_like_400,
             error_message='Expected status 400', second_part_path='/')


if __name__ == '__main__':
    main()
