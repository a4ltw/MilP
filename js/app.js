// Military Vocabulary Learning System
// Main Application JavaScript

class VocabApp {
    constructor() {
        this.vocabulary = [];
        this.filteredVocabulary = [];
        this.userProgress = this.loadProgress();
        this.currentLearnSet = [];
        this.currentLearnIndex = 0;
        this.learnMode = 'ch-en'; // 'ch-en' or 'en-ch'
        this.quizMode = 'ch-en';
        this.quizType = 'multiple';
        this.currentQuiz = [];
        this.currentQuizIndex = 0;
        this.quizScore = 0;
        this.wrongAnswers = [];

        this.init();
    }

    async init() {
        try {
            await this.loadVocabulary();
            this.setupEventListeners();
            this.renderBrowseTab();
            this.updateProgressTab();
        } catch (error) {
            console.error('Initialization failed:', error);
            alert('載入詞彙資料失敗，請檢查 data/vocabulary.json 檔案');
        }
    }

    async loadVocabulary() {
        try {
            const response = await fetch('data/vocabulary.json');
            const data = await response.json();
            this.vocabulary = data.vocabulary;
            this.filteredVocabulary = [...this.vocabulary];
        } catch (error) {
            throw new Error('Failed to load vocabulary');
        }
    }

    loadProgress() {
        const saved = localStorage.getItem('vocabProgress');
        return saved ? JSON.parse(saved) : {
            mastered: [],
            needReview: []
        };
    }

    saveProgress() {
        localStorage.setItem('vocabProgress', JSON.stringify(this.userProgress));
    }

    setupEventListeners() {
        // Tab Navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Browse Tab
        document.getElementById('search-input').addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.getElementById('category-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('difficulty-filter').addEventListener('change', () => this.applyFilters());
        document.getElementById('sort-option').addEventListener('change', () => this.applySorting());

        // Learn Tab
        document.getElementById('mode-ch-en').addEventListener('click', () => this.setLearnMode('ch-en'));
        document.getElementById('mode-en-ch').addEventListener('click', () => this.setLearnMode('en-ch'));
        document.getElementById('start-learn').addEventListener('click', () => this.startLearning());
        document.getElementById('exit-learn').addEventListener('click', () => this.exitLearning());
        document.getElementById('flashcard').addEventListener('click', () => this.flipCard());
        document.getElementById('btn-need-review').addEventListener('click', () => this.markNeedReview());
        document.getElementById('btn-next').addEventListener('click', () => this.nextCard());
        document.getElementById('btn-mastered').addEventListener('click', () => this.markMastered());
        document.getElementById('restart-learn').addEventListener('click', () => this.startLearning());

        // Keyboard shortcuts for flashcards
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcut(e));

        // Quiz Tab
        document.getElementById('quiz-mode-ch-en').addEventListener('click', () => this.setQuizMode('ch-en'));
        document.getElementById('quiz-mode-en-ch').addEventListener('click', () => this.setQuizMode('en-ch'));
        document.getElementById('start-quiz').addEventListener('click', () => this.startQuiz());
        document.getElementById('submit-answer').addEventListener('click', () => this.submitAnswer());
        document.getElementById('next-question').addEventListener('click', () => this.nextQuestion());
        document.getElementById('retry-quiz').addEventListener('click', () => this.retryQuiz());
        document.getElementById('review-wrong').addEventListener('click', () => this.addWrongToReview());

        // Progress Tab
        document.getElementById('reset-progress').addEventListener('click', () => this.resetProgress());
        document.getElementById('export-progress').addEventListener('click', () => this.exportProgress());
    }

