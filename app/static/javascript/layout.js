const mobileToggleBtn = document.querySelector("#mobile-toggle-nav-btn")
const navbar = document.querySelector("#navbar")

let count = 0


mobileToggleBtn.addEventListener("click", () => {
    if (count == 1) {
        navbar.classList.add("navbar")
        mobileToggleBtn.innerHTML = "="
        count = 0
    } else if (count == 0) {
        navbar.classList.remove("navbar")
        mobileToggleBtn.innerHTML = "X"
        count = 1
    }
})