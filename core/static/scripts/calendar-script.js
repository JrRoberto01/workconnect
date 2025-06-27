const calendarGrid = document.getElementById("calendar-grid");
const monthYearLabel = document.getElementById("month-year");

let today = new Date();
let currentMonth = today.getMonth(); // 0 = janeiro
let currentYear = today.getFullYear();

function processEventDates(dates) {
  const eventsByMonth = {};

  dates.forEach(dateString => {
    const date = new Date(dateString + 'T00:00:00');
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    const key = `${year}-${String(month).padStart(2, '0')}`;

    if (!eventsByMonth[key]) {
      eventsByMonth[key] = [];
    }

    if (!eventsByMonth[key].includes(day)) {
      eventsByMonth[key].push(day);
    }
  });

  return eventsByMonth;
}

const selectedDays = processEventDates(window.eventDates || []);

function getDaysInMonth(month, year) {
  return new Date(year, month + 1, 0).getDate();
}

function formatMonthYear(month, year) {
  const meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];
  return `${meses[month]} de ${year}`;
}

function createCalendar(month, year) {
  calendarGrid.innerHTML = "";
  const diasNoMes = getDaysInMonth(month, year);
  const hoje = new Date();

  monthYearLabel.textContent = formatMonthYear(month, year);

  const key = `${year}-${String(month + 1).padStart(2, '0')}`;
  const diasSelecionados = selectedDays[key] || [];

  for (let dia = 1; dia <= diasNoMes; dia++) {
    const cell = document.createElement("div");
    cell.classList.add("calendar-day");

    if (
      dia === hoje.getDate() &&
      month === hoje.getMonth() &&
      year === hoje.getFullYear()
    ) {
      cell.classList.add("current-day");
    }

    if (diasSelecionados.includes(dia)) {
      cell.classList.add("selected-day");
    }

    cell.textContent = dia;
    calendarGrid.appendChild(cell);
  }
}

function changeMonth(offset) {
  currentMonth += offset;

  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  } else if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }

  createCalendar(currentMonth, currentYear);
}

// Inicialização
createCalendar(currentMonth, currentYear);
