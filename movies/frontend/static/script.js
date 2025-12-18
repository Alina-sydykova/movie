// // Функция инициализации карусели
// function initCarousel(trackId, prevBtnId, nextBtnId, cardClass, slidesPerView) {
//     const track = document.getElementById(trackId);
//     const prevButton = document.getElementById(prevBtnId);
//     const nextButton = document.getElementById(nextBtnId);

//     // Если элементы не найдены, выходим, чтобы не было ошибок
//     if (!track || !prevButton || !nextButton) {
//         // console.warn(`Карусель с ID ${trackId} не найдена или неполная.`);
//         return;
//     }

//     // Находим карточки внутри конкретной дорожки
//     // Используем querySelectorAll, который найдет элементы с указанным классом внутри track
//     const slides = track.querySelectorAll(`.${cardClass}`);
//     const totalSlides = slides.length;
//     let currentIndex = 0;

//     // Функция обновления кнопок
//     const updateNavButtons = () => {
//         prevButton.disabled = currentIndex === 0;

//         // Блокируем кнопку "вперед", если достигли конца
//         if (currentIndex >= totalSlides - slidesPerView) {
//             nextButton.disabled = true;
//         } else {
//             nextButton.disabled = false;
//         }
//     };

//     // Функция движения
//     const moveCarousel = () => {
//         // Вычисляем процент сдвига (100% / кол-во видимых)
//         const offsetPercentagePerSlide = 100 / slidesPerView;
//         const percentageOffset = -(currentIndex * offsetPercentagePerSlide);
//         track.style.transform = `translateX(${percentageOffset}%)`;
//         updateNavButtons();
//     };

//     // События клика
//     nextButton.addEventListener('click', () => {
//         if (currentIndex < totalSlides - slidesPerView) {
//             currentIndex++;
//             moveCarousel();
//         }
//     });

//     prevButton.addEventListener('click', () => {
//         if (currentIndex > 0) {
//             currentIndex--;
//             moveCarousel();
//         }
//     });

//     // Запуск при старте
//     updateNavButtons();
// }

// // Запускаем 4 независимые карусели после загрузки страницы
// document.addEventListener('DOMContentLoaded', () => {

//     // 1. Сейчас смотрят (4 карточки в ряд)
//     initCarousel('carouselTrack_now', 'prevButton_now', 'nextButton_now', 'movie-card', 4);

//     // 2. Жанры (4 карточки в ряд)
//     initCarousel('carouselTrack_genre', 'prevButton_genre', 'nextButton_genre', 'movie-card', 4);

//     // 3. СКОРО (2.5 карточки в ряд, так как они шире)
//     initCarousel('carouselTrack_soon', 'prevButton_soon', 'nextButton_soon', 'movie-card', 2.5);

//     // 4. Кинокидс (4 карточки в ряд)
//     initCarousel('carouselTrack_kids', 'prevButton_kids', 'nextButton_kids', 'movie-card', 4);

// });


function initCarousel(trackId, prevBtnId, nextBtnId, cardClass, slidesPerView) {
  const track = document.getElementById(trackId);
  const prevButton = document.getElementById(prevBtnId);
  const nextButton = document.getElementById(nextBtnId);

  if (!track || !prevButton || !nextButton) return;

  const slides = Array.from(track.querySelectorAll(`.${cardClass}`));
  if (!slides.length) return;

  const viewport = track.closest(".carousel-viewport");
  let currentIndex = 0;

  const getStepPx = () => {
    const slide = slides[0];
    const styles = window.getComputedStyle(slide);
    const marginL = parseFloat(styles.marginLeft) || 0;
    const marginR = parseFloat(styles.marginRight) || 0;
    return slide.getBoundingClientRect().width + marginL + marginR;
  };

  const getVisibleCount = () => {
    if (slidesPerView) return Math.max(1, Math.ceil(slidesPerView));
    if (!viewport) return 1;
    const step = getStepPx() || 1;
    const w = viewport.getBoundingClientRect().width || step;
    return Math.max(1, Math.floor(w / step));
  };

  const maxIndex = () => Math.max(0, slides.length - getVisibleCount());

  const updateButtons = () => {
    prevButton.disabled = currentIndex <= 0;
    nextButton.disabled = currentIndex >= maxIndex();
  };

  const move = (behavior = "smooth") => {
    const step = getStepPx();
    const max = maxIndex();
    if (currentIndex > max) currentIndex = max;
    if (currentIndex < 0) currentIndex = 0;

    const offset = currentIndex * step;
    track.style.transition = behavior === "smooth" ? "" : "none";
    track.style.transform = `translateX(${-offset}px)`;
    if (behavior !== "smooth") requestAnimationFrame(() => (track.style.transition = ""));

    updateButtons();
  };

  nextButton.addEventListener("click", () => {
    if (currentIndex < maxIndex()) {
      currentIndex += 1;
      move();
    }
  });

  prevButton.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex -= 1;
      move();
    }
  });

  window.addEventListener("resize", () => move("instant"));

  move("instant");
}

document.addEventListener("DOMContentLoaded", () => {
  initCarousel("carouselTrack_now", "prevButton_now", "nextButton_now", "movie-card", 4);
  initCarousel("carouselTrack_genre", "prevButton_genre", "nextButton_genre", "movie-card", 4);
  initCarousel("carouselTrack_soon", "prevButton_soon", "nextButton_soon", "movie-card", 2.5);
  initCarousel("carouselTrack_kids", "prevButton_kids", "nextButton_kids", "movie-card", 4);
  initCarousel("carouselTrack_favorites", "prevButton_favorites", "nextButton_favorites", "movie-card", 4);
  initCarousel("carouselTrack_watchlater", "prevButton_watchlater", "nextButton_watchlater", "movie-card", 4);
  initCarousel("carouselTrack_family", "prevButton_family", "nextButton_family", "movie-card", 4);
});

