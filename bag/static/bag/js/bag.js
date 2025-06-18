document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit-weight-form").forEach(form => {
        const select = form.querySelector(".weight-select");
        const updateBtn = form.querySelector(".update-button");
        const deleteBtn = form.querySelector(".delete-button");
        const original = select.dataset.originalWeight;

        select.addEventListener("change", () => {
            const changed = select.value !== original;

            if (changed) {
                updateBtn.classList.add("show");
                deleteBtn.classList.add("hidden");
                updateBtn.disabled = false;
            } else {
                updateBtn.classList.remove("show");
                deleteBtn.classList.remove("hidden");
                updateBtn.disabled = true;
            }
        });
    });
});
