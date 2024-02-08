<a href="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018d7941-3809-4ea6-93a1-7bfaf71eaefc"><img src="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018d7941-3809-4ea6-93a1-7bfaf71eaefc.svg" alt="wakatime"></a>
# Тестирование C кода с помощью cffi

## Используемые фреймворки и библиотеки

<strong>
<ul>
<li>Python</li>
<li>CFFI</li>
<li>Unittest</li>
<li>Numpy</li>
</ul>
</strong>

## Функционал

<strong>
<ol>
<li>Тестирование C файла, в котором содержатся функции операций с векторами и матрицами</li>
<li>Автоматическая генерация векторов и матриц для тестов</li>
<li>Парсинг C хедера</li>
<li>Логирование</li>
</ol>
</strong>

## Использование

<strong>
<ul>
<li>Установить все необходимые зависимости</li>
<li>Запустить главный исполняемый файл src/tests.py</li>
<li>В файле scr/parser_header.py парсер для заголовочного C файла name.h</li>
<li>В файле src/data_for_test.py класс для генерации матриц и векторов по названию</li>
<li>В файле src/matrix_operation.py numpy функции операций с векторами и матрицами</li>
<li>В папке src/logs файл с настройками логирования и сами логи</li>
</ul>
</strong>

