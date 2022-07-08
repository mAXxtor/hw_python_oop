from dataclasses import asdict, dataclass, fields
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Строка сообщения."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите метод get_spent_calories '
                                  'в классе %s.' % (type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    MEAN_SPEED_RATE_1 = 18
    MEAN_SPEED_RATE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.MEAN_SPEED_RATE_1
                * self.get_mean_speed()
                - self.MEAN_SPEED_RATE_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: int

    WEIGHT_RATE_1 = 0.035
    EXPONENTATION_RATE = 2
    WEIGHT_RATE_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        return ((self.WEIGHT_RATE_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.EXPONENTATION_RATE
                 // self.height)
                * self.WEIGHT_RATE_2
                * self.weight)
                * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    LEN_STEP = 1.38
    MEAN_SPEED_RATE = 1.1
    WEIGHT_RATE = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        return ((self.get_mean_speed()
                + self.MEAN_SPEED_RATE)
                * self.WEIGHT_RATE
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type:
        raise ValueError
    elif (len(fields(training_type[workout_type]))) != len(data):
        raise Exception
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    try:
        for workout_type, data in packages:
            main(read_package(workout_type, data))
    except ValueError:
        print(f'Неизвестный тип тренировки - {workout_type}')
    except Exception:
        print('Ошибка в количестве переданных параметров')
