const express = require('express');
const router = express.Router();
const db = require('../database');

const DEFAULT_NUM_QUESTIONS = 10;

// POST /api/quiz/start - Start a new quiz session
router.post('/start', (req, res) => {
    const { user_id, num_questions } = req.body;
    const numQ = num_questions || DEFAULT_NUM_QUESTIONS;

    if (!user_id || isNaN(parseInt(user_id))) {
        return res.status(400).json({ error: 'Valid user_id is required' });
    }

    try {
        // Verify user exists
        const user = db.prepare('SELECT id FROM users WHERE id = ?').get(user_id);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Get random questions without correct answers
        const questions = db.prepare(`
      SELECT id, text, option_a, option_b, option_c, option_d, category
      FROM questions
      ORDER BY RANDOM()
      LIMIT ?
    `).all(numQ);

        if (questions.length === 0) {
            return res.status(500).json({ error: 'No questions available' });
        }

        // Format questions for client (without correct_answer)
        const formattedQuestions = questions.map(q => ({
            id: q.id,
            text: q.text,
            category: q.category,
            options: [
                { key: 'A', text: q.option_a },
                { key: 'B', text: q.option_b },
                { key: 'C', text: q.option_c },
                { key: 'D', text: q.option_d }
            ]
        }));

        res.json({
            session_id: Date.now().toString(36) + Math.random().toString(36).substr(2),
            total_questions: questions.length,
            questions: formattedQuestions
        });
    } catch (error) {
        console.error('Error starting quiz:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// POST /api/quiz/submit - Submit quiz answers
router.post('/submit', (req, res) => {
    const { user_id, answers, time_seconds } = req.body;

    // Validation
    if (!user_id || isNaN(parseInt(user_id))) {
        return res.status(400).json({ error: 'Valid user_id is required' });
    }
    if (!Array.isArray(answers) || answers.length === 0) {
        return res.status(400).json({ error: 'Answers array is required' });
    }
    if (typeof time_seconds !== 'number' || time_seconds < 0) {
        return res.status(400).json({ error: 'Valid time_seconds is required' });
    }

    try {
        // Verify user exists
        const user = db.prepare('SELECT id FROM users WHERE id = ?').get(user_id);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Get question IDs and validate answers
        const questionIds = answers.map(a => a.question_id);
        const placeholders = questionIds.map(() => '?').join(',');
        const questions = db.prepare(`
      SELECT id, correct_answer FROM questions WHERE id IN (${placeholders})
    `).all(...questionIds);

        // Create a map for quick lookup
        const correctAnswers = new Map(questions.map(q => [q.id, q.correct_answer]));

        // Calculate score
        let correctCount = 0;
        for (const answer of answers) {
            const correct = correctAnswers.get(answer.question_id);
            if (correct && answer.answer === correct) {
                correctCount++;
            }
        }

        const totalQuestions = answers.length;
        const score = Math.round((correctCount / totalQuestions) * 100);

        // Save attempt
        const result = db.prepare(`
      INSERT INTO attempts (user_id, score, correct_count, total_questions, time_seconds)
      VALUES (?, ?, ?, ?, ?)
    `).run(user_id, score, correctCount, totalQuestions, Math.round(time_seconds));

        const attempt = db.prepare('SELECT * FROM attempts WHERE id = ?').get(result.lastInsertRowid);

        res.json({
            attempt_id: attempt.id,
            score: attempt.score,
            correct_count: attempt.correct_count,
            total_questions: attempt.total_questions,
            time_seconds: attempt.time_seconds,
            completed_at: attempt.completed_at
        });
    } catch (error) {
        console.error('Error submitting quiz:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
