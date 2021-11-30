from api import PetFriends
from settings import valid_email, valid_password, empty_email, empty_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Дора', animal_type='такса', age='4', pet_photo='images/taksa.jfif'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Айси", "хаски", "3", "images/1.jfif")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Чуча', animal_type='пони', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_valid_data(name="Карлос", animal_type="утка", age="6"):
    # Проверка возможности создания питомца без фото

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_successful_add_pet_photo():
    # Проверка возможности добавления фото питомцу

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    foto = my_pets['pets'][0]['pet_photo']  # фото питомца на сайте до добавления нового

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], "images/1.jfif")
        assert status == 200
        assert foto != result["pet_photo"]  # проверка, что фото действительно поменялось, и оно отличается от старого
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_empty_data(animal_type="лошадь", age="10"):
        # Проверка возможности создания питомца без обязательного параметра name

        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet_without_photo_norequired_params(auth_key, animal_type, age)
        assert status == 400

def test_add_new_pet_without_photo_invalid_datatype(name="Лапуля", animal_type=121212, age="3"):
        # Проверка возможности создания питомца с числовым параметром вместо строкового

        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet_without_photo_invalid_datatype(auth_key, name, animal_type, age)
        assert status == 400  # тест упал, код 200, питомец успешно создается

def test_add_new_pet_with_large_parametr_name(name='вфаывыпрволываолрджоправожлдэлорпавыпролждэлокуешщгждюолбьтимьтбжгдшншеукуцкегшжлдюобпавпыаффывапролждэжшгенекуецкушщгжолдрпавыавфвапролднгнеекушгдплрптавыафвпролднекуецкеншгдлропавыафвфапролдрпавапвралдпоавыфывапрдлорпоавпыафываролдрлпоавпыапрооапрпопавпа'
                                     , animal_type='',age=''):
    """Проверяем можно ли добавить питомца c большим значением в параметре name"""

       # Запрашиваем api-ключ и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_large_parametr_type(name=''
                                     , animal_type='вфаывыпрволываолрджоправожлдэлорпавыпролждэлокуешщгждюолбьтимьтбжгдшншеукуцкегшжлдюобпавпыаффывапролждэжшгенекуецкушщгжолдрпавыавфвапролднгнеекушгдплрптавыафвпролднекуецкеншгдлропавыафвфапролдрпавапвралдпоавыфывапрдлорпоавпыафываролдрлпоавпыапрооапрпопавпа'
                                     ,age=''):
    """Проверяем можно ли добавить питомца c большим значением в параметре animal_type"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_large_parametr_age(name=''
                                     , animal_type=''
                                     ,age='вфаывыпрволываолрджоправожлдэлорпавыпролждэлокуешщгждюолбьтимьтбжгдшншеукуцкегшжлдюобпавпыаффывапролждэжшгенекуецкушщгжолдрпавыавфвапролднгнеекушгдплрптавыафвпролднекуецкеншгдлропавыафвфапролдрпавапвралдпоавыфывапрдлорпоавпыафываролдрлпоавпыапрооапрпопавпа'):
    """Проверяем можно ли добавить питомца c большим значением в параметре age"""

       # Запрашиваем api-ключ и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    result['age'] = age.isdigit()
    assert age.isdigit() == True
def test_add_new_pet_with_invalid_name(name="@@@%%%$$$", animal_type="Собака", age="3",
                                           pet_photo="images/taksa.jfif"):
        # Проверка возможности создания питомца с именем, состоящим только из спецсимволов

        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 400  # тест падает, код 200, питомец успешно создается
        assert result["name"] == name

def test_add_new_pet_without_photo_noncorrect(name='Гена', animal_type='крокодил',
                                     age='Сто'):
    """Проверяем можно ли добавить питомца с некорректными данными"""

       # Запрашиваем api-ключ и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    result['age'] = age.isdigit()
    assert age.isdigit() == False
def test_add_new_pet_without_parrametrs(name='', animal_type='',
                                     age=''):
    """Проверяем, можно ли добавить питомца с пустыми параметрами"""

       # Запрашиваем api-ключ и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_valid_data_empty_key(name="Ричард", animal_type="собака", age="2",
                                               pet_photo="images/1.jfif"):
    # Проверка возможности создания питомца без авторизации с пустым auth_key

    auth_key = {"key": ""}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403

def test_get_api_key_for_valid_password_empty_email(email=empty_email, password=valid_password):
    # Проверка возможности получить auth_key с существующим паролем и пустой почтой

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result  # убедиться, что ключ действительно не получен

def test_get_api_key_for_valid_password_empty_password(email=valid_email, password=empty_password):
    # Проверка возможности получить auth_key с существующей почтой и пустым паролем

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result  # убедиться, что ключ действительно не получен
