/**
 * Questions entity - Mock data
 */
const QuestionsData = {
    // Summary stats
    total: 25,
    categories: 5,
    avgCorrectRate: 58,

    // Category distribution
    categoryDistribution: [
        { label: 'Science', value: 5, color: 'primary' },
        { label: 'Geography', value: 5, color: 'success' },
        { label: 'History', value: 5, color: 'purple' },
        { label: 'Technology', value: 5, color: 'cyan' },
        { label: 'Entertainment', value: 5, color: 'warning' },
    ],

    // Correct answer distribution
    answerDistribution: [
        { label: 'Risposta A', value: 3, color: 'primary' },
        { label: 'Risposta B', value: 12, color: 'success' },
        { label: 'Risposta C', value: 8, color: 'warning' },
        { label: 'Risposta D', value: 2, color: 'purple' },
    ],

    // Difficulty by correct rate (simulated from attempts)
    difficultyDistribution: [
        { label: 'Facili (>70%)', value: 7, color: 'success' },
        { label: 'Medie (50-70%)', value: 11, color: 'warning' },
        { label: 'Difficili (<50%)', value: 7, color: 'error' },
    ],

    // Hardest questions
    hardestQuestions: [
        { text: 'Qual è l\'elemento più abbondante nell\'universo?', category: 'Science', correctRate: 32 },
        { text: 'Chi era il primo imperatore romano?', category: 'History', correctRate: 38 },
        { text: 'Qual è il fiume più lungo del mondo?', category: 'Geography', correctRate: 41 },
        { text: 'Chi ha inventato il World Wide Web?', category: 'Technology', correctRate: 44 },
        { text: 'Quanti stati ha l\'Italia?', category: 'Geography', correctRate: 47 },
    ],

    // Easiest questions
    easiestQuestions: [
        { text: 'Quale band ha cantato "Bohemian Rhapsody"?', category: 'Entertainment', correctRate: 89 },
        { text: 'In quale film appare la frase "Io sono tuo padre"?', category: 'Entertainment', correctRate: 85 },
        { text: 'Quanti pianeti ci sono nel sistema solare?', category: 'Science', correctRate: 82 },
        { text: 'Chi ha sviluppato la teoria della relatività?', category: 'Science', correctRate: 79 },
        { text: 'Chi ha fondato Microsoft?', category: 'Technology', correctRate: 76 },
    ],

    // Sample records
    sampleRecords: [
        { id: 1, text: 'Qual è il simbolo chimico dell\'oro?', category: 'Science', correct_answer: 'B', correctRate: 68 },
        { id: 6, text: 'Qual è la capitale dell\'Australia?', category: 'Geography', correct_answer: 'C', correctRate: 52 },
        { id: 11, text: 'In che anno è caduto il Muro di Berlino?', category: 'History', correct_answer: 'B', correctRate: 71 },
        { id: 16, text: 'Chi ha fondato Microsoft?', category: 'Technology', correct_answer: 'B', correctRate: 76 },
        { id: 21, text: 'Chi ha diretto "Il Padrino"?', category: 'Entertainment', correct_answer: 'B', correctRate: 55 },
        { id: 4, text: 'Qual è l\'elemento più abbondante nell\'universo?', category: 'Science', correct_answer: 'C', correctRate: 32 },
        { id: 23, text: 'In quale film appare "Io sono tuo padre"?', category: 'Entertainment', correct_answer: 'B', correctRate: 85 },
    ],

    // Insights
    insights: [
        { icon: '⚖️', type: 'warning', text: '<strong>48% delle risposte corrette sono B</strong>. Sbilanciamento significativo che potrebbe favorire strategie di guessing.' },
        { icon: '📚', type: 'info', text: 'Le domande di <strong>Entertainment</strong> hanno il tasso di correttezza più alto (72% medio), mentre <strong>Geography</strong> è la categoria più difficile (49%).' },
        { icon: '🎯', type: 'success', text: 'Il <strong>44% delle domande</strong> ha difficoltà bilanciata (50-70% correct rate), garantendo un\'esperienza equilibrata.' },
        { icon: '⚠️', type: 'warning', text: 'Le domande <strong>D-correct</strong> sono solo 2 (8%). Considerare l\'aggiunta di domande con risposte D corrette.' },
    ]
};
