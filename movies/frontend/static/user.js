document.addEventListener("DOMContentLoaded", () => {
  // =========================
  // 1) ЛЕВОЕ МЕНЮ (sidebar)
  // =========================
  const sidebarButtons = document.querySelectorAll(".profile-sidebar .nav-button");
  if (sidebarButtons.length > 0) {
    sidebarButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        if (!targetId) return;

        // Активная кнопка
        sidebarButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        // --- Вариант А: старая разметка ---
        // .content-wrapper .profile-content  + классы hidden-content / active-content
        const oldBlocks = document.querySelectorAll(".content-wrapper .profile-content");
        if (oldBlocks.length > 0) {
          oldBlocks.forEach((block) => {
            block.classList.add("hidden-content");
            block.classList.remove("active-content");
            block.style.display = ""; // сброс, чтобы не залипало
          });

          const targetBlock = document.getElementById(targetId);
          if (targetBlock) {
            targetBlock.classList.remove("hidden-content");
            targetBlock.classList.add("active-content");

            // Если у профиля должен быть flex
            if (targetId === "profile-content-block") {
              targetBlock.style.display = "flex";
            }
          }
          return; // если нашли oldBlocks — дальше не идём
        }

        // --- Вариант B: новая разметка ---
        // .main-content-wrapper .content-block + классы hidden-block / active-block
        const newBlocks = document.querySelectorAll(".main-content-wrapper .content-block");
        if (newBlocks.length > 0) {
          newBlocks.forEach((block) => {
            block.classList.add("hidden-block");
            block.classList.remove("active-block");
          });

          const targetBlock = document.getElementById(targetId);
          if (targetBlock) {
            targetBlock.classList.remove("hidden-block");
            targetBlock.classList.add("active-block");
          }
        }
      });
    });
  }

  // =========================
  // 2) ПОДМЕНЮ (avatar section)
  // =========================
  const subNavButtons = document.querySelectorAll(".profile-sub-nav .sub-nav-button");
  const subBlocks = document.querySelectorAll(".sub-content-wrapper .sub-content-block");

  // если подменю/блоков нет — просто ничего не делаем (без ошибок)
  if (subNavButtons.length > 0 && subBlocks.length > 0) {
    subNavButtons.forEach((button) => {
      // "Выйти" не переключает контент
      if (button.classList.contains("logout-button")) return;

      button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-sub-target");
        if (!targetId) return;

        // Активная кнопка подменю
        subNavButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        // Скрываем все подблоки
        subBlocks.forEach((block) => {
          block.classList.add("hidden-sub-block");
          block.classList.remove("active-sub-block");
        });

        // Показываем нужный
        const targetBlock = document.getElementById(targetId);
        if (targetBlock) {
          targetBlock.classList.remove("hidden-sub-block");
          targetBlock.classList.add("active-sub-block");
        }
      });
    });
  }

  // =========================
  // 3) ПОЛ В ПРОФИЛЕ
  // =========================
  const genderButtons = document.querySelectorAll(".gender-button");
  if (genderButtons.length > 0) {
    genderButtons.forEach((button) => {
      button.addEventListener("click", () => {
        genderButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");
        const input = button.querySelector("input[type='radio']");
        if (input) input.checked = true;
      });
    });
  }

  // =========================
  // 4) АВАТАР (preview)
  // =========================
  const avatarInput = document.getElementById("avatarInput");
  const avatarPreview = document.getElementById("avatarPreview");
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener("change", () => {
      const file = avatarInput.files && avatarInput.files[0];
      if (!file) return;
      const url = URL.createObjectURL(file);
      avatarPreview.src = url;
    });
  }
});
