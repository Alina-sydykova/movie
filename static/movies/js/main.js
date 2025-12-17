// Функция инициализации карусели
function initCarousel(trackId, prevBtnId, nextBtnId, cardClass, slidesPerView) {
    const track = document.getElementById(trackId);
    const prevButton = document.getElementById(prevBtnId);
    const nextButton = document.getElementById(nextBtnId);

    if (!track || !prevButton || !nextButton) {
        return;
    }

    const slides = track.querySelectorAll(`.${cardClass}`);
    const totalSlides = slides.length;
    let currentIndex = 0;

    const updateNavButtons = () => {
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex >= totalSlides - slidesPerView;
    };

    const moveCarousel = () => {
        const offsetPercentagePerSlide = 100 / slidesPerView;
        const percentageOffset = -(currentIndex * offsetPercentagePerSlide);
        track.style.transform = `translateX(${percentageOffset}%)`;
        updateNavButtons();
    };

    nextButton.addEventListener('click', () => {
        if (currentIndex < totalSlides - slidesPerView) {
            currentIndex++;
            moveCarousel();
        }
    });

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            moveCarousel();
        }
    });

    updateNavButtons();
}

// Функция инициализации карусели (предполагаем, что она определена выше)
// function initCarousel(...) { ... }

document.addEventListener('DOMContentLoaded', () => {
    // Инициализация каруселей
    // 1. Сейчас смотрят (4 карточки в ряд)
    initCarousel('carouselTrack_now', 'prevButton_now', 'nextButton_now', 'movie-card', 4);

    // 2. Жанры (4 карточки)
    initCarousel('carouselTrack_genre', 'prevButton_genre', 'nextButton_genre', 'movie-card', 4);

    // 3. Скоро (2.5 карточки)
    initCarousel('carouselTrack_soon', 'prevButton_soon', 'nextButton_soon', 'movie-card', 2.5);

    // 4. Kids (4 карточки)
    initCarousel('carouselTrack_kids', 'prevButton_kids', 'nextButton_kids', 'movie-card', 4);


    // Кнопка-лупа -> показать/спрятать строку поиска в шапке (ИСПРАВЛЕННЫЙ БЛОК)
    const searchBox = document.querySelector(".search-box");
    const searchForm = document.getElementById("search-form");

    function toggleSearch() {
        // Проверьте, что класс 'header-search--open' корректно отображает форму
        searchForm.classList.toggle("header-search--open"); 
        
        const input = searchForm.querySelector("input[name='q']");
        
        if (searchForm.classList.contains("header-search--open") && input) {
            input.focus();
        }
    }

    if (searchBox) {
        // Мы уже внутри DOMContentLoaded, просто навешиваем обработчик клика
        searchBox.addEventListener("click", toggleSearch); 
    }
});
