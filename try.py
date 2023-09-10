M_IN_KM = 1000

class InfoMessage:
    """Информационное сообщение о тренировке."""
    
    def __init__(self, training_type, duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    
    def get_message(self):
        return print(f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}. ')
    
    pass


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        distance = self.action * LEN_STEP / M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        InfoMessage.get_message()
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79 
        mean_speed = self.get_mean_speed()
        spent_calories = ((CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed + CALORIES_MEAN_SPEED_SHIFT)* self.weight / M_IN_KM * (self.duration*60)) 
        return spent_calories
    
run1 = Running(15000, 1, 75)
#run1.show_training_info()
info1 = InfoMessage('run', 3, 10, 5, 3000)
print('111')
print(info1.get_message())