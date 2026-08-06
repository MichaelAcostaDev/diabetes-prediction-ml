const languageSelector = document.getElementById("language");
const predictButton = document.getElementById("predictButton");
const resetButton = document.getElementById("resetButton");
const resultPanel = document.getElementById("resultPanel");
const resultLabel = document.getElementById("resultLabel");
const resultConfidence = document.getElementById("resultConfidence");
const resultExplanation = document.getElementById("resultExplanation");
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");

function setLanguage(lang) {
    window.location.search = `?lang=${lang}`;
}

function getFieldValues() {
    const formData = {};
    document.querySelectorAll(".field-block input").forEach((input) => {
        formData[input.name] = input.value.trim();
    });
    return formData;
}

function resetErrors() {
    document.querySelectorAll(".field-error").forEach((errorElement) => {
        errorElement.textContent = "";
    });
}

function showProgress() {
    progressBar.hidden = false;
    progressFill.style.width = "0%";
    setTimeout(() => {
        progressFill.style.width = "44%";
    }, 50);
    setTimeout(() => {
        progressFill.style.width = "88%";
    }, 450);
}

function hideProgress() {
    progressFill.style.width = "100%";
    setTimeout(() => {
        progressBar.hidden = true;
        progressFill.style.width = "0%";
    }, 350);
}

function renderResult(data) {
    resultLabel.textContent = data.prediction_label;
    resultConfidence.textContent = `${data.probability_text}: ${data.confidence}%`;
    resultExplanation.textContent = data.explanation;
    resultPanel.hidden = false;
}

function renderErrors(errors) {
    resetErrors();
    Object.keys(errors).forEach((field) => {
        const element = document.querySelector(`[data-field-error-for="${field}"]`);
        if (element) {
            element.textContent = errors[field];
        }
    });
}

predictButton.addEventListener("click", async () => {
    const lang = languageSelector.value;
    const formData = getFieldValues();
    resetErrors();
    resultPanel.hidden = true;
    showProgress();

    const payload = { data: formData, lang };
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (!response.ok) {
            const errors = result.errors || {};
            renderErrors(errors);
        } else {
            renderResult(result);
        }
    } catch (error) {
        resultLabel.textContent = "Request failed. Please try again.";
        resultPanel.hidden = false;
    } finally {
        hideProgress();
    }
});

resetButton.addEventListener("click", () => {
    document.querySelectorAll(".field-block input").forEach((input) => {
        input.value = "";
    });
    resultPanel.hidden = true;
    resetErrors();
});

languageSelector.addEventListener("change", () => {
    setLanguage(languageSelector.value);
});
