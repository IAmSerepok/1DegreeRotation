from PIL import Image


class PillowRotator:
    """Класс для многократного поворота изображений на малый градус с использованием библиотеки Pillow.

    Attributes:
        input_path (str): Путь к исходному изображению.
        output_path (str): Путь для сохранения результата.
        angle (float): Угол поворота в градусах.
    """

    def __init__(self, input_path: str, output_path: str, angle: float) -> None:
        """Инициализация врящателя изображений.

        Args:
            input_path (str): Путь к исходному файлу изображения.
            output_path (str): Путь для сохранения повернутого изображения.
            angle (float): Угол поворота в градусах (положительный - против часовой стрелки).
        """
        self.input_path = input_path
        self.output_path = output_path
        self.angle = angle

    def __rotate_image(self, input_path: str, output_path: str) -> None:
        """Поворачивает изображение и сохраняет результат.

        Args:
            input_path (str): Путь к изображению для поворота.
            output_path (str): Путь для сохранения результата.
        """
        image = Image.open(input_path).convert("RGB")
        rotated_image = image.rotate(self.angle)
        rotated_image.save(output_path)
        image.close()

    def process(self, n_iter: int) -> None:
        """Выполняет многократный поворот изображения.

        Args:
            n_iter (int): Количество итераций поворота.
        """
        self.__rotate_image(self.input_path, self.output_path)
        for _ in range(n_iter - 1):
            self.__rotate_image(self.output_path, self.output_path)


if __name__ == "__main__":  # Пример использования класса
    rotator = PillowRotator(
        input_path='input/line.png', 
        output_path='output/image/result.png',
        angle=3
    )
    rotator.process(200)
