
function changeLanguage(language) {

    var languageContent = {
        'en': {
            'title': 'Text Classification',
            'chooseFileLabel': 'Choose a file:',
            'chooseModelLabel': 'Choose a model:',
            'classifyButton': 'Classify',
            'resultLabel': 'Classification Result:',
            'historyLabel': 'History'
        },
        'vi': {
            'title': 'Phân loại Văn bản',
            'chooseFileLabel': 'Chọn tệp:',
            'chooseModelLabel': 'Chọn mô hình:',
            'classifyButton': 'Phân loại',
            'resultLabel': 'Kết quả phân loại:',
            'historyLabel': 'Lịch sử'
        }
    };

    document.getElementById('title').textContent = languageContent[language]['title'];
    document.getElementById('chooseFileLabel').textContent = languageContent[language]['chooseFileLabel'];
    document.getElementById('chooseModelLabel').textContent = languageContent[language]['chooseModelLabel'];
    document.getElementById('classifyButton').textContent = languageContent[language]['classifyButton'];
    document.getElementById('resultLabel').textContent = languageContent[language]['resultLabel'];
    document.getElementById('historyLabel').textContent = languageContent[language]['historyLabel'];

    if (language === 'en') {
        showViFlag();
    }
    else if(language === 'vi'){
      showEngFlag();
    }
}

function changeTheme(theme) {
    var themeLink = document.getElementById('theme-link');

    if (theme === 'light') {
        showMoonTheme()
        themeLink.href = "{{ url_for('static', filename='theme-light.css') }}";
    } else if (theme === 'dark') {
        showSunTheme()
        themeLink.href = "{{ url_for('static', filename='theme-dark.css') }}";
    }
}

 function showMoonTheme() {
    document.getElementById('sunButton').style.display = 'none';
    document.getElementById('moonButton').style.display = 'inline';
}


function showSunTheme() {
    document.getElementById('moonButton').style.display = 'none';
    document.getElementById('sunButton').style.display = 'inline';
}

function showEngFlag() {
    document.getElementById('viButton').style.display = 'none';
    document.getElementById('engButton').style.display = 'inline';
}


function showViFlag() {
    document.getElementById('engButton').style.display = 'none';
    document.getElementById('viButton').style.display = 'inline';
}