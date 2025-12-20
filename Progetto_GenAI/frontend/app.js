/**
 * Trivia Quiz - Client Application
 */

const API_BASE = '/api';

// ==========================================
// State Management
// ==========================================

const state = {
    user: null,
    quiz: {
        questions: [],
        currentIndex: 0,
        answers: [],
        startTime: null,
        timerInterval: null
    }
};

// ==========================================
// DOM Elements
// ==========================================

const screens = {
    login: document.getElementById('login-screen'),
    home: document.getElementById('home-screen'),
    quiz: document.getElementById('quiz-screen'),
    result: document.getElementById('result-screen')
};

const elements = {
    // Login
    loginForm: document.getElementById('login-form'),
    usernameInput: document.getElementById('username-input'),
    loginError: document.getElementById('login-error'),

    // Home
    displayUsername: document.getElementById('display-username'),
    logoutBtn: document.getElementById('logout-btn'),
    startQuizBtn: document.getElementById('start-quiz-btn'),
    statGames: document.getElementById('stat-games'),
    statAvg: document.getElementById('stat-avg'),
    statBest: document.getElementById('stat-best'),
    historyList: document.getElementById('history-list'),

    // Quiz
    questionCounter: document.getElementById('question-counter'),
    progressFill: document.getElementById('progress-fill'),
    timerValue: document.getElementById('timer-value'),
    questionCategory: document.getElementById('question-category'),
    questionText: document.getElementById('question-text'),
    optionsContainer: document.getElementById('options-container'),
    nextBtn: document.getElementById('next-btn'),

    // Result
    resultIcon: document.getElementById('result-icon'),
    resultTitle: document.getElementById('result-title'),
    resultSubtitle: document.getElementById('result-subtitle'),
    resultScore: document.getElementById('result-score'),
    resultCorrect: document.getElementById('result-correct'),
    resultTime: document.getElementById('result-time'),
    playAgainBtn: document.getElementById('play-again-btn'),
    backHomeBtn: document.getElementById('back-home-btn')
};

// ==========================================
// Utilities
// ==========================================

function showScreen(screenName) {
    Object.values(screens).forEach(s => s.classList.remove('active'));
    screens[screenName].classList.add('active');
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'API request failed');
    }

    return data;
}

// ==========================================
// Auth Functions
// ==========================================

async function handleLogin(e) {
    e.preventDefault();
    const username = elements.usernameInput.value.trim();

    if (username.length < 2) {
        elements.loginError.textContent = 'Username must be at least 2 characters';
        return;
    }

    elements.loginError.textContent = '';

    try {
        // Try to get existing user
        let user;
        try {
            user = await apiRequest(`/users/${encodeURIComponent(username)}`);
        } catch (err) {
            // User doesn't exist, create new one
            user = await apiRequest('/users', {
                method: 'POST',
                body: JSON.stringify({ username })
            });
        }

        state.user = user;
        localStorage.setItem('trivia_user', JSON.stringify(user));

        showHomeScreen();
    } catch (err) {
        elements.loginError.textContent = err.message;
    }
}

function handleLogout() {
    state.user = null;
    localStorage.removeItem('trivia_user');
    elements.usernameInput.value = '';
    showScreen('login');
}

function checkSavedSession() {
    const saved = localStorage.getItem('trivia_user');
    if (saved) {
        try {
            state.user = JSON.parse(saved);
            showHomeScreen();
        } catch (e) {
            localStorage.removeItem('trivia_user');
        }
    }
}

// ==========================================
// Home Screen
// ==========================================

async function showHomeScreen() {
    elements.displayUsername.textContent = state.user.username;
    showScreen('home');
    await loadUserStats();
}

