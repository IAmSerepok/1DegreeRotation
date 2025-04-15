import cv2
import numpy as np

from typing import Optional


class CVRotatorVideo:
    """Класс для создания видео с многократным поворотом изображения на малый градус с использованием OpenCV.

    Attributes:
        angle (int): Угол поворота в градусах.
        original_image (np.ndarray): Исходное изображение в формате numpy array.
        width (int): Ширина изображения после дополнения до квадрата.
        height (int): Высота изображения после дополнения до квадрата.
    """

    def __init__(self, image_path: str, angle: float = 1) -> None:
        """Инициализация вращятеля.

        Args:
            image_path (str): Путь к исходному изображению.
            angle (float): Угол поворота для каждого кадра (по умолчанию 1 градус).
        """
        self.angle = angle
        self.original_image = cv2.imread(image_path)
        self.original_image = self.extend_to_square(self.original_image)
        self.height, self.width, _ = self.original_image.shape

    def process(self, n_iter: int, output_path: Optional[str] = None, fps: int = 60) -> None:
        """Основной метод обработки - отображает и/или сохраняет видео.

        Args:
            n_iter (int): Количество итераций (кадров) поворота.
            output_path (Optional[str]): Путь для сохранения видео (если None - только отображение).
            fps (int): Частота кадров для выходного видео.
        """
        # Инициализация VideoWriter если указан путь для сохранения
        if output_path is not None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (self.width, self.height))

        rotated_image = self.original_image

        for _ in range(n_iter):
            # Сохранение кадра в видео если нужно
            if output_path is not None:
                out.write(rotated_image)

            # Отображение текущего кадра
            cv2.imshow("Rotated Image", rotated_image)
            cv2.waitKey(1)  # Короткая пауза для отображения

            # Применение поворота
            rotated_image = self.rotate_image(rotated_image, self.angle)

        # Завершение записи видео
        if output_path is not None:
            out.release()

        # Ожидание закрытия окна
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """Поворачивает изображение на заданный угол.

        Args:
            image (np.ndarray): Входное изображение в формате numpy array.
            angle (float): Угол поворота в градусах.

        Returns:
            rotated_image (np.ndarray): Повернутое изображение.
        """
        rotation_matrix = cv2.getRotationMatrix2D((self.width / 2, self.height / 2), angle, 1)
        return cv2.warpAffine(image, rotation_matrix, (self.width, self.height))

    def extend_to_square(self, image: np.ndarray) -> np.ndarray:
        """Дополняет изображение до квадратной формы, добавляя черные поля.

        Args:
            image (np.ndarray): Входное изображение любой формы.

        Returns:
            extended_image (nd.array): Квадратное изображение с исходным изображением по центру.
        """
        height, width = image.shape[:2]
        max_dim = max(height, width)
        
        square_image = np.zeros((max_dim, max_dim, 3), np.uint8)
        start_y = (max_dim - height) // 2
        start_x = (max_dim - width) // 2
        square_image[start_y:start_y + height, start_x:start_x + width] = image
        
        return square_image


if __name__ == "__main__":  # Пример использования
    rotator = CVRotatorVideo('input/line.png', angle=0.3)
    rotator.process(1000)
