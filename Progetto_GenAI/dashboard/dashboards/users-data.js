/**
 * Users entity - Mock data
 */
const UsersData = {
    // Summary stats
    total: 47,
    newLast7Days: 12,
    newLast30Days: 31,
    activeUsers: 35, // Users with at least 1 attempt in last 30 days

    // Users with most attempts
    topUsers: [
        { username: 'marco_quiz', attempts: 28, avgScore: 78 },
        { username: 'giulia.test', attempts: 24, avgScore: 65 },
        { username: 'ale_trivia', attempts: 19, avgScore: 71 },
        { username: 'user_master', attempts: 17, avgScore: 82 },
        { username: 'quiz_lover', attempts: 15, avgScore: 59 },
    ],

    // Registration trend (last 7 days)
    registrationTrend: [
        { label: 'Lun', value: 2 },
        { label: 'Mar', value: 3 },
        { label: 'Mer', value: 1 },
        { label: 'Gio', value: 2 },
        { label: 'Ven', value: 1 },
        { label: 'Sab', value: 2 },
        { label: 'Dom', value: 1 },
    ],

    // User engagement distribution
    engagementDistribution: [
        { label: '1 quiz', value: 12, color: 'cyan' },
        { label: '2-5 quiz', value: 18, color: 'primary' },
        { label: '6-10 quiz', value: 10, color: 'purple' },
        { label: '11-20 quiz', value: 5, color: 'warning' },
        { label: '20+ quiz', value: 2, color: 'success' },
    ],

    // Sample records
    sampleRecords: [
        { id: 1, username: 'marco_quiz', created_at: '2024-11-15 10:23:41', attempts: 28, avgScore: 78 },
        { id: 2, username: 'giulia.test', created_at: '2024-11-18 14:55:02', attempts: 24, avgScore: 65 },
        { id: 3, username: 'ale_trivia', created_at: '2024-11-22 09:12:33', attempts: 19, avgScore: 71 },
        { id: 4, username: 'user_master', created_at: '2024-11-25 16:44:18', attempts: 17, avgScore: 82 },
        { id: 5, username: 'quiz_lover', created_at: '2024-12-01 11:30:55', attempts: 15, avgScore: 59 },
        { id: 6, username: 'newbie_2024', created_at: '2024-12-10 08:15:22', attempts: 3, avgScore: 45 },
        { id: 7, username: 'test_player', created_at: '2024-12-14 19:22:10', attempts: 1, avgScore: 60 },
    ],

    // Insights
    insights: [
        { icon: '📈', type: 'success', text: '<strong>74% degli utenti</strong> ha completato più di un quiz, indicando un buon tasso di retention iniziale.' },
        { icon: '⚠️', type: 'warning', text: '<strong>12 utenti (26%)</strong> hanno fatto un solo tentativo. Possibile opportunità per campagne di re-engagement.' },
        { icon: '🏆', type: 'info', text: 'I <strong>top 5 utenti</strong> rappresentano il 33% di tutti i tentativi. Power users da monitorare.' },
        { icon: '📅', type: '', text: 'Il <strong>66% delle registrazioni</strong> è avvenuto negli ultimi 30 giorni, segnale di crescita attiva.' },
    ]
};
