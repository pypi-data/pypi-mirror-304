"""
Clase base para manejar los logs.
"""

import logging
import os
from typing import Optional


class LoggingHandler:
    """
    Clase base para manejar los logs.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        log_file: Optional[str] = None,
    ):
        """
        Inicializa el logger al instanciar la clase.

        :param log_file: Path del archivo .log donde se guardarán los logs.
        :type log_file: str
        """
        # Configurar nombre del logger
        self.name = name or self.__class__.__name__
        # Configura el formato de log
        self._log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        # Configura el logger en el momento de la instancia
        self._logger = self.configure_logger(self.name, log_file)

    @property
    def get_logger(self) -> logging.Logger:
        """
        Getter para acceder al logger actual.

        :return: El logger actual.
        :rtype: logging.Logger
        """
        return self._logger

    @property
    def get_log_format(self) -> str:
        """
        Getter para acceder al formato de log actual.

        :return: El formato de log actual.
        :rtype: str
        """
        return self._log_format

    @get_log_format.setter
    def set_log_format(self, new_format):
        """
        Setter para cambiar el formato de log actual.

        :param new_format: El nuevo formato de log.
        :type new_format: str
        :raises ValueError: Si el nuevo formato de log está vacío.
        """
        if not new_format:
            raise ValueError("El formato de log no puede estar vacío.")

        # Aquí podrías agregar más validaciones si es necesario
        self._log_format = new_format

        # Actualizar el formato en los handlers existentes
        for handler in self._logger.handlers:
            handler.setFormatter(logging.Formatter(self._log_format))

    def configure_logger(
        self,
        name: Optional[str] = None,
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """
        Configura un logger para la clase base.

        :param name: Nombre del logger.
        :type name: str
        :param log_file: Path opcional del archivo .log para guardar los logs.
        :type log_file: str
        :return: Logger configurado.
        :rtype: logging.Logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if log_file:
            # Si se pasa log_file, usar FileHandler para guardar logs en el archivo .log
            handler = self._create_file_handler(log_file)
        else:
            # Si no se pasa log_file, usar StreamHandler para mostrar logs por consola
            # y que no se genere error
            handler = self._create_stream_handler()

        # Anexar el handler al logger
        logger.addHandler(handler)

        return logger

    def _create_log_directory(self, log_file: str) -> None:
        """
        Crea la carpeta para el archivo de log.

        :param log_file: Path del archivo .log.
        :type log_file: str
        """
        # Obtener directorio padre del fichero log
        log_dir = os.path.dirname(log_file)
        # Crear el directorio si no existe
        os.makedirs(log_dir, exist_ok=True)

    def _create_file_handler(self, log_file: str) -> logging.FileHandler:
        """
        Crea y configura el FileHandler para el archivo .log.

        :param log_file: Path del archivo .log.
        :type log_file: str
        :return: FileHandler configurado.
        :rtype: logging.FileHandler
        """
        # Crear la carpeta para el archivo .log si no existe
        self._create_log_directory(log_file)

        # Configurar el FileHandler que es configurador de la salida de los logs
        # hacia el archivo .log
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(self.get_log_format))
        return file_handler

    def _create_stream_handler(self) -> logging.StreamHandler:
        """
        Crea y configura el StreamHandler para la salida de los logs por consola.

        :return: StreamHandler configurado.
        :rtype: logging.StreamHandler
        """
        # Configurar el StreamHandler que es configurador de la salida de los logs
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self.get_log_format))
        return stream_handler
