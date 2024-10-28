"""
Clase base para manejar errores.
"""

import logging
import re
import sys
import traceback


class ErrorHandler:
    """
    Clase que proporciona métodos para manejar y registrar errores de manera reutilizable.
    """

    def handle_error(
        self, message: str, logger: logging.Logger, exit_code: int = 1
    ) -> None:
        """
        Maneja los errores registrándolos y finalizando el programa.

        :param message: Mensaje de error a registrar.
        :param logger: Logger que se utilizará para registrar el error.
        :param exit_code: Código de salida del programa. 1 para terminar el programa,
        != 1 para seguir con el programa a pesar del error.
        """
        # Obtener detalle del error
        detailed_traceback = traceback.format_exc()

        # Construir mensaje de error final
        if re.search("NoneType: None", detailed_traceback):
            message = f"{message}"
        else:
            message = f"{message}\n{detailed_traceback}"

        # Mostrar el error critico de consola y finalizar el programa
        if exit_code == 1:
            print(message, file=sys.stderr)
            logger.critical(message + "\n")
            sys.exit(exit_code)
        else:
            logger.error(message)
