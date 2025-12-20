const express = require('express');
const router = express.Router();
const db = require('../database');

// POST /api/users - Create a new user
router.post('/', (req, res) => {
    const { username } = req.body;

    if (!username || typeof username !== 'string' || username.trim().length < 2) {
        return res.status(400).json({ error: 'Username must be at least 2 characters' });
    }

    const cleanUsername = username.trim();

    try {
        // Check if username exists
        const existing = db.prepare('SELECT id FROM users WHERE username = ?').get(cleanUsername);
        if (existing) {
            return res.status(409).json({ error: 'Username already exists' });
        }

        const result = db.prepare('INSERT INTO users (username) VALUES (?)').run(cleanUsername);
        const user = db.prepare('SELECT id, username, created_at FROM users WHERE id = ?').get(result.lastInsertRowid);

        res.status(201).json(user);
    } catch (error) {
        console.error('Error creating user:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// GET /api/users/:username - Get user by username
router.get('/:username', (req, res) => {
    const { username } = req.params;

    try {
        const user = db.prepare('SELECT id, username, created_at FROM users WHERE username = ?').get(username);

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json(user);
    } catch (error) {
        console.error('Error fetching user:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// GET /api/users/:id/attempts - Get all attempts for a user
router.get('/:id/attempts', (req, res) => {
    const userId = parseInt(req.params.id);

    if (isNaN(userId)) {
        return res.status(400).json({ error: 'Invalid user ID' });
    }

    try {
        const attempts = db.prepare(`
      SELECT id, score, correct_count, total_questions, time_seconds, completed_at
      FROM attempts
      WHERE user_id = ?
      ORDER BY completed_at DESC
    `).all(userId);

        res.json(attempts);
    } catch (error) {
        console.error('Error fetching attempts:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
