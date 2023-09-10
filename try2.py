from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        """Возвращает строку сообщения."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        time_in_min = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIES_MEAN_SPEED * mean_speed
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * time_in_min)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    duration: float
    weight: int
    height: int

    WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    COEF_IN_MH_IN_HOUR: ClassVar[float] = 0.278
    MULTIPLIER_AVERAGE_SPEED: ClassVar[float] = 0.029
    METERS_IN_SM: ClassVar[int] = 100

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.COEF_IN_MH_IN_HOUR
        time_in_min = self.duration * self.MIN_IN_HOUR
        height_in_meters = self.height / self.METERS_IN_SM
        return (self.WEIGHT_MULTIPLIER * self.weight + (mean_speed ** 2 / height_in_meters) * self.MULTIPLIER_AVERAGE_SPEED * self.weight) * time_in_min
    #(0.035 * weight + ((speed*0.278)**2 / (height/100)*0.029*weight)*duration*0.029


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    action: int
    duration: float
    weight: int

    LEN_STEP: ClassVar[float] = 1.38
    OFFSET_VALUE_MEAN: ClassVar[float] = 1.1
    SWIM_SPEED_MULTIPLIER: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((mean_speed + self.OFFSET_VALUE_MEAN)
                * self.SWIM_SPEED_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_training_cls_map: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type not in workout_type_training_cls_map:
        raise ValueError('Внимание! Такой тренировки не существует!')

    return workout_type_training_cls_map[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)