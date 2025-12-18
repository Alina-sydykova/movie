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
  if (!viewport) return;

  // На всякий случай сбрасываем старые transform-сдвиги, если они остались от прошлой логики
  track.style.transform = "";

  const getStepPx = () => {
    const slide = slides[0];
    const styles = window.getComputedStyle(slide);
    const marginL = parseFloat(styles.marginLeft) || 0;
    const marginR = parseFloat(styles.marginRight) || 0;
    const trackStyles = window.getComputedStyle(track);
    const gap =
      parseFloat(trackStyles.columnGap) ||
      parseFloat(trackStyles.gap) ||
      parseFloat(trackStyles.rowGap) ||
      0;
    return slide.getBoundingClientRect().width + marginL + marginR + gap;
  };

  const maxScrollLeft = () => Math.max(0, viewport.scrollWidth - viewport.clientWidth);

  const updateButtons = () => {
    const x = viewport.scrollLeft;
    const max = maxScrollLeft();
    prevButton.disabled = x <= 0;
    nextButton.disabled = x >= max - 1;
  };

  const scrollToLeft = (left, behavior = "smooth") => {
    const max = maxScrollLeft();
    const clamped = Math.max(0, Math.min(left, max));
    if (typeof viewport.scrollTo === "function") {
      try {
        viewport.scrollTo({ left: clamped, behavior });
        return;
      } catch (_) {
        // fallthrough
      }
    }
    viewport.scrollLeft = clamped;
  };

  const scrollByStep = (direction) => {
    const step = getStepPx();
    const fallback = Math.max(1, Math.floor(viewport.clientWidth * 0.9));
    const delta = (step && Number.isFinite(step) ? step : fallback) * direction;
    scrollToLeft(viewport.scrollLeft + delta, "smooth");
  };

  nextButton.addEventListener("click", (e) => {
    e.preventDefault();
    scrollByStep(1);
  });

  prevButton.addEventListener("click", (e) => {
    e.preventDefault();
    scrollByStep(-1);
  });

  // UX fallback/enhancement:
  // - Scroll with mouse wheel (vertical wheel -> horizontal)
  // - Drag with mouse/touch
  viewport.addEventListener(
    "wheel",
    (e) => {
      // If user already scrolls horizontally (trackpad), don't interfere
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (maxScrollLeft() <= 0) return;

      scrollToLeft(viewport.scrollLeft + e.deltaY, "auto");
      e.preventDefault();
    },
    { passive: false }
  );

  const DRAG_THRESHOLD_PX = 5;
  let isPointerDown = false;
  let startX = 0;
  let startScrollLeft = 0;
  let suppressClick = false;

  const endDrag = (pointerId) => {
    if (!isPointerDown) return;
    isPointerDown = false;
    viewport.classList.remove("is-dragging");
    if (typeof pointerId === "number" && viewport.releasePointerCapture) {
      try {
        viewport.releasePointerCapture(pointerId);
      } catch (_) {}
    }
    updateButtons();
    if (suppressClick) {
      setTimeout(() => {
        suppressClick = false;
      }, 0);
    }
  };

  viewport.addEventListener("pointerdown", (e) => {
    if (e.pointerType === "mouse" && e.button !== 0) return;
    isPointerDown = true;
    suppressClick = false;
    startX = e.clientX;
    startScrollLeft = viewport.scrollLeft;
    viewport.classList.add("is-dragging");
    if (viewport.setPointerCapture) {
      try {
        viewport.setPointerCapture(e.pointerId);
      } catch (_) {}
    }
  });

  viewport.addEventListener("pointermove", (e) => {
    if (!isPointerDown) return;
    const dx = e.clientX - startX;
    if (Math.abs(dx) > DRAG_THRESHOLD_PX) suppressClick = true;
    viewport.scrollLeft = startScrollLeft - dx;
  });

  viewport.addEventListener("pointerup", (e) => endDrag(e.pointerId));
  viewport.addEventListener("pointercancel", (e) => endDrag(e.pointerId));

  // Prevent accidental navigation when a drag just happened
  viewport.addEventListener(
    "click",
    (e) => {
      if (!suppressClick) return;
      e.preventDefault();
      e.stopPropagation();
    },
    true
  );

  viewport.addEventListener("scroll", updateButtons, { passive: true });
  window.addEventListener("resize", updateButtons);
  window.addEventListener("load", updateButtons);

  // Инициализация
  updateButtons();
  requestAnimationFrame(updateButtons);
  setTimeout(updateButtons, 250);
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