    handleKeyboardShortcut(e) {
        // Check if flashcard container is visible
        const flashcardContainer = document.getElementById('flashcard-container');
        const isFlashcardVisible = flashcardContainer && flashcardContainer.style.display !== 'none';

        // Check if quiz container is visible
        const quizContainer = document.getElementById('quiz-container');
        const isQuizVisible = quizContainer && quizContainer.style.display !== 'none';

        // If neither is visible, don't handle shortcuts
        if (!isFlashcardVisible && !isQuizVisible) {
            return;
        }

        // Ignore if user is typing in an input field (except for quiz mode)
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            // In quiz mode, allow space for submit/next
            if (!isQuizVisible || (e.key !== ' ' && e.key !== 'Enter')) {
                return;
            }
        }

        // Handle flashcard shortcuts
        if (isFlashcardVisible) {
            switch(e.key) {
                case '1':
                    e.preventDefault();
                    this.markNeedReview();
                    break;
                case '2':
                    e.preventDefault();
                    this.nextCard();
                    break;
                case '3':
                    e.preventDefault();
                    this.markMastered();
                    break;
                case ' ':
                case 'Enter':
                    e.preventDefault();
                    this.flipCard();
                    break;
            }
        }

        // Handle quiz shortcuts
        if (isQuizVisible) {
            const submitBtn = document.getElementById('submit-answer');
            const nextBtn = document.getElementById('next-question');
            const isSubmitVisible = submitBtn && submitBtn.style.display !== 'none';
            const isNextVisible = nextBtn && nextBtn.style.display !== 'none';

            switch(e.key) {
                case '1':
                case '2':
                case '3':
                case '4':
                    e.preventDefault();
                    this.selectQuizOption(parseInt(e.key) - 1);
                    break;
                case ' ':
                    e.preventDefault();
                    if (isSubmitVisible) {
                        this.submitAnswer();
                    } else if (isNextVisible) {
                        this.nextQuestion();
                    }
                    break;
            }
        }
    }

    selectQuizOption(index) {
        // Only for multiple choice
        if (this.quizType !== 'multiple') {
            return;
        }

        const options = document.querySelectorAll('.quiz-option');
        if (index >= 0 && index < options.length) {
            // Remove previous selection
            options.forEach(opt => opt.classList.remove('selected'));
            // Select the option
            options[index].classList.add('selected');
        }
    }

    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Refresh tab content
        if (tabName === 'progress') {
            this.updateProgressTab();
        }
    }

    // ===== BROWSE TAB =====

    handleSearch(query) {
        this.applyFilters(query);
    }

    applyFilters(searchQuery = '') {
        const query = searchQuery || document.getElementById('search-input').value;
        const category = document.getElementById('category-filter').value;
        const difficulty = document.getElementById('difficulty-filter').value;

        this.filteredVocabulary = this.vocabulary.filter(item => {
            const matchesSearch = !query ||
                item.chinese.includes(query) ||
                item.english.toLowerCase().includes(query.toLowerCase()) ||
                (item.abbreviation && item.abbreviation.toLowerCase().includes(query.toLowerCase()));

            const matchesCategory = category === 'all' || item.category === category;
            const matchesDifficulty = difficulty === 'all' || item.difficulty.toString() === difficulty;

            return matchesSearch && matchesCategory && matchesDifficulty;
        });

        this.applySorting();
    }

    applySorting() {
        const sortBy = document.getElementById('sort-option').value;

        this.filteredVocabulary.sort((a, b) => {
            if (sortBy === 'chinese') {
                return a.chinese.localeCompare(b.chinese, 'zh-TW');
            } else if (sortBy === 'english') {
                return a.english.localeCompare(b.english);
            }
            return 0; // default order
        });

        this.renderVocabList();
    }

    renderBrowseTab() {
        this.renderVocabList();
    }

    renderVocabList() {
        const container = document.getElementById('vocab-list');
        const statsContainer = document.getElementById('vocab-stats');

        if (this.filteredVocabulary.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>沒有找到符合條件的詞彙</h3></div>';
            statsContainer.innerHTML = '';
            return;
        }

        container.innerHTML = this.filteredVocabulary.map(item => this.createVocabCard(item)).join('');
        statsContainer.innerHTML = `顯示 ${this.filteredVocabulary.length} / ${this.vocabulary.length} 個詞彙`;
    }

    createVocabCard(item) {
        const categoryName = {
            'general': '通用',
            'army': '陸軍',
            'navy': '海軍',
            'airforce': '空軍'
        };

        const isMastered = this.userProgress.mastered.includes(item.id);
        const needReview = this.userProgress.needReview.includes(item.id);

        let statusBadge = '';
        if (isMastered) statusBadge = '<span style="color: #27ae60; font-weight: bold;">✓ 已掌握</span>';
        if (needReview) statusBadge = '<span style="color: #f39c12; font-weight: bold;">⚠ 需複習</span>';

        return `
            <div class="vocab-card">
                <span class="category-badge ${item.category}">${categoryName[item.category]}</span>
                <span class="difficulty-indicator difficulty-${item.difficulty}"></span>
                ${statusBadge}
                <h3>${item.chinese}</h3>
                <div class="english">${item.english}</div>
                ${item.abbreviation ? `<div class="abbreviation">${item.abbreviation}</div>` : ''}
                <div class="example">
                    <p>中：${item.examples.chinese}</p>
                    <p>英：${item.examples.english}</p>
                </div>
            </div>
        `;
    }

    // ===== LEARNING MODE =====

    setLearnMode(mode) {
        this.learnMode = mode;
        document.getElementById('mode-ch-en').classList.toggle('active', mode === 'ch-en');
        document.getElementById('mode-en-ch').classList.toggle('active', mode === 'en-ch');
    }

    startLearning() {
        const category = document.getElementById('learn-category').value;

        // Get vocabulary based on category
        let vocabSet;
        if (category === 'review') {
            vocabSet = this.vocabulary.filter(item => this.userProgress.needReview.includes(item.id));
            if (vocabSet.length === 0) {
                alert('沒有需要複習的詞彙！');
                return;
            }
        } else if (category === 'all') {
            vocabSet = [...this.vocabulary];
        } else {
            vocabSet = this.vocabulary.filter(item => item.category === category);
        }

        // Shuffle the set
        this.currentLearnSet = this.shuffleArray(vocabSet);
        this.currentLearnIndex = 0;

        // Hide controls, show flashcard
        document.querySelector('.learn-controls').style.display = 'none';
        document.getElementById('flashcard-container').style.display = 'block';
        document.getElementById('learn-complete').style.display = 'none';

        this.showCard();
    }

    showCard() {
        if (this.currentLearnIndex >= this.currentLearnSet.length) {
            this.completeLearn();
            return;
        }

        const item = this.currentLearnSet[this.currentLearnIndex];
        const flashcard = document.getElementById('flashcard');
        flashcard.classList.remove('flipped');

        // Update counter
        document.getElementById('card-counter').textContent =
            `${this.currentLearnIndex + 1} / ${this.currentLearnSet.length}`;

        // Set card content based on mode
        if (this.learnMode === 'ch-en') {
            document.getElementById('card-question').textContent = item.chinese;
            document.getElementById('card-answer').textContent = item.english;
        } else {
            document.getElementById('card-question').textContent = item.english;
            document.getElementById('card-answer').textContent = item.chinese;
        }

        document.getElementById('card-abbreviation').textContent =
            item.abbreviation ? `縮寫: ${item.abbreviation}` : '';
        document.getElementById('card-example').innerHTML =
            `<div style="margin-top: 15px;">
                <div>中：${item.examples.chinese}</div>
                <div style="margin-top: 5px;">英：${item.examples.english}</div>
            </div>`;
    }

    flipCard() {
        document.getElementById('flashcard').classList.toggle('flipped');
    }

    markNeedReview() {
        const item = this.currentLearnSet[this.currentLearnIndex];
        if (!this.userProgress.needReview.includes(item.id)) {
            this.userProgress.needReview.push(item.id);
        }
        // Remove from mastered if it was there
        this.userProgress.mastered = this.userProgress.mastered.filter(id => id !== item.id);
        this.saveProgress();
        this.nextCard();
    }

    markMastered() {
        const item = this.currentLearnSet[this.currentLearnIndex];
        if (!this.userProgress.mastered.includes(item.id)) {
            this.userProgress.mastered.push(item.id);
        }
        // Remove from review if it was there
        this.userProgress.needReview = this.userProgress.needReview.filter(id => id !== item.id);
        this.saveProgress();
        this.nextCard();
    }

    nextCard() {
        this.currentLearnIndex++;
        this.showCard();
    }

    completeLearn() {
        const mastered = this.currentLearnSet.filter(item =>
            this.userProgress.mastered.includes(item.id)
        ).length;

        const review = this.currentLearnSet.filter(item =>
            this.userProgress.needReview.includes(item.id)
        ).length;

        document.getElementById('flashcard-container').style.display = 'none';
        document.getElementById('learn-complete').style.display = 'block';

        document.getElementById('learn-total').textContent = this.currentLearnSet.length;
        document.getElementById('learn-mastered').textContent = mastered;
        document.getElementById('learn-review').textContent = review;
    }

    exitLearning() {
        document.querySelector('.learn-controls').style.display = 'block';
        document.getElementById('flashcard-container').style.display = 'none';
        document.getElementById('learn-complete').style.display = 'none';
    }

    // ===== QUIZ MODE =====

    setQuizMode(mode) {
        this.quizMode = mode;
        document.getElementById('quiz-mode-ch-en').classList.toggle('active', mode === 'ch-en');
        document.getElementById('quiz-mode-en-ch').classList.toggle('active', mode === 'en-ch');
    }

    startQuiz() {
        this.quizType = document.getElementById('quiz-type').value;
        const category = document.getElementById('quiz-category').value;
        const count = parseInt(document.getElementById('quiz-count').value);

        // Get vocabulary based on category
        let vocabSet = category === 'all' ?
            [...this.vocabulary] :
            this.vocabulary.filter(item => item.category === category);

        if (vocabSet.length < count) {
            alert(`該分類只有 ${vocabSet.length} 個詞彙，少於所需的 ${count} 題`);
            return;
        }

        // Shuffle and take the required count
        this.currentQuiz = this.shuffleArray(vocabSet).slice(0, count);
        this.currentQuizIndex = 0;
        this.quizScore = 0;
        this.wrongAnswers = [];

        // Hide setup, show quiz
        document.querySelector('.quiz-setup').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        document.getElementById('quiz-result').style.display = 'none';

        this.showQuestion();
    }

    showQuestion() {
        if (this.currentQuizIndex >= this.currentQuiz.length) {
            this.showQuizResult();
            return;
        }

        const item = this.currentQuiz[this.currentQuizIndex];

        // Update progress
        document.getElementById('quiz-counter').textContent =
            `題目 ${this.currentQuizIndex + 1} / ${this.currentQuiz.length}`;
        document.getElementById('quiz-score').textContent = `得分：${this.quizScore}`;

        // Set question text
        const questionText = this.quizMode === 'ch-en' ? item.chinese : item.english;
        document.getElementById('question-text').textContent = questionText;

        // Clear feedback
        document.getElementById('quiz-feedback').innerHTML = '';
        document.getElementById('quiz-feedback').className = 'quiz-feedback';

        // Render options based on quiz type
        const optionsContainer = document.getElementById('quiz-options');

        if (this.quizType === 'multiple') {
            this.renderMultipleChoice(item);
        } else {
            this.renderFillBlank(item);
        }

        // Show/hide buttons
        document.getElementById('submit-answer').style.display = 'block';
        document.getElementById('next-question').style.display = 'none';
    }

    renderMultipleChoice(correctItem) {
        const optionsContainer = document.getElementById('quiz-options');
        const correctAnswer = this.quizMode === 'ch-en' ? correctItem.english : correctItem.chinese;

        // Get wrong options from same category
        let wrongOptions = this.vocabulary
            .filter(item =>
                item.id !== correctItem.id &&
                item.category === correctItem.category
            )
            .map(item => this.quizMode === 'ch-en' ? item.english : item.chinese);

        // Shuffle and take 3
        wrongOptions = this.shuffleArray(wrongOptions).slice(0, 3);

        // Combine and shuffle all options
        const allOptions = this.shuffleArray([correctAnswer, ...wrongOptions]);

        optionsContainer.innerHTML = allOptions.map((option, index) => `
            <div class="quiz-option" data-option="${option}">
                <span class="option-letter">${String.fromCharCode(65 + index)}</span>. ${option}
                <span class="shortcut-key">[${index + 1}]</span>
            </div>
        `).join('');

        // Add click listeners
        optionsContainer.querySelectorAll('.quiz-option').forEach(opt => {
            opt.addEventListener('click', (e) => {
                // Remove previous selection
                optionsContainer.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
                // Add selection to clicked option
                e.currentTarget.classList.add('selected');
            });
        });
    }

    renderFillBlank(item) {
        const optionsContainer = document.getElementById('quiz-options');
        optionsContainer.innerHTML = `
            <input type="text" class="quiz-input" id="fill-answer"
                   placeholder="請輸入答案..." autocomplete="off">
        `;

        // Allow Enter key to submit
        document.getElementById('fill-answer').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitAnswer();
            }
        });

        // Focus on input
        setTimeout(() => document.getElementById('fill-answer').focus(), 100);
    }

    submitAnswer() {
        const item = this.currentQuiz[this.currentQuizIndex];
        const correctAnswer = this.quizMode === 'ch-en' ? item.english : item.chinese;
        let userAnswer = '';
        let isCorrect = false;

        if (this.quizType === 'multiple') {
            const selected = document.querySelector('.quiz-option.selected');
            if (!selected) {
                alert('請選擇一個答案');
                return;
            }
            userAnswer = selected.dataset.option;
            isCorrect = userAnswer === correctAnswer;

            // Mark correct/wrong
            document.querySelectorAll('.quiz-option').forEach(opt => {
                opt.classList.add('disabled');
                if (opt.dataset.option === correctAnswer) {
                    opt.classList.add('correct');
                } else if (opt.classList.contains('selected')) {
                    opt.classList.add('wrong');
                }
            });
        } else {
            userAnswer = document.getElementById('fill-answer').value.trim();
            if (!userAnswer) {
                alert('請輸入答案');
                return;
            }

            // Check if answer is correct (case-insensitive for English, exact for Chinese)
            if (this.quizMode === 'ch-en') {
                isCorrect = userAnswer.toLowerCase() === correctAnswer.toLowerCase();
            } else {
                isCorrect = userAnswer === correctAnswer;
            }

            document.getElementById('fill-answer').disabled = true;
        }

        // Update score and feedback
        if (isCorrect) {
            this.quizScore++;
            document.getElementById('quiz-feedback').innerHTML = '✓ 正確！';
            document.getElementById('quiz-feedback').classList.add('correct');
        } else {
            document.getElementById('quiz-feedback').innerHTML =
                `✗ 錯誤！正確答案是：<strong>${correctAnswer}</strong>`;
            document.getElementById('quiz-feedback').classList.add('wrong');

            // Record wrong answer
            this.wrongAnswers.push({
                question: this.quizMode === 'ch-en' ? item.chinese : item.english,
                userAnswer: userAnswer,
                correctAnswer: correctAnswer,
                item: item
            });
        }

        // Update score display
        document.getElementById('quiz-score').textContent = `得分：${this.quizScore}`;

        // Show next button
        document.getElementById('submit-answer').style.display = 'none';
        document.getElementById('next-question').style.display = 'block';
    }

    nextQuestion() {
        this.currentQuizIndex++;
        this.showQuestion();
    }

    showQuizResult() {
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('quiz-result').style.display = 'block';

        const percentage = Math.round((this.quizScore / this.currentQuiz.length) * 100);

        document.getElementById('final-score').textContent = percentage;
        document.getElementById('correct-count').textContent = this.quizScore;
        document.getElementById('wrong-count').textContent = this.currentQuiz.length - this.quizScore;
        document.getElementById('total-questions').textContent = this.currentQuiz.length;

        // Show wrong answers
        const wrongContainer = document.getElementById('wrong-answers');
        if (this.wrongAnswers.length > 0) {
            wrongContainer.innerHTML = `
                <h3>錯誤題目回顧</h3>
                ${this.wrongAnswers.map((wa, index) => `
                    <div class="wrong-item">
                        <strong>題 ${index + 1}:</strong> ${wa.question}<br>
                        你的答案：<span style="color: #e74c3c;">${wa.userAnswer}</span><br>
                        正確答案：<span style="color: #27ae60;">${wa.correctAnswer}</span>
                    </div>
                `).join('')}
            `;
        } else {
            wrongContainer.innerHTML = '<p style="text-align: center; color: #27ae60;">完美！全部答對！</p>';
        }
    }

    retryQuiz() {
        document.querySelector('.quiz-setup').style.display = 'block';
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('quiz-result').style.display = 'none';
    }

    addWrongToReview() {
        this.wrongAnswers.forEach(wa => {
            if (!this.userProgress.needReview.includes(wa.item.id)) {
                this.userProgress.needReview.push(wa.item.id);
            }
        });
        this.saveProgress();
        alert(`已將 ${this.wrongAnswers.length} 個詞彙加入複習清單`);
        this.updateProgressTab();
    }

    // ===== PROGRESS TAB =====

    updateProgressTab() {
        const totalVocab = this.vocabulary.length;
        const masteredCount = this.userProgress.mastered.length;
        const reviewCount = this.userProgress.needReview.length;
        const masteryRate = totalVocab > 0 ? Math.round((masteredCount / totalVocab) * 100) : 0;

        document.getElementById('total-vocab').textContent = totalVocab;
        document.getElementById('mastered-vocab').textContent = masteredCount;
        document.getElementById('review-vocab').textContent = reviewCount;
        document.getElementById('mastery-rate').textContent = `${masteryRate}%`;

        // Category stats
        this.renderCategoryStats();
    }

    renderCategoryStats() {
        const categories = {
            'general': '通用術語',
            'army': '陸軍',
            'navy': '海軍',
            'airforce': '空軍'
        };

        const container = document.getElementById('category-stats');
        container.innerHTML = Object.keys(categories).map(cat => {
            const total = this.vocabulary.filter(item => item.category === cat).length;
            const mastered = this.vocabulary.filter(item =>
                item.category === cat && this.userProgress.mastered.includes(item.id)
            ).length;
            const percentage = total > 0 ? Math.round((mastered / total) * 100) : 0;

            return `
                <div class="category-stat-item">
                    <div class="category-name">${categories[cat]}</div>
                    <div class="category-progress-bar">
                        <div class="category-progress-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div>${mastered} / ${total} (${percentage}%)</div>
                </div>
            `;
        }).join('');
    }

    resetProgress() {
        if (confirm('確定要重置所有學習進度嗎？此操作無法復原。')) {
            this.userProgress = {
                mastered: [],
                needReview: []
            };
            this.saveProgress();
            this.updateProgressTab();
            this.renderBrowseTab();
            alert('進度已重置');
        }
    }

    exportProgress() {
        const exportData = {
            date: new Date().toISOString(),
            progress: this.userProgress,
            stats: {
                total: this.vocabulary.length,
                mastered: this.userProgress.mastered.length,
                needReview: this.userProgress.needReview.length
            }
        };

        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `vocab-progress-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        URL.revokeObjectURL(url);
    }

    // ===== UTILITY FUNCTIONS =====

    shuffleArray(array) {
        const newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VocabApp();
});
