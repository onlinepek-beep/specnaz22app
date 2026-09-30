const navigationItems = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");
const themeButton = document.querySelector(".theme-button");

const roleNames = {
    admin: "Администратор",
    manager: "Руководитель",
    operator: "Оператор"
};

function setTheme(theme) {
    document.documentElement.dataset.theme = theme === "light" ? "light" : "dark";
    localStorage.setItem("specnaz22-theme", theme);
    if (themeButton) themeButton.textContent = theme === "light" ? "☾" : "☀";
}

function openPage(pageId) {
    navigationItems.forEach(item => item.classList.toggle("active", item.dataset.page === pageId));
    pages.forEach(page => page.classList.toggle("active", page.id === "page-" + pageId));
}

navigationItems.forEach(item => item.addEventListener("click", () => openPage(item.dataset.page)));

if (themeButton) {
    themeButton.addEventListener("click", () => {
        const current = document.documentElement.dataset.theme || "dark";
        setTheme(current === "dark" ? "light" : "dark");
    });
}

function applyPermissions(role, permissions) {
    navigationItems.forEach(item => {
        item.hidden = !permissions.includes(item.dataset.page);
    });

    const active = [...navigationItems].find(item => !item.hidden && item.classList.contains("active"));
    if (!active) {
        const first = [...navigationItems].find(item => !item.hidden);
        if (first) openPage(first.dataset.page);
    }

    const profileName = document.querySelector(".profile-name");
    const profileRole = document.querySelector(".profile-role");

    if (profileRole) profileRole.textContent = roleNames[role] || "Пользователь";
    if (profileName) profileName.textContent = "Пользователь";
}

async function loadCurrentUser() {
    try {
        const response = await fetch("/api/me");
        if (!response.ok) {
            window.location.href = "/";
            return;
        }

        const user = await response.json();

        if (!user.authenticated) {
            window.location.href = "/";
            return;
        }

        const profileName = document.querySelector(".profile-name");
        if (profileName) profileName.textContent = user.name || "Пользователь";

        applyPermissions(user.role, user.permissions || []);
    } catch (error) {
        console.error("Ошибка загрузки пользователя:", error);
        window.location.href = "/";
    }
}

setTheme(localStorage.getItem("specnaz22-theme") || "dark");
loadCurrentUser();
