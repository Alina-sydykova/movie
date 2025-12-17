
// main.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const container = document.getElementById("movies-container");

  if (!form || !input || !container) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) {
      container.innerHTML = "<p>Введите название фильма.</p>";
      return;
    }

    searchMovies(query);
  });
});

// запрос к /api/movies/search/?q=...
function searchMovies(query) {
  const container = document.getElementById("movies-container");
  container.innerHTML = "<p>Ищем...</p>";

  fetch(`/api/movies/search/?q=${encodeURIComponent(query)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка запроса");
      }
      return response.json();
    })
    .then((data) => {
      renderMovies(data);
    })
    .catch((err) => {
      console.error(err);
      container.innerHTML = "<p>Что-то пошло не так при поиске.</p>";
    });
}

// отрисовка карточек
function renderMovies(movies) {
  const container = document.getElementById("movies-container");

  if (!movies || movies.length === 0) {
    container.innerHTML = "<p>Ничего не найдено.</p>";
    return;
  }

  const html = movies
    .map((m) => {
      const poster = m.poster_url && m.poster_url !== "N/A"
        ? `<img src="${m.poster_url}" alt="${m.title}" class="movie-poster">`
        : `<div class="movie-poster placeholder">No image</div>`;

      return `
        <div class="movie-card" data-imdb-id="${m.imdb_id}">
          ${poster}
          <h3>${m.title}</h3>
          <p>${m.year || ""}</p>
          <div class="movie-actions">
            <a href="/movie/${m.imdb_id}/">Подробнее</a>
            <button type="button" class="btn-fav"
              data-imdb-id="${m.imdb_id}"
              data-title="${m.title}"
              data-year="${m.year || ""}"
              data-poster="${m.poster_url || ""}">
              В избранное
            </button>
          </div>
        </div>
      `;
    })
    .join("");

  container.innerHTML = html;

  // повесим обработчики на кнопки "В избранное"
  document.querySelectorAll(".btn-fav").forEach((btn) => {
    btn.addEventListener("click", () => {
      const movie = {
        imdb_id: btn.dataset.imdbId,
        title: btn.dataset.title,
        year: btn.dataset.year,
        poster_url: btn.dataset.poster,
      };
      addToFavorites(movie);
    });
  });
}




function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // cookie начинается с "name="
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");




function addToFavorites(movie) {
  fetch("/api/favorites/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(movie),
  })
    .then((response) => {
      if (response.status === 403) {
        alert("Нужно войти в аккаунт, чтобы добавлять в избранное.");
        window.location.href = "/accounts/login/?next=/";
        return null;
      }
      if (!response.ok) {
        throw new Error("Ошибка при добавлении в избранное");
      }
      return response.json();
    })
    .then((data) => {
      if (!data) return;
      console.log("Добавлено в избранное:", data);
      alert(`Фильм "${data.title}" добавлен в избранное.`);
    })
    .catch((err) => {
      console.error(err);
      alert("Не удалось добавить в избранное.");
    });
}
