let answers = {};

let surveyQuestions = [
  {
    question: 'Сколько тебе лет? (это нужно для более справедливого подсчёта результата)',
    type: 'range',
    min: -50,
    max: 125
  },
  {
    question: 'Какая область математики вам наиболее понятна? Выберите только одну.',
    type: 'select',
    options: ['Алгебра', 'Геометрия', 'Матан', 'Линал', 'Теорвер', 'МатСтат',
              'Диффуры', 'Компан (ТФКП)', 'Топология', 'Функан', 'Теормех']
  },
  {
    question: 'За сколько секунд ты бы примерно решил такое уравнение?',
    type: 'number',
    img: '/static/images/survey/equation1.png',
    min: 0,
    max: 31557945
  },
  {
    question: 'Очевидна ли для тебя эта картинка?',
    type: 'radio',
    img: '/static/images/survey/figure2.jpg',
    options: ['Да', 'Нет', 'Надо подумать']
  },
  {
    question: 'Сколько теорем, признаков, критериев, лемм, формул, неравенств и уравнений Коши вы знаете?',
    type: 'radio',
    options: ['0', '1-3', '4-10', '> 10', 'Кто это?']
  },
  {
    question: 'Найди вероятность',
    type: 'radio',
    options: ['?', 'Не нашёл', 'Нашёл, больше не теряй']
  },
  {
    question: 'Реши задачу Коши и укажи правильный вариант решения',
    type: 'radio',
    img: '/static/images/survey/problem3.png',
    options: ['y\' = 1/2 * e^{-x}; y = 1/2 * e^{-x} - 2',
              'y\' = -1/2 * e^{-x} + 1; y = 1/2 * e^{-x} + x + 2',
              'y\' = -1/2 * e^{-x} - 1; y = -1/2 * e^{-x} - x + 4',
              'y\' = -1/2 * e^{-x} + 1; y = 1/2 * e^{-x} + x + 4']
  },
  {
    question: 'Выбери свою любимую константу',
    type: 'radio',
    options: ['e', 'π', 'Φ', 'i', 'Ω', 'γ - постоянная Эйлера-Маскерони', 'ζ(3) - постоянная Апери',
              'λ - постоянная Голомба — Дикмана', 'g₆₄ - число Грэма', 'Rayo(10^100) = число Райо']
  },
  {
    question: 'Сколько решил задач из Демидовича? Только честно',
    type: 'radio',
    options: ['0', '1-9', '10-100', '> 100', 'кто?']
  }
];

function processAnswer(questionIndex, response) {
  let currentQuestion = surveyQuestions[questionIndex];
  answers[currentQuestion.question] = response;
}

