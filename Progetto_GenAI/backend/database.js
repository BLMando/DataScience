const Database = require('better-sqlite3');
const path = require('path');

const db = new Database(path.join(__dirname, 'trivia.db'));

// Enable foreign keys
db.pragma('foreign_keys = ON');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A', 'B', 'C', 'D')),
    category TEXT DEFAULT 'General'
  );

  CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    correct_count INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    time_seconds INTEGER NOT NULL,
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );
`);

// Seed questions if empty
const questionCount = db.prepare('SELECT COUNT(*) as count FROM questions').get();

if (questionCount.count === 0) {
    const insertQuestion = db.prepare(`
    INSERT INTO questions (text, option_a, option_b, option_c, option_d, correct_answer, category)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

    const questions = [
        // Science
        ['Qual è il simbolo chimico dell\'oro?', 'Ag', 'Au', 'Fe', 'Cu', 'B', 'Science'],
        ['Quanti pianeti ci sono nel sistema solare?', '7', '8', '9', '10', 'B', 'Science'],
        ['Qual è la velocità della luce in km/s (approssimativamente)?', '150.000', '300.000', '450.000', '600.000', 'B', 'Science'],
        ['Qual è l\'elemento più abbondante nell\'universo?', 'Ossigeno', 'Carbonio', 'Idrogeno', 'Elio', 'C', 'Science'],
        ['Chi ha sviluppato la teoria della relatività?', 'Newton', 'Einstein', 'Galileo', 'Hawking', 'B', 'Science'],

        // Geography
        ['Qual è la capitale dell\'Australia?', 'Sydney', 'Melbourne', 'Canberra', 'Perth', 'C', 'Geography'],
        ['Qual è il fiume più lungo del mondo?', 'Nilo', 'Amazzone', 'Yangtze', 'Mississippi', 'A', 'Geography'],
        ['In quale continente si trova l\'Egitto?', 'Asia', 'Europa', 'Africa', 'Oceania', 'C', 'Geography'],
        ['Qual è il paese più grande del mondo per superficie?', 'Canada', 'Cina', 'USA', 'Russia', 'D', 'Geography'],
        ['Quanti stati ha l\'Italia?', '15', '18', '20', '22', 'C', 'Geography'],

        // History
        ['In che anno è caduto il Muro di Berlino?', '1987', '1989', '1991', '1993', 'B', 'History'],
        ['Chi era il primo imperatore romano?', 'Giulio Cesare', 'Augusto', 'Nerone', 'Tiberio', 'B', 'History'],
        ['In che anno Colombo scoprì l\'America?', '1482', '1492', '1502', '1512', 'B', 'History'],
        ['Quale civiltà costruì Machu Picchu?', 'Maya', 'Aztechi', 'Inca', 'Olmec', 'C', 'History'],
        ['Chi dipinse la Cappella Sistina?', 'Leonardo', 'Raffaello', 'Michelangelo', 'Botticelli', 'C', 'History'],

        // Technology
        ['Chi ha fondato Microsoft?', 'Steve Jobs', 'Bill Gates', 'Mark Zuckerberg', 'Jeff Bezos', 'B', 'Technology'],
        ['In che anno è stato lanciato il primo iPhone?', '2005', '2007', '2009', '2011', 'B', 'Technology'],
        ['Cosa significa HTML?', 'Hyper Text Markup Language', 'High Tech Modern Language', 'Hyper Transfer Meta Language', 'Home Tool Markup Language', 'A', 'Technology'],
        ['Qual è il linguaggio di programmazione più usato nel web frontend?', 'Python', 'Java', 'JavaScript', 'C++', 'C', 'Technology'],
        ['Chi ha inventato il World Wide Web?', 'Bill Gates', 'Tim Berners-Lee', 'Steve Jobs', 'Linus Torvalds', 'B', 'Technology'],

        // Entertainment
        ['Chi ha diretto "Il Padrino"?', 'Martin Scorsese', 'Francis Ford Coppola', 'Steven Spielberg', 'Quentin Tarantino', 'B', 'Entertainment'],
        ['Quale band ha cantato "Bohemian Rhapsody"?', 'The Beatles', 'Led Zeppelin', 'Queen', 'Pink Floyd', 'C', 'Entertainment'],
        ['In quale film appare la frase "Io sono tuo padre"?', 'Star Trek', 'Star Wars', 'Matrix', 'Alien', 'B', 'Entertainment'],
        ['Chi ha scritto "Harry Potter"?', 'Stephen King', 'J.R.R. Tolkien', 'J.K. Rowling', 'George R.R. Martin', 'C', 'Entertainment'],
        ['Quale videogioco presenta il personaggio Mario?', 'Sonic', 'Zelda', 'Super Mario Bros', 'Pac-Man', 'C', 'Entertainment'],
    ];

    const insertMany = db.transaction((items) => {
        for (const q of items) {
            insertQuestion.run(...q);
        }
    });

    insertMany(questions);
    console.log('Database seeded with 25 questions');
}

module.exports = db;
