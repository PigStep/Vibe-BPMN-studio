(function () {
    var TRANSLATIONS = {
        ru: {
            lang_switch: 'EN',
            app_title: 'Vibe BPMN Editor AI powered',
            open: 'Открыть',
            download_bpmn: 'Скачать .bpmn',
            download_svg: 'Скачать .svg',
            zoom_out: 'Уменьшить',
            zoom_in: 'Увеличить',
            fit_viewport: 'Подогнать',
            ai_assistant: 'AI Ассистент',
            xml: 'XML',
            chat_placeholder: 'Ваш запрос...',
            chat_send: 'Отправить',
            xml_edit_label: 'Редактирование источника',
            apply: 'Применить',
            hint_text: 'Опишите вашу предметную область. Или загрузите ваш XML код для старта редактирования',
            status_online: 'Online',
            notification_hint: 'Справка: Вы можете загрузить свой XML код в отдельном пункте XML. Используйте, если хотите отрисовать XML с помощью сторонней LLM',
            error_unavailable: 'К сожалению, сервис AI недоступен. Попробуйте позже.',
            error_ai_unavailable: 'Сервис AI не отвечает. Используйте панель XML код и сторонний LLM.',
            error_generic: 'К сожалению, произошла ошибка. Попробуйте позже.',
            request_in_progress: 'Запрос уже выполняется. Дождитесь ответа.',
            success: 'Готово!',
        },
        en: {
            lang_switch: 'RU',
            app_title: 'Vibe BPMN Editor AI powered',
            open: 'Open',
            download_bpmn: 'Download .bpmn',
            download_svg: 'Download .svg',
            zoom_out: 'Zoom Out',
            zoom_in: 'Zoom In',
            fit_viewport: 'Fit Viewport',
            ai_assistant: 'AI Assistant',
            xml: 'XML',
            chat_placeholder: 'Your request...',
            chat_send: 'Send',
            xml_edit_label: 'Source Editing',
            apply: 'Apply',
            hint_text: 'Describe your subject area. Or upload your XML code to start editing.',
            status_online: 'Online',
            notification_hint: 'Tip: Upload your XML in the XML panel. Use this to render XML from a third-party LLM.',
            error_unavailable: 'Sorry, the AI service is unavailable. Try again later.',
            error_ai_unavailable: 'AI service is not responding. Use the XML panel and a third-party LLM.',
            error_generic: 'Sorry, an error occurred. Try again later.',
            request_in_progress: 'A request is already in progress. Please wait.',
            success: 'Done!',
        }
    };

    var STORAGE_KEY = 'vibe-bpmn-lang';

    function detectLang() {
        var stored = localStorage.getItem(STORAGE_KEY);
        if (stored) return stored;
        return (navigator.language || '').slice(0, 2) === 'en' ? 'en' : 'ru';
    }

    window.I18N = {
        currentLang: 'ru',
        translations: TRANSLATIONS,

        init: function () {
            this.currentLang = detectLang();
        },

        t: function (key) {
            var lang = TRANSLATIONS[this.currentLang];
            return lang && lang[key] !== undefined ? lang[key] : key;
        },

        switchLang: function () {
            this.currentLang = this.currentLang === 'ru' ? 'en' : 'ru';
            localStorage.setItem(STORAGE_KEY, this.currentLang);
            document.documentElement.lang = this.currentLang;
            this.translatePage();
            window.dispatchEvent(new CustomEvent('languagechange', {
                detail: { lang: this.currentLang }
            }));
        },

        translatePage: function () {
            document.querySelectorAll('[data-i18n]').forEach(function (el) {
                var key = el.getAttribute('data-i18n');
                el.textContent = window.I18N.t(key);
            });
            document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
                var key = el.getAttribute('data-i18n-placeholder');
                el.placeholder = window.I18N.t(key);
            });
            document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
                var key = el.getAttribute('data-i18n-title');
                el.title = window.I18N.t(key);
            });
        }
    };

    window.I18N.init();
})();
