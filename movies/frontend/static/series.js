// series.js (fixed)

document.addEventListener("DOMContentLoaded", () => {
  // 1) Все кнопки эпизодов
  const episodeButtons = document.querySelectorAll(".episode-btn");
  // 2) Заголовок над плеером
  const sectionTitle = document.querySelector(".section-title");
  const player = document.getElementById("episodePlayer");
  const source = document.getElementById("episodeSource");
  const defaultSrc = player ? player.dataset.defaultSrc : "";

  // Если на странице нет эпизодов — спокойно выходим (это не ошибка)
  if (!episodeButtons.length || !sectionTitle) return;

  // Обновление заголовка
  const setTitle = (btn) => {
    const seasonNumber = btn.dataset.season || btn.getAttribute("data-season") || "";
    const episodeNumber = btn.dataset.episode || btn.getAttribute("data-episode") || "";

    // fallback, если атрибуты не заданы
    if (!seasonNumber && !episodeNumber) {
      sectionTitle.textContent = "ВЫБЕРИТЕ СЕРИЮ";
      return;
    }

    sectionTitle.textContent = `${seasonNumber} СЕЗОН ${episodeNumber} СЕРИЯ`;
  };

  // Снять active со всех, поставить на одну
  const setActive = (btn) => {
    episodeButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
  };

  const setVideo = (btn) => {
    if (!player || !source) return;
    const src = btn.dataset.src || defaultSrc;
    if (!src) return;
    source.src = src;
    player.load();
    player.play().catch(() => {});
  };

  // Обработчик клика (делегирование — надежнее)
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".episode-btn");
    if (!btn) return;

    // если кликнули по кнопке-эпизоду
    setActive(btn);
    setTitle(btn);
    setVideo(btn);

    // тут можно подгружать видео/серии если будет логика
    // console.log(`Выбрана серия: Сезон ${btn.dataset.season}, Эпизод ${btn.dataset.episode}`);
  });

  // Автовыбор первой кнопки (или той, что уже active)
  const initial = document.querySelector(".episode-btn.active") || episodeButtons[0];
  if (initial) {
    setActive(initial);
    setTitle(initial);
    setVideo(initial);
  }
});
