/**
 * Attempts entity - Mock data
 */
const AttemptsData = {
    // Summary stats
    total: 312,
    avgScore: 62,
    avgTime: 272, // seconds (4:32)
    avgCorrect: 6.2,
    perfectScores: 18,
    failedAttempts: 24, // score < 40%

    // Score distribution
    scoreDistribution: [
        { label: '0-20%', value: 8, color: 'error' },
        { label: '21-40%', value: 31, color: 'error' },
        { label: '41-60%', value: 98, color: 'warning' },
        { label: '61-80%', value: 127, color: 'success' },
        { label: '81-100%', value: 48, color: 'success' },
    ],

    // Daily attempts (last 7 days)
    dailyTrend: [
        { label: 'Lun', value: 42 },
        { label: 'Mar', value: 38 },
        { label: 'Mer', value: 51 },
        { label: 'Gio', value: 45 },
        { label: 'Ven', value: 39 },
        { label: 'Sab', value: 55 },
        { label: 'Dom', value: 42 },
    ],

    // Time distribution
    timeDistribution: [
        { label: '<3 min', value: 45, color: 'cyan' },
        { label: '3-5 min', value: 124, color: 'success' },
        { label: '5-7 min', value: 98, color: 'primary' },
        { label: '7-10 min', value: 35, color: 'warning' },
        { label: '>10 min', value: 10, color: 'error' },
    ],

    // Correct answers distribution
    correctDistribution: [
        { label: '0-2', value: 15 },
        { label: '3-4', value: 42 },
        { label: '5-6', value: 95 },
        { label: '7-8', value: 112 },
        { label: '9-10', value: 48 },
    ],

    // Sample records
    sampleRecords: [
        { id: 312, user_id: 1, username: 'marco_quiz', score: 80, correct_count: 8, total_questions: 10, time_seconds: 245, completed_at: '2024-12-17 16:42:18' },
        { id: 311, user_id: 3, username: 'ale_trivia', score: 70, correct_count: 7, total_questions: 10, time_seconds: 312, completed_at: '2024-12-17 15:30:05' },
        { id: 310, user_id: 2, username: 'giulia.test', score: 50, correct_count: 5, total_questions: 10, time_seconds: 198, completed_at: '2024-12-17 14:55:33' },
        { id: 309, user_id: 5, username: 'quiz_lover', score: 60, correct_count: 6, total_questions: 10, time_seconds: 420, completed_at: '2024-12-17 12:22:11' },
        { id: 308, user_id: 4, username: 'user_master', score: 100, correct_count: 10, total_questions: 10, time_seconds: 178, completed_at: '2024-12-17 10:15:44' },
        { id: 307, user_id: 6, username: 'newbie_2024', score: 40, correct_count: 4, total_questions: 10, time_seconds: 520, completed_at: '2024-12-16 22:08:19' },
        { id: 306, user_id: 1, username: 'marco_quiz', score: 90, correct_count: 9, total_questions: 10, time_seconds: 289, completed_at: '2024-12-16 18:44:55' },
    ],

    // Insights
    insights: [
        { icon: '📈', type: 'success', text: '<strong>56% degli attempts</strong> ha score ≥60%, indicando un buon livello medio di preparazione degli utenti.' },
        { icon: '⏱️', type: 'info', text: 'Il <strong>tempo medio è 4:32</strong> (40-45 sec/domanda). Gli utenti con score >80% sono in media <strong>25% più veloci</strong>.' },
        { icon: '🏆', type: 'success', text: '<strong>18 quiz perfetti (5.8%)</strong> completati, tutti da utenti con almeno 5 tentativi precedenti.' },
        { icon: '⚠️', type: 'warning', text: '<strong>24 tentativi (7.7%)</strong> hanno score <40%. Correlazione con primo tentativo dell\'utente nel 75% dei casi.' },
    ]
};
