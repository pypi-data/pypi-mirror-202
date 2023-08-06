from logging_funcs import app_logger

if __name__ == "__main__":
    logger = app_logger()

    logger.set_current_user(current_username='DORSA')
    logger.create_new_log(message='This is a debug message', level=0)
    logger.create_new_log(message='This is a info message', level=1)
    logger.create_new_log(message='This is a warning message', level=2)
    logger.create_new_log(message='This is a error message', level=3)
    logger.create_new_log(message='This is a critical error message', level=4)
    logger.create_new_log(message='This is a excepion error message', level=5)