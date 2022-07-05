import dataclasses
from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Строка сообщения."""
        return self.message.format(**dataclasses.asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed: float = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        """Перевести длительность в минуты"""
        duration_min: float = self.duration * 60
        run: float = ((coeff_calorie_1
                      * self.get_mean_speed()
                      - coeff_calorie_2)
                      * self.weight
                      / self.M_IN_KM
                      * duration_min)
        return run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: int = 2
        coeff_calorie_3: float = 0.029
        """Перевести длительность в минуты"""
        duration_min: float = self.duration * 60
        walking: float = ((coeff_calorie_1
                          * self.weight
                          + (self.get_mean_speed() ** coeff_calorie_2
                           // self.height)
                          * coeff_calorie_3
                          * self.weight)
                          * duration_min)
        return walking


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        avg_swim_speed: float = (self.length_pool
                                 * self.count_pool
                                 / self.M_IN_KM
                                 / self.duration)
        return avg_swim_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        calories: float = ((self.get_mean_speed()
                           + coeff_calorie_1)
                           * coeff_calorie_2
                           * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_training:
        return dict_training[workout_type](*data)
    raise KeyError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
