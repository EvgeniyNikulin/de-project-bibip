from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import json
import os.path
import functions


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> str | None:
        '''Добавляет модель'''
        model_to_json = model.model_dump_json().ljust(500) + '\n'
        # Открываем файл models.txt в режиме "добавление в конец файла".
        with open(f'{self.root_directory_path}/models.txt', 'a', encoding='utf8') as file_model:
            file_model.write(model_to_json)
        # Проверяем, есть ли файл models_index.txt.
        if os.path.exists(f'{self.root_directory_path}/models_index.txt'):
            # Если есть - открываем в режиме 'r+'.
            with open(f'{self.root_directory_path}/models_index.txt', 'r+', encoding='utf8') as file_model_index:
                model_index_list = file_model_index.readlines()
                line_number = len(model_index_list)
                model_index_to_csv = f'{model.id};{line_number + 1}'.ljust(500) + '\n'
                model_index_list.append(model_index_to_csv)
                new_model_index_list = [el.rstrip().split(';') for el in model_index_list]
                # Сортируем по id модели.
                new_model_index_list.sort(key=lambda x: x[0])
                # Переводим курсор в начало файла.
                file_model_index.seek(0)
                # Перезаписываем файл models_index.txt.
                for el in new_model_index_list:
                    file_model_index.write(f'{el[0]};{el[1]}'.ljust(500) + '\n')
        else:
            # Если нету - открываем в режиме 'w', чтобы файл создался, и записываем первую строку.
            with open(f'{self.root_directory_path}/models_index.txt', 'w', encoding='utf8') as file_model_index:
                model_index_to_csv = f'{model.id};1'.ljust(500) + '\n'
                file_model_index.write(model_index_to_csv)
        return None

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> str | None:
        '''Добавляет машину'''
        car_to_json = car.model_dump_json().ljust(500) + '\n'
        with open(f'{self.root_directory_path}/cars.txt', 'a', encoding='utf8') as file_car:
            file_car.write(car_to_json)
        if os.path.exists(f'{self.root_directory_path}/cars_index.txt'):
            with open(f'{self.root_directory_path}/cars_index.txt', 'r+', encoding='utf8') as file_car_index:
                car_index_list = file_car_index.readlines()
                line_number = len(car_index_list)
                car_index_to_csv = f'{car.vin};{line_number + 1}'.ljust(500) + '\n'
                car_index_list.append(car_index_to_csv)
                new_car_index_list = [el.rstrip().split(';') for el in car_index_list]
                new_car_index_list.sort(key=lambda x: x[0])
                file_car_index.seek(0)
                for el in new_car_index_list:
                    file_car_index.write(f'{el[0]};{el[1]}'.ljust(500) + '\n')
        else:
            with open(f'{self.root_directory_path}/cars_index.txt', 'w', encoding='utf8') as file_car_index:
                car_index_to_csv = f'{car.vin};1'.ljust(500) + '\n'
                file_car_index.write(car_index_to_csv)
        return None

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> None:
        '''Добавляет продажу'''
        sale_to_json = sale.model_dump_json().ljust(500) + '\n'
        with open(f'{self.root_directory_path}/sales.txt', 'a', encoding='utf8') as file_sale:
            file_sale.write(sale_to_json)
        if os.path.exists(f'{self.root_directory_path}/sales_index.txt'):
            with open(f'{self.root_directory_path}/sales_index.txt', 'r+', encoding='utf8') as file_sale_index:
                sale_index_list = file_sale_index.readlines()
                line_number = len(sale_index_list)
                sale_index_to_csv = f'{sale.sales_number};{line_number + 1}'.ljust(500) + '\n'
                sale_index_list.append(sale_index_to_csv)
                new_sale_index_list = [el.rstrip().split(';') for el in sale_index_list]
                new_sale_index_list.sort(key=lambda x: x[0])
                file_sale_index.seek(0)
                for el in new_sale_index_list:
                    file_sale_index.write(f'{el[0]};{el[1]}'.ljust(500) + '\n')
        else:
            with open(f'{self.root_directory_path}/sales_index.txt', 'w', encoding='utf8') as file_sale_index:
                sale_index_to_csv = f'{sale.sales_number};1'.ljust(500) + '\n'
                file_sale_index.write(sale_index_to_csv)
        with open(f'{self.root_directory_path}/cars.txt', 'r', encoding='utf8') as file_car, \
             open(f'{self.root_directory_path}/cars_index.txt', 'r', encoding='utf8') as file_car_index:
            car_index_list = file_car_index.readlines()
            # Для поиска нужной строки используем бинарный поиск по индексу.
            num_row_car = functions.binary_search(sale.car_vin, car_index_list)
            file_car.seek((num_row_car - 1) * 501)
            val = file_car.read(500).strip()
        car_to_dict = json.loads(val)
        obj_car = Car.model_validate(car_to_dict)
        obj_car.status = CarStatus.sold
        car_to_json = obj_car.model_dump_json().ljust(500) + '\n'
        with open(f'{self.root_directory_path}/cars.txt', 'r+', encoding='utf8') as file_car:
            file_car.seek((num_row_car - 1) * 502)
            file_car.write(car_to_json)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        '''Показывает доступные к продаже авто'''
        car_list = []
        with open(f'{self.root_directory_path}/cars.txt', 'r', encoding='utf-8') as file_car:
            data_car = file_car.read(500).rstrip()
            while data_car:
                data_car_to_dict = json.loads(data_car)
                obj_car = Car.model_validate(data_car_to_dict)
                if obj_car.status == status:
                    car_list.append(obj_car)
                data_car = file_car.read(500).rstrip()
        return car_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        '''Детальная информация машины по vin'''
        with open(f'{self.root_directory_path}/cars.txt', 'r', encoding='utf-8') as file_car, \
             open(f'{self.root_directory_path}/cars_index.txt', 'r', encoding='utf-8') as file_car_index, \
             open(f'{self.root_directory_path}/models_index.txt', 'r', encoding='utf-8') as file_model_index, \
             open(f'{self.root_directory_path}/models.txt', 'r', encoding='utf-8') as file_model:
            # Читаем строку с машиной.
            car_index_list = file_car_index.readlines()
            num_row_car = functions.binary_search(vin, car_index_list)
            # Если vin не нашелся, ничего не выводим.
            if num_row_car is None:
                return None
            file_car.seek((num_row_car - 1) * 501)
            data_car = file_car.read(500).rstrip()
            data_car_to_dict = json.loads(data_car)
            obj_car = Car.model_validate(data_car_to_dict)
            # Читаем строку с моделью.
            model_index_list = file_model_index.readlines()
            num_row_model = functions.binary_search(str(obj_car.model), model_index_list)
            file_model.seek((num_row_model - 1) * 501)
            data_model = file_model.read(500).rstrip()
            data_model_to_dict = json.loads(data_model)
            obj_model = Model.model_validate(data_model_to_dict)
        if obj_car.status == CarStatus.sold:
	        # Читаем строку с продажей.
            with open(f'{self.root_directory_path}/sales.txt', 'r', encoding='utf-8') as file_sale: 
                data_sale = file_sale.read(500).rstrip()
                while data_sale:
                    data_sale_to_dict = json.loads(data_sale)
                    obj_sale = Sale.model_validate(data_sale_to_dict)
                    if obj_sale.car_vin == vin:
                        sales_date = obj_sale.sales_date
                        sales_cost = obj_sale.cost
                        break
                    data_sale = file_sale.read(500).rstrip()
        else:
            sales_date = None
            sales_cost = None
        # Формируем объект CarFullInfo.
        result = CarFullInfo(vin=obj_car.vin, car_model_name=obj_model.name, car_model_brand=obj_model.brand, price=obj_car.price, date_start=obj_car.date_start, status=obj_car.status, sales_date=sales_date, sales_cost=sales_cost)
        return result

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> None:
        '''Обновляет vin машины'''
        with open(f'{self.root_directory_path}/cars_index.txt', 'r+', encoding='utf-8') as file_car_index, \
             open(f'{self.root_directory_path}/cars.txt', 'r+', encoding='utf-8') as file_car:
            car_index_list = file_car_index.readlines()
            num_row_car = functions.binary_search(vin, car_index_list)
            file_car.seek((num_row_car - 1) * 501)
            data_car = file_car.read(500).rstrip()
            data_car_to_dict = json.loads(data_car)
            obj_car = Car.model_validate(data_car_to_dict)
            # Меняем vin.
            obj_car.vin = new_vin
            new_car_vin_to_json = obj_car.model_dump_json().ljust(500) + '\n'
            # Перезаписываем строку с новым vin  в файл cars.txt.
            file_car.seek(0)
            file_car.seek((num_row_car - 1) * 502)
            file_car.write(new_car_vin_to_json)
            # Меняем vin в прочитанном списке car_index_list.
            data_vin = f'{vin};{num_row_car}'.ljust(500) + '\n'
            new_data_vin = f'{new_vin};{num_row_car}'.ljust(500) + '\n'
            vin_index = car_index_list.index(data_vin)
            car_index_list[vin_index] = new_data_vin
            # Сортируем новый список индекса.
            car_index_list.sort()
            # Перезаписываем заново файл cars_index.txt.
            file_car_index.seek(0)
            for el in car_index_list:
                file_car_index.write(el)

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> None:
        '''Удаляет продажу'''
        with open(f'{self.root_directory_path}/sales_index.txt', 'r+', encoding='utf-8') as file_sale_index, \
             open(f'{self.root_directory_path}/sales.txt', 'r+', encoding='utf-8') as file_sale, \
             open(f'{self.root_directory_path}/cars.txt', 'r+', encoding='utf-8') as file_car, \
             open(f'{self.root_directory_path}/cars_index.txt', 'r', encoding='utf-8') as file_car_index:
            sale_index_list = file_sale_index.readlines()
            num_row_sale = functions.binary_search(sales_number, sale_index_list)
            file_sale.seek((num_row_sale - 1) * 501)
            data_sale = file_sale.read(500).rstrip()
            data_sale_to_dict = json.loads(data_sale)
            obj_sale = Sale.model_validate(data_sale_to_dict)
            # Помечаем строку на удаление (в классе Sale, добавлено поле).
            data_sale_to_dict['is_deleted'] = 'True'
            # Перезаписываем строку.
            data_sale_to_json = json.dumps(data_sale_to_dict).ljust(500) + '\n'
            file_sale.seek(0)
            file_sale.seek((num_row_sale - 1) * 501)
            file_sale.write(data_sale_to_json)
            # Удаляем строку продажи из файла sale_index.txt.
            data_sale_index = f'{sales_number};{num_row_sale}'.ljust(500) + '\n'
            sale_index_list.remove(data_sale_index)
            # Список остается отсортированным.
            # Перезаписываем заново файл cars_index.txt.
            file_sale_index.seek(0)
            for el in sale_index_list:
                file_sale_index.write(el)
            # Меняем статус машины.
            car_index_list = file_car_index.readlines()
            num_row_car = functions.binary_search(obj_sale.car_vin, car_index_list)
            file_car.seek((num_row_car - 1) * 501)
            data_car = file_car.read(500).rstrip()
            data_car_to_dict = json.loads(data_car)
            data_car_to_dict['status'] = 'available'
            data_car_to_json = json.dumps(data_car_to_dict).ljust(500) + '\n'
            file_car.seek((num_row_car - 1) * 501)
            file_car.write(data_car_to_json)

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        '''Показывает топ-3 продаваемых моделей'''
        # Словарь для хранения количества каждой проданной модели.
        count_models_by_sales = {}
        # Словарь для хранения общей стоимости каждой проданной модели. Если количество совпадет, будем сортировать по общей стоимости.
        total_price_models_by_sales = {}
        with open(f'{self.root_directory_path}/sales.txt', 'r', encoding='utf-8') as file_sale, \
             open(f'{self.root_directory_path}/cars_index.txt', 'r', encoding='utf-8') as file_car_index, \
             open(f'{self.root_directory_path}/cars.txt', 'r', encoding='utf-8') as file_car:
            car_index_list = file_car_index.readlines()
            # Считываем первую строку из файла sales.txt.
            data_sale = file_sale.read(500).rstrip()
            # Читаем файл sales.txt. построчно.
            while data_sale:
                data_sale_to_dict = json.loads(data_sale)
                obj_sale = Sale.model_validate(data_sale_to_dict)
                # Проверяем, не удалена ли продажа.
                if obj_sale.is_deleted == False:
                    num_row_car = functions.binary_search(obj_sale.car_vin, car_index_list)
                    file_car.seek((num_row_car - 1) * 501)
                    data_car = file_car.read(500).rstrip()
                    data_car_to_dict = json.loads(data_car)
                    obj_car = Car.model_validate(data_car_to_dict)
                    count_models_by_sales[obj_car.model] = count_models_by_sales.get(obj_car.model, 0) + 1
                    total_price_models_by_sales[obj_car.model] = total_price_models_by_sales.get(obj_car.model, 0) + obj_sale.cost
                data_sale = file_sale.read(500).rstrip()
        # Формируем список из кортежей (модель, количество, общая стоимость).
        model_count_price = []
        for key, value in count_models_by_sales.items():
            model_count_price.append((key, value, total_price_models_by_sales[key]))
        # Сортурем сначала по количеству моделей, затем по общей стоимости.
        model_count_price.sort(key=lambda x: (x[1], x[2]), reverse=True)
        top_3_model_count_price = model_count_price[:3]
        top_3_models_by_sales = []
        with open(f'{self.root_directory_path}/models.txt', 'r', encoding='utf-8') as file_model, \
             open(f'{self.root_directory_path}/models_index.txt', 'r', encoding='utf-8') as file_model_index:
            model_index_list = file_model_index.readlines()
            for el in top_3_model_count_price:
                num_row_model = functions.binary_search(str(el[0]), model_index_list)
                file_model.seek((num_row_model - 1) * 501)
                data_model = file_model.read(500)
                data_model_to_dict = json.loads(data_model)
                obj_model = Model.model_validate(data_model_to_dict)
                # Формируем объект ModelSaleStats.
                res = ModelSaleStats(car_model_name=obj_model.name, brand=obj_model.brand, sales_number=el[1])
                top_3_models_by_sales.append(res)
                file_model.seek(0)
        return top_3_models_by_sales
