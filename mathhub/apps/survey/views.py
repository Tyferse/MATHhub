import json
from collections import Counter
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def survey_page(request):
    # if request.method == 'POST':
    #     answers = request.POST.getlist('answers[]')
    #
    #     # Тут можно сохранять ответы в базу данных
    #     # или обрабатывать каким-либо другим способом
    #
    #     # В этом примере мы просто подсчитываем количество
    #     # уникальных ответов
    #     statistics = dict(Counter(answers))
    #
    #     return JsonResponse({'statistics': statistics})
    
    return render(request, 'survey/index.html')


@require_POST
@csrf_exempt
def save_answers(request):
    if request.method == 'POST':
        print('что-то произошло')
        print(repr(request.POST))
        try:
            rp = request.POST
            print('данные загружены')
            answers = [(key[key.index('[') + 1: -1],
                        rp[key][0] if len(rp[key]) == 1 else rp[key])
                       for key in rp if key.startswith('answers[')]
            print('ответы получены')
            
            value = k = 0  # результат игрока и множитель возраста
            personal_stat = []
            rank = 'Дефолтный математический нормис'
            if 0 < int(answers[0][1]) < 18:
                k = 1.5
            elif 18 <= int(answers[0][1]) < 36:
                k = 0.9
            elif 36 <= int(answers[0][1]) < 60:
                k = 1
            elif 60 <= int(answers[0][1]) < 80:
                k = 1.1
            else:
                k = 1.25
            
            if answers[1][1] in ['Алгебра', 'Геометрия']:
                value += 2
                personal_stat.append((answers[1][1],
                                      'Любитель попроще? Понимаю.', 2))
            elif answers[1][1] in ['Матан', 'Линал']:
                value += 4
                personal_stat.append((answers[1][1],
                                      'Нормальная математика пошла. Хорош.', 4))
            elif answers[1][1] in ['Теорвер', 'МатСтат']:
                value += 6
                personal_stat.append((answers[1][1],
                                      'Welcome to the club', 6))
            elif answers[1][1] in ['Диффуры', 'Компан (ТФКП)']:
                value += 8
                personal_stat.append(
                    (answers[1][1], 'А ты любитель острых ощущений', 8))
            elif answers[1][1] in ['Топология', 'Функан', 'Теормех']:
                value += 10
                personal_stat.append((answers[1][1], 'Соболезную', 10))
            
            if int(answers[2][1]) <= 10:
                value -= 10
                personal_stat.append(
                    (answers[1][1],
                     'Меньше 10 секунд!? Кому ты тут сказки '
                     'рассказываешь? В следующий раз либо отвечай '
                     'честно, либо не проходи этот тест больше никогда',
                     -10))
            elif 10 < int(answers[2][1]) < 60:
                value -= 5
                personal_stat.append(
                    (answers[1][1],
                     'Меньше минуты!? Это хотя бы не меньше 10 секунд, '
                     'но тоже невозможно. За то, что ты соврал(-а) '
                     'не так сильно, минус балл будет '
                     'не такой большой.',
                     -5))
            elif 60 <= int(answers[2][1]) < 600:
                value += 10
                personal_stat.append(
                    (answers[1][1],
                     'Вау! Меньше 10 минут на такое уравнение! '
                     'Уже звучит реалистично, потому заслуживает '
                     'уважения.',
                     10))
            elif 600 <= int(answers[2][1]) < 86400:
                value += 6
                personal_stat.append(
                    (answers[1][1],
                     'Ты потратил на решение меньше суток. '
                     'Уже не очень, но всё равно заслуживает '
                     '+ несколько баллов.',
                     6))
            elif 86400 <= int(answers[2][1]) < 2592000:
                value += 3
                personal_stat.append(
                    (answers[1][1],
                     'Меньше месяца на такую задачу? Мда...',
                     3))
            elif 2592000 <= int(answers[2][1]):
                value += 1
                personal_stat.append(
                    (answers[1][1],
                     'Как вообще можно было ввести такое значение? '
                     'Я не знаю. Тестируешь опрос что ли? '
                     'Ладно, держи 1 балл как тестировщик',
                     1))
            
            if answers[3][1] == 'Да':
                value += 10
                personal_stat.append((answers[3][1], 'Правильно', 10))
            elif answers[3][1] == 'Нет':
                value += 2
                personal_stat.append((answers[3][1], 'Неправильно', 2))
            else:
                value += 5
                personal_stat.append((answers[3][1],
                                      '5 очков на подумать.',
                                      5))
                
            if answers[4][1] == '0':
                value += 1
                personal_stat.append((answers[4][1], 'Кринж', 1))
            elif answers[4][1] == '1-3':
                value += 4
                personal_stat.append((answers[4][1],
                                      'Это только начало', 4))
            elif answers[4][1] == '4-10':
                value += 7
                personal_stat.append((answers[4][1],
                                      'Да вы прям знаток матана.', 7))
            elif answers[4][1] == '> 10':
                value += 10
                personal_stat.append(
                    (answers[4][1],
                     'Так много не знает, наверное, даже сам Коши.',
                     10))
            else:
                personal_stat.append(
                    (answers[4][1],
                     'Скоро узнаешь, но всё равно кринж',
                     0))
            
            if answers[5][1] == '?':
                value -= 1
                personal_stat.append((answers[5][1], 'Минус балл', -1))
            elif answers[5][1] == 'Не нашёл':
                value += 2
                personal_stat.append(
                    (answers[5][1],
                     'А теперь найди и больше не теряй',
                     2))
            else:
                value += 10
                personal_stat.append((answers[5][1],
                                      'Молодец',
                                      10))
            
            if answers[6][1] == ('y\' = -1/2 * e^{-x} + 1; '
                                 'y = 1/2 * e^{-x} + x + 2'):
                value += 10
                personal_stat.append(
                    (answers[6][1],
                     'Это абсолютно правильный ответ! '
                     'Возьми с полки пирожок', 10))
            else:
                value += 2
                personal_stat.append(
                    (answers[6][1],
                     'Ответ неправильный, но за попытку '
                     '(или её отсутствие), можно накинуть', 2))
            
            if answers[7][1] in ['e', 'π', 'Φ', 'i', 'Ω']:
                value += 6
                personal_stat.append(
                    (answers[7][1], 'Вполне нормисная константа', 6))
            elif answers[7][1] in ['γ - постоянная Эйлера-Маскерони',
                                   'ζ(3) - постоянная Апери',
                                   'λ - постоянная Голомба — Дикмана']:
                value += 8
                personal_stat.append(
                    (answers[7][1], 'Довольно редкая константа.', 8))
            else:
                value += 10
                personal_stat.append(
                    (answers[7][1], 'А вы ценитель больших чисел', 10))
            
            if answers[8][1] == '0':
                value += 1
                personal_stat.append((answers[8][1], 'Неодобряемо', 1))
            elif answers[8][1] == '1-9':
                value += 3
                personal_stat.append((answers[8][1],
                                      'Прикоснулся к великому', 4))
            elif answers[8][1] == '10-100':
                value += 6
                personal_stat.append((answers[8][1],
                                      'Уважение и хвала воину', 7))
            elif answers[8][1] == '> 100':
                value += 10
                personal_stat.append(
                    (answers[8][1],
                     'Вот бы мужчины вместо года в армии '
                     'год решали Демидовича... '
                     'Это мир был бы прекрасен',
                     10))
            else:
                personal_stat.append(
                    (answers[8][1],
                     'Сборник задач по матанализу. '
                     'Такую базу должен знать каждый математик.',
                     0))
            
            value = round(value * k)
            if value < 10:
                rank = 'Рус'
            elif value < 30:
                rank = 'Человек'
            elif value < 40:
                pass
            elif value < 50:
                rank = 'Жёсткий математик'
            elif value < 65:
                rank = 'Математический Моцарт'
            elif value >= 65:
                rank = 'Ящер'
            
            statistics = [[f'{q} | Ваш ответ: {a}', d, f'Результат: {s}']
                          for (a, d, s), (q, ans)
                          in zip(personal_stat, answers[1:])]
            
            return JsonResponse({'rank': rank,
                                 'statistics': statistics,
                                 'score': value})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'},
                                status=400)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'},
                            status=405)