async function loadUserStats() {
    try {
        const attempts = await apiRequest(`/users/${state.user.id}/attempts`);

        // Calculate stats
        const totalGames = attempts.length;
        const avgScore = totalGames > 0
            ? Math.round(attempts.reduce((sum, a) => sum + a.score, 0) / totalGames)
            : 0;
        const bestScore = totalGames > 0
            ? Math.max(...attempts.map(a => a.score))
            : 0;

        elements.statGames.textContent = totalGames;
        elements.statAvg.textContent = `${avgScore}%`;
        elements.statBest.textContent = `${bestScore}%`;

        // Render history
        if (attempts.length === 0) {
            elements.historyList.innerHTML = '<p class="empty-state">Nessuna partita ancora. Inizia a giocare!</p>';
        } else {
            elements.historyList.innerHTML = attempts.slice(0, 10).map(a => `
        <div class="history-item">
          <span class="history-score" style="color: ${getScoreColor(a.score)}">${a.score}%</span>
          <div class="history-details">
            <span>${a.correct_count}/${a.total_questions} corrette</span>
            <span>${formatTime(a.time_seconds)} • ${formatDate(a.completed_at)}</span>
          </div>
        </div>
      `).join('');
        }
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

function getScoreColor(score) {
    if (score >= 80) return 'var(--color-success)';
    if (score >= 50) return 'var(--color-warning)';
    return 'var(--color-error)';
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' });
}

// ==========================================
// Quiz Functions
// ==========================================

async function startQuiz() {
    try {
        const data = await apiRequest('/quiz/start', {
            method: 'POST',
            body: JSON.stringify({ user_id: state.user.id })
        });

        state.quiz = {
            questions: data.questions,
            currentIndex: 0,
            answers: [],
            startTime: Date.now(),
            timerInterval: null
        };

        showScreen('quiz');
        startTimer();
        renderQuestion();
    } catch (err) {
        alert('Failed to start quiz: ' + err.message);
    }
}

function startTimer() {
    updateTimer();
    state.quiz.timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    const elapsed = (Date.now() - state.quiz.startTime) / 1000;
    elements.timerValue.textContent = formatTime(elapsed);
}

function stopTimer() {
    if (state.quiz.timerInterval) {
        clearInterval(state.quiz.timerInterval);
        state.quiz.timerInterval = null;
    }
}

function renderQuestion() {
    const { questions, currentIndex } = state.quiz;
    const question = questions[currentIndex];
    const total = questions.length;

    // Update progress
    elements.questionCounter.textContent = `${currentIndex + 1}/${total}`;
    elements.progressFill.style.width = `${((currentIndex + 1) / total) * 100}%`;

    // Update question
    elements.questionCategory.textContent = question.category;
    elements.questionText.textContent = question.text;

    // Render options
    elements.optionsContainer.innerHTML = question.options.map(opt => `
    <button class="option-btn" data-key="${opt.key}">
      <span class="option-key">${opt.key}</span>
      <span class="option-text">${opt.text}</span>
    </button>
  `).join('');

    // Add click handlers
    elements.optionsContainer.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', () => selectOption(btn.dataset.key));
    });

    // Reset next button
    elements.nextBtn.disabled = true;
    elements.nextBtn.textContent = currentIndex === total - 1 ? 'Termina Quiz' : 'Prossima Domanda';
}

function selectOption(key) {
    const { currentIndex } = state.quiz;

    // Save answer
    state.quiz.answers[currentIndex] = key;

    // Update UI
    elements.optionsContainer.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.key === key) {
            btn.classList.add('selected');
        }
    });

    // Enable next
    elements.nextBtn.disabled = false;
}

function nextQuestion() {
    const { questions, currentIndex } = state.quiz;

    if (currentIndex < questions.length - 1) {
        state.quiz.currentIndex++;
        renderQuestion();
    } else {
        submitQuiz();
    }
}

async function submitQuiz() {
    stopTimer();

    const timeSeconds = (Date.now() - state.quiz.startTime) / 1000;
    const answers = state.quiz.questions.map((q, i) => ({
        question_id: q.id,
        answer: state.quiz.answers[i] || ''
    }));

    try {
        const result = await apiRequest('/quiz/submit', {
            method: 'POST',
            body: JSON.stringify({
                user_id: state.user.id,
                answers,
                time_seconds: timeSeconds
            })
        });

        showResult(result);
    } catch (err) {
        alert('Failed to submit quiz: ' + err.message);
        showHomeScreen();
    }
}

function showResult(result) {
    // Set icon and title based on score
    if (result.score >= 80) {
        elements.resultIcon.textContent = '🏆';
        elements.resultTitle.textContent = 'Fantastico!';
        elements.resultSubtitle.textContent = 'Sei un vero esperto!';
    } else if (result.score >= 50) {
        elements.resultIcon.textContent = '👍';
        elements.resultTitle.textContent = 'Bel lavoro!';
        elements.resultSubtitle.textContent = 'Continua così!';
    } else {
        elements.resultIcon.textContent = '📚';
        elements.resultTitle.textContent = 'Puoi fare di meglio!';
        elements.resultSubtitle.textContent = 'Riprova e migliorerai!';
    }

    elements.resultScore.textContent = `${result.score}%`;
    elements.resultCorrect.textContent = `${result.correct_count}/${result.total_questions}`;
    elements.resultTime.textContent = formatTime(result.time_seconds);

    showScreen('result');
}

// ==========================================
// Event Listeners
// ==========================================

elements.loginForm.addEventListener('submit', handleLogin);
elements.logoutBtn.addEventListener('click', handleLogout);
elements.startQuizBtn.addEventListener('click', startQuiz);
elements.nextBtn.addEventListener('click', nextQuestion);
elements.playAgainBtn.addEventListener('click', startQuiz);
elements.backHomeBtn.addEventListener('click', showHomeScreen);

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (screens.quiz.classList.contains('active')) {
        if (['A', 'B', 'C', 'D'].includes(e.key.toUpperCase())) {
            selectOption(e.key.toUpperCase());
        } else if (e.key === 'Enter' && !elements.nextBtn.disabled) {
            nextQuestion();
        }
    }
});

// ==========================================
// Initialize
// ==========================================

checkSavedSession();