// Функция для отображения формы для текущего вопроса опроса
function showQuestion(index) {
  let question = surveyQuestions[index];
  $('#question').empty(); // Очищаем контейнер от предыдущих элементов формы

  let questionElement;
  if (question.type === 'text') {
    questionElement = $('<input type="text" class="form-control">');
    questionElement.on('input', function () {
      let inputValue = $(this).val();
      if (inputValue.length !== 0 && inputValue.length < 256) {
        $('#next-btn').prop('disabled', true);
      }
      else {
        $('#next-btn').prop('disabled', false);
      }
    })
  }
  else if (question.type === 'number') {
    questionElement = $('<input type="number">');
    questionElement.attr('min', question.min);
    questionElement.attr('max', question.max);
    questionElement.attr('value', question.min);
    questionElement.on('input', function () {
      let inputValue = parseInt($(this).val());
      if (isNaN(inputValue) || (inputValue > question.max || inputValue < question.min)) {
        $('#next-btn').prop('disabled', true);
      }
      else {
        $('#next-btn').prop('disabled', false);
      }
    })
  }
  else if (question.type === 'select') {
    questionElement = $('<select class="form-select" aria-label="' + question.question + '">');
    question.options.forEach(function(option) {
      questionElement.append($('<option>').text(option));
    });
  }
  else if (question.type === 'range') {
    questionElement = $('<input type="range" class="form-range">');
    questionElement.attr('min', question.min);
    questionElement.attr('max', question.max);
  }
  else if (question.type === 'radio') {
    questionElement = $('<div>');
    question.options.forEach(function(option) {
      let check_div = $('<div class="form-check">');
      check_div.append($('<input class="form-check-input" type="radio" name="radioGroup" value="' + option + '">'));
      check_div.append($('<label class="form-check-label">').text(option));
      questionElement.append(check_div);
    });
    questionElement.find('input[type="radio"]:first').prop('checked', true);
  }

  if (index === 1 && parseInt(answers[surveyQuestions[0].question]) < 0) {
    $('#question').append($('<label>').text('Вау, да ты задолжал самому времени, чтобы пройти этот опрос пораньше. А ну быстро возвращайся назад в свою машину времени или отвечай на вопрос более честно.'));
    $('#next-btn').text('Назад');
    currentQuestionIndex = -1;
  }
  else {
    $('#question').append($('<label class="form-label">').text(question.question));
    if ('img' in question) {
      $('#question').append($('<img src="' + question.img + '">'));
      $('#question').append($('<br>'));
    }

    $('#question').append($('<br>'));
    $('#question').append(questionElement);
    if (question.type === 'range') {
      $('#question').append($('<span id="min-range-value">').text(question.min));
      $('#question').append($('<span id="max-range-value">').text(question.max));
      $('#question').append($('<span id="curr-range-value">').text(Math.floor((question.min + question.max) / 2)));
      $('#question input[type="range"]').on('input', function () {
        $('#curr-range-value').text($(this).val());
      });
    }
  }
}

let currentQuestionIndex = 0;
showQuestion(currentQuestionIndex);

function displayStatistics() {
  // Отправка ответов на сервер (AJAX)
  $.ajax({
    type: 'POST',
    url: window.location.origin + '/survey/save-answers/',
    data: {answers: answers},
    success: function(response) {
      $('h1').text('Твой ранг:').after('<h2>' + response.rank + '</h2>');
      $('#result').empty();

      response.statistics.forEach(function (q) {
        let elem = $('<div>');
        elem.append($('<p>').text(q[0]));
        elem.append($('<p class="res-desc">').text(q[1]));
        elem.append($('<p class="q-score">').text(q[2]));
        $('#result').append(elem);
      })
      $('#result').append($('<p id="survey-score">').text('Итоговый результат: ' + response.score));
      $('#result').show().css('display', 'flex');
    },
    error: function() {
      $('#result').text('Ошибка получения статистики').show();
    }
  });
}

$('#next-btn').on('click', function() {
  if (currentQuestionIndex < 0) {
    $('#next-btn').text('Далее');
    showQuestion(0);
    currentQuestionIndex = 0;
  }
  else {
    let currentQuestion = surveyQuestions[currentQuestionIndex];
    let response;

    // Получение данных ответа пользователя из формы в зависимости от типа вопроса
    if (currentQuestion.type === 'text') {
      response = $('#question input:text').val();
    }
    else if (currentQuestion.type === 'number') {
      response = $('#question input[type="number"]').val();
    }
    else if (currentQuestion.type === 'select') {
      response = $('#question select').val();
    }
    else if (currentQuestion.type === 'range') {
      response = $('#question input[type="range"]').val();
    }
    else if (currentQuestion.type === 'radio') {
      response = $('input[name="radioGroup"]:checked').val();
    }

    // Обработка ответа пользователя
    processAnswer(currentQuestionIndex, response);

    // Переход к следующему вопросу опроса
    currentQuestionIndex++;
    if (currentQuestionIndex === surveyQuestions.length - 1) {
      $('#next-btn').text('Узнать результат');
    }

    if (currentQuestionIndex < surveyQuestions.length) {
      showQuestion(currentQuestionIndex);
    }
    else {
      $('#question').empty();
      $('#next-btn').hide();
      displayStatistics();
    }
  }
});
