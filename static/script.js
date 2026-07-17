document.addEventListener('DOMContentLoaded', () => {
    const questionInput = document.getElementById('question-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = document.getElementById('btn-text');
    const spinner = document.getElementById('spinner');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const resultsSection = document.getElementById('results-section');
    const displayQuestion = document.getElementById('display-question');
    const displayAnswer = document.getElementById('display-answer');

    // Handle form submit
    analyzeBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        
        const question = questionInput.value.trim();

        // 1. Basic validation
        if (!question) {
            showError("Please enter a question before analyzing.");
            return;
        }

        // Clear previous error
        hideError();

        // 2. Set loading state
        setLoading(true);

        try {
            // 3. API Request
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question })
            });

            const result = await response.json();

            if (!response.ok) {
                // If API returned a custom validation/execution error
                throw new Error(result.detail || "An unexpected error occurred while communicating with Gemini.");
            }

            // 4. Render results on success
            displayQuestion.textContent = result.question;
            displayAnswer.innerHTML = formatMarkdown(result.answer);

            // Render evidence sources
            const displayEvidence = document.getElementById('display-evidence');
            displayEvidence.innerHTML = ''; // Clear previous results

            const sources = result.sources || [];
            if (sources.length === 0) {
                const noEvidenceEl = document.createElement('div');
                noEvidenceEl.className = 'no-evidence-box animate-fade-in';
                noEvidenceEl.innerHTML = '<i class="fa-solid fa-circle-info" style="margin-right: 0.5rem; opacity: 0.6;"></i>No trusted evidence found.';
                displayEvidence.appendChild(noEvidenceEl);
            } else {
                sources.forEach((source, index) => {
                    const card = document.createElement('div');
                    card.className = `evidence-card animate-fade-in`;
                    card.style.animationDelay = `${(index + 1) * 0.1}s`;
                    
                    const title = document.createElement('h4');
                    title.className = 'evidence-title';
                    title.textContent = source.title || 'Untitled Source';
                    
                    const snippet = document.createElement('p');
                    snippet.className = 'evidence-snippet';
                    snippet.textContent = source.content || 'No description snippet available.';
                    
                    const link = document.createElement('a');
                    link.className = 'evidence-link';
                    link.href = source.url || '#';
                    link.target = '_blank';
                    link.rel = 'noopener noreferrer';
                    link.innerHTML = 'View Source <i class="fa-solid fa-up-right-from-square" style="font-size: 0.75rem;"></i>';
                    
                    card.appendChild(title);
                    card.appendChild(snippet);
                    card.appendChild(link);
                    displayEvidence.appendChild(card);
                });
            }

            // Render verification result
            const ver = result.verification || {};
            const badge = document.getElementById('verification-badge');
            const percent = document.getElementById('confidence-percentage');
            const bar = document.getElementById('confidence-bar');
            const reason = document.getElementById('verification-reason');
            const factsList = document.getElementById('supported-facts-list');
            const contraSection = document.getElementById('contradictions-section');
            const contraList = document.getElementById('contradictions-list');

            // 1. Update Badge
            badge.textContent = ver.label || 'Needs Verification';
            badge.className = 'verification-badge'; // Reset status classes
            
            // 2. Update Confidence Bar Color Classes
            bar.className = 'confidence-bar-fill'; // Reset status classes
            
            const labelStr = (ver.label || '').toLowerCase();
            if (labelStr.includes('certain') && !labelStr.includes('un')) {
                badge.classList.add('label-certain');
                bar.classList.add('confidence-certain');
            } else if (labelStr.includes('uncertain')) {
                badge.classList.add('label-uncertain');
                bar.classList.add('confidence-uncertain');
            } else {
                badge.classList.add('label-verify');
                bar.classList.add('confidence-verify');
            }

            // 3. Update Confidence Score & Bar Width
            const confVal = ver.confidence !== undefined ? ver.confidence : 0;
            percent.textContent = `${confVal}%`;
            
            // Set initial bar width to 0 first, then update in timeout to trigger CSS transition animation
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = `${confVal}%`;
            }, 50);

            // 4. Update Reason
            reason.textContent = ver.reason || 'No explanation provided.';

            // 5. Update Supported Facts List
            factsList.innerHTML = '';
            const facts = ver.supported_facts || [];
            if (facts.length === 0) {
                const li = document.createElement('li');
                li.textContent = 'No specific supported facts listed.';
                factsList.appendChild(li);
            } else {
                facts.forEach(fact => {
                    const li = document.createElement('li');
                    li.textContent = fact;
                    factsList.appendChild(li);
                });
            }

            // 6. Update Contradictions Section
            const contradictions = ver.contradictions || [];
            if (contradictions.length > 0) {
                contraSection.classList.remove('hidden');
                contraList.innerHTML = '';
                contradictions.forEach(contra => {
                    const li = document.createElement('li');
                    li.textContent = contra;
                    contraList.appendChild(li);
                });
            } else {
                contraSection.classList.add('hidden');
                contraList.innerHTML = '';
            }

            // Show results container with animation (retrigger animation by removing and adding class)
            resultsSection.classList.remove('hidden');
            
            // Scroll results into view smoothly
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error during analysis:', error);
            showError(error.message || "Failed to connect to the backend server.");
        } finally {
            // 5. Reset loading state
            setLoading(false);
        }
    });

    // Helper functions
    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            spinner.classList.remove('hidden');
            btnText.textContent = "Analyzing...";
            analyzeBtn.style.opacity = '0.85';
        } else {
            analyzeBtn.disabled = false;
            spinner.classList.add('hidden');
            btnText.textContent = "Analyze Answer";
            analyzeBtn.style.opacity = '1';
        }
    }

    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
        errorText.textContent = "";
    }

    function formatMarkdown(text) {
        if (!text) return "";
        let safe = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
        
        // Bold: **text** -> <strong>text</strong>
        safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        // Bullet list points: * item -> • item
        safe = safe.replace(/^\*\s+(.*?)$/gm, "• $1");
        // Italics: *text* -> <em>text</em>
        safe = safe.replace(/\*(.*?)\*/g, "<em>$1</em>");
        
        return safe;
    }
});
