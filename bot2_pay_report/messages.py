__version__ = 0.0004

MESSAGES = {"hello1": "Я Бот АвтоМеханик и давай немного расскажу о себе.\n" \
                      "Я делюсь с тобой информацией полученной другими пользователями ранее из системы Autoteka " \
                      "по платной подписке.\n" \
                      "Поэтому она может быть не самой актуальной, но! бесплатно. По каким то машинам информации " \
                      "может и не быть вообще если ее ранее не загрузили ко мне в базу. \n\n" \
                      "*Вся информация у нас предоставляется бесплатно!*"
                      "Но есть система мотивации ввиде внутренних монет RQ. \n" \
                      "- Каждая монета позволяет получить один отчет.\n" \
                      "- Пригласи друга и получи +1 RQ\n" \
                      "- Загрузи отчет и получи +2 RQ\n\n" \
                      "Все очень просто просто начни у тебя есть 3 подарочных RQ.",
            "hello_short": "Привет.",
            "set_ref": "Введите номер пригласителя.\n" \
                       "Ввести его можно будет только один раз.\n" \
                       "Пригласителю буду начислены + 1 RQ",
            "referal1": "Для того чтобы пригласить друга перешлите ему сообщение ниже.",
            "referal2": "Вас приглашают в Бот с бесплатной базой Автотеки. Перейдите по ссылке t.me/automechanicbot" \
                        " и при первом старте укажите код друга {code}",
            "wallet": "Ваш баланс {rq} RQ",
            "error": "Не знаю что с этим делать!\n",
            "load_car": "Скопируйте ссылку в личном кабинете и отправте мне сообщением.\n\nЛибо /exit для выхода в основное меню.",
            "load_car_bad_link": "Ссылка которую вы отправили неправильная или повреждена.\n " \
                                 "Получить корректную ссылку можно войдя в личный кабинет https://avtoteka.ru/ " \
                                 "Далее перейти в раздел Отчеты. Выбрать отчет и нажать на кнпку Поделиться. " \
                                 "Ссылка автоматически скопируется в буфер обмена.",
            "load_old_car": "Данные по этой машине уже есть и они более свежие чем ваши.",
            "load_car_success": "Данные по машине добавлены а вам начисленно +2 RQ!",
            "get_request": "Введите данные на выбор:\n"
                           "- VIN заглавные латинские буквы и цифры\n"
                           "- гос.номер в формате Х777ХХ777 русские буквы, цифры без пробелов.",
            "get_car_info": "Есть отчет по {brand}\n {model}\n {year}\n от {createdAt}. ",
            "get_error1": "Нет данных по такому номеру. Проверьте что все правильно ввели и повторите попытку.",
            "get_error2": "У вас недостаточно RQ для получения отчета. Получить дополнительные RQ можно:\n" \
                          "- пригласив нового пользователя (+1 RQ)" \
                          "- добавив отчет о пашине в нашу базу (+2 RQ)",
            "ref_err_1": "Такого пользователя нет.\nПопробуйте еще раз.\n\nЛибо /exit для выхода в основное меню.",
            "ref_err_2": "У вас уже введен пригласитель.",
            "ref_code_not_numeric": "Код пригласителя может содержать только цифры. Проверте еще раз код который вводите.",
            "ref_info_1": "Если вас указывают как пригласителя вы получаете +1 RQ к текущему балансу.",
            "ref_add": "Друг добавлен и ему будет дополнительно начислен +1 RQ."}
