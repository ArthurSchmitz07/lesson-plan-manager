const API_URL = "http://localhost:5000";

const form = document.getElementById("lesson-plan-form");
const formMessage = document.getElementById("form-message");
const lessonList = document.getElementById("lesson-list");

const lessonIdInput = document.getElementById("lesson-id");
const titleInput = document.getElementById("title");
const objectiveInput = document.getElementById("objective");
const summaryInput = document.getElementById("summary");
const plannedDateInput = document.getElementById("planned_date");
const disciplineInput = document.getElementById("discipline");
const contentsInput = document.getElementById("contents");
const supportResourcesInput = document.getElementById("support_resources");
const tagsInput = document.getElementById("tags");

const smartAssistButton = document.getElementById("smart-assist-button");
const clearFormButton = document.getElementById("clear-form-button");
const filterButton = document.getElementById("filter-button");

const searchInput = document.getElementById("search");
const filterDisciplineInput = document.getElementById("filter-discipline");
const filterTagInput = document.getElementById("filter-tag");
const filterDateInput = document.getElementById("filter-date");
const sortByInput = document.getElementById("sort-by");

function showMessage(message, type = "success") {
  formMessage.textContent = message;
  formMessage.className = `message ${type}`;
}

function clearForm() {
  lessonIdInput.value = "";
  form.reset();
  showMessage("");
}

function getFormData() {
  return {
    title: titleInput.value,
    objective: objectiveInput.value,
    summary: summaryInput.value,
    planned_date: plannedDateInput.value,
    discipline: disciplineInput.value,
    contents: contentsInput.value,
    support_resources: supportResourcesInput.value,
    tags: tagsInput.value,
  };
}

async function loadLessonPlans() {
  const params = new URLSearchParams();

  if (searchInput.value) {
    params.append("search", searchInput.value);
  }

  if (filterDisciplineInput.value) {
    params.append("discipline", filterDisciplineInput.value);
  }

  if (filterTagInput.value) {
    params.append("tag", filterTagInput.value);
  }

  if (filterDateInput.value) {
    params.append("planned_date", filterDateInput.value);
  }

  params.append("sort_by", sortByInput.value);
  params.append("page", "1");
  params.append("limit", "10");

  const response = await fetch(`${API_URL}/lesson-plans?${params.toString()}`);
  const data = await response.json();

  lessonList.innerHTML = "";

  if (!data.items || data.items.length === 0) {
    lessonList.innerHTML = "<p>Nenhum plano de aula encontrado.</p>";
    return;
  }

  data.items.forEach((lesson) => {
    const card = document.createElement("article");
    card.className = "lesson-card";

    card.innerHTML = `
      <h3>${lesson.title}</h3>
      <p><strong>Disciplina:</strong> ${lesson.discipline}</p>
      <p><strong>Data prevista:</strong> ${lesson.planned_date}</p>
      <p><strong>Objetivo:</strong> ${lesson.objective}</p>
      <p><strong>Resumo:</strong> ${lesson.summary}</p>
      <p><strong>Conteúdos:</strong> ${lesson.contents || "-"}</p>
      <p><strong>Recursos:</strong> ${lesson.support_resources || "-"}</p>
      <p><strong>Tags:</strong> ${lesson.tags || "-"}</p>

      <div class="lesson-actions">
        <button data-testid="edit-lesson-${lesson.id}" onclick="editLesson(${lesson.id})">
          Editar
        </button>
        <button class="danger" data-testid="delete-lesson-${lesson.id}" onclick="deleteLesson(${lesson.id})">
          Excluir
        </button>
      </div>
    `;

    lessonList.appendChild(card);
  });
}

async function saveLessonPlan(event) {
  event.preventDefault();

  const lessonId = lessonIdInput.value;
  const formData = getFormData();

  const url = lessonId
    ? `${API_URL}/lesson-plans/${lessonId}`
    : `${API_URL}/lesson-plans`;

  const method = lessonId ? "PUT" : "POST";

  const response = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  if (!response.ok) {
    showMessage(data.error || "Erro ao salvar plano de aula.", "error");
    return;
  }

  showMessage(data.message || "Plano salvo com sucesso.", "success");
  clearForm();
  loadLessonPlans();
}

async function editLesson(id) {
  const response = await fetch(`${API_URL}/lesson-plans/${id}`);
  const lesson = await response.json();

  lessonIdInput.value = lesson.id;
  titleInput.value = lesson.title;
  objectiveInput.value = lesson.objective;
  summaryInput.value = lesson.summary;
  plannedDateInput.value = lesson.planned_date;
  disciplineInput.value = lesson.discipline;
  contentsInput.value = lesson.contents || "";
  supportResourcesInput.value = lesson.support_resources || "";
  tagsInput.value = lesson.tags || "";

  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function deleteLesson(id) {
  const confirmDelete = confirm("Deseja realmente excluir este plano de aula?");

  if (!confirmDelete) {
    return;
  }

  const response = await fetch(`${API_URL}/lesson-plans/${id}`, {
    method: "DELETE",
  });

  const data = await response.json();

  if (!response.ok) {
    showMessage(data.error || "Erro ao excluir plano de aula.", "error");
    return;
  }

  showMessage(data.message || "Plano excluído com sucesso.", "success");
  loadLessonPlans();
}

async function generateRecommendations() {
  if (!titleInput.value || !disciplineInput.value || !summaryInput.value) {
    showMessage(
      "Preencha título, disciplina e ementa/resumo antes de usar a IA.",
      "error"
    );
    return;
  }

  smartAssistButton.disabled = true;
  smartAssistButton.textContent = "Gerando recomendações...";

  try {
    const response = await fetch(`${API_URL}/smart-assist`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: titleInput.value,
        discipline: disciplineInput.value,
        summary: summaryInput.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage(data.error || "Erro ao gerar recomendações.", "error");
      return;
    }

    const recommendations = data.recommendations;

    contentsInput.value = recommendations.contents.join(", ");
    supportResourcesInput.value = recommendations.support_resources.join(", ");
    tagsInput.value = recommendations.recommended_tags.join(", ");

    showMessage("Recomendações geradas com sucesso.", "success");
  } catch (error) {
    showMessage("Não foi possível conectar com a API de IA.", "error");
  } finally {
    smartAssistButton.disabled = false;
    smartAssistButton.textContent = "Gerar Recomendações com IA";
  }
}

form.addEventListener("submit", saveLessonPlan);
smartAssistButton.addEventListener("click", generateRecommendations);
clearFormButton.addEventListener("click", clearForm);
filterButton.addEventListener("click", loadLessonPlans);

loadLessonPlans();
