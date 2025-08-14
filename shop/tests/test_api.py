import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_category_crud(api_client):
    # CREATE
    r = api_client.post('/api/categories/', {'title': 'Музыка'}, format='json')
    assert r.status_code == 201
    cat_id = r.data['id']

    # LIST
    r = api_client.get('/api/categories/')
    assert r.status_code == 200
    assert any(c['id'] == cat_id for c in r.data)

    # DETAIL
    r = api_client.get(f'/api/categories/{cat_id}/')
    assert r.status_code == 200
    assert r.data['title'] == 'Музыка'

    # UPDATE
    r = api_client.patch(f'/api/categories/{cat_id}/', {'title': 'Новая музыка'}, format='json')
    assert r.status_code == 200
    assert r.data['title'] == 'Новая музыка'

    # DELETE
    r = api_client.delete(f'/api/categories/{cat_id}/')
    assert r.status_code == 204


@pytest.mark.django_db
def test_product_crud(api_client):
    # Сначала создаём категорию
    r = api_client.post('/api/categories/', {'title': 'Инструменты'}, format='json')
    category_id = r.data['id']

    product_data = {
        'title': 'Гитара',
        'category_id': category_id,
        'description': 'Акустическая гитара',
        'characteristics': 'Дерево, 6 струн',
        'price': '15000.00',
        'stock': 5
    }

    # CREATE
    r = api_client.post('/api/products/', product_data, format='json')
    assert r.status_code == 201
    product_id = r.data['id']

    # LIST
    r = api_client.get('/api/products/')
    assert r.status_code == 200
    assert any(p['id'] == product_id for p in r.data)

    # DETAIL
    r = api_client.get(f'/api/products/{product_id}/')
    assert r.status_code == 200
    assert r.data['title'] == 'Гитара'

    # UPDATE
    r = api_client.patch(f'/api/products/{product_id}/', {'price': '14000.00'}, format='json')
    assert r.status_code == 200
    assert r.data['price'] == '14000.00'

    # DELETE
    r = api_client.delete(f'/api/products/{product_id}/')
    assert r.status_code == 204


def create_test_image_file():
    # Создаём простое изображение 1x1 px в памяти
    image = Image.new('RGB', (1, 1), color='white')
    tmp_file = io.BytesIO()
    image.save(tmp_file, format='PNG')
    tmp_file.seek(0)
    return SimpleUploadedFile('test.png', tmp_file.read(), content_type='image/png')


@pytest.mark.django_db
def test_product_image_crud(api_client):
    # Создаём категорию
    cat_resp = api_client.post('/api/categories/', {'title': 'Струнные'}, format='json')
    category_id = cat_resp.data['id']

    # Создаём продукт с категорией
    prod_resp = api_client.post('/api/products/', {
        'title': 'Скрипка',
        'category_id': category_id,
        'description': '',
        'characteristics': '',
        'price': '20000.00',
        'stock': 3
    }, format='json')
    product_id = prod_resp.data['id']

    # Создаём валидный файл изображения
    image_file = create_test_image_file()

    # CREATE
    r = api_client.post('/api/product-images/', {
        'product': product_id,
        'image': image_file,
    }, format='multipart')
    assert r.status_code == 201, r.data
    image_id = r.data['id']

    # LIST
    r = api_client.get('/api/product-images/')
    assert r.status_code == 200
    assert any(i['id'] == image_id for i in r.data)

    # DETAIL
    r = api_client.get(f'/api/product-images/{image_id}/')
    assert r.status_code == 200

    # UPDATE - заменяем изображение новым
    new_image_file = create_test_image_file()
    r = api_client.patch(f'/api/product-images/{image_id}/', {'image': new_image_file}, format='multipart')
    assert r.status_code == 200

    # DELETE
    r = api_client.delete(f'/api/product-images/{image_id}/')
    assert r.status_code == 204
