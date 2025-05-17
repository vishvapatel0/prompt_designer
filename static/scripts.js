document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded');
    
    // Initialize tab functionality
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tabId = button.getAttribute('data-tab');
            
            // Deactivate all buttons and tabs
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            // Activate selected button and tab
            button.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // Star rating functionality
    function initStarRating(container, callback) {
        if (!container) return;
        
        const stars = container.querySelectorAll('.star');
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const value = parseInt(this.getAttribute('data-value'));
                
                // Update visual state
                stars.forEach(s => {
                    s.classList.remove('active');
                    if (parseInt(s.getAttribute('data-value')) <= value) {
                        s.classList.add('active');
                    }
                });
                
                // Call callback function with the rating value
                if (callback) callback(value);
            });
        });
    }

    // Initialize star ratings
    let effectivenessRating = 0;
    let clarityRating = 0;
    let currentQueryId = null;
    
    initStarRating(document.getElementById('effectivenessRating'), (rating) => {
        effectivenessRating = rating;
        console.log('Effectiveness rating:', rating);
    });
    
    initStarRating(document.getElementById('clarityRating'), (rating) => {
        clarityRating = rating;
        console.log('Clarity rating:', rating);
    });

    // Handle query submission
    const submitQueryBtn = document.getElementById('submitQuery');
    if (submitQueryBtn) {
        submitQueryBtn.addEventListener('click', async function() {
            const queryInput = document.getElementById('queryInput');
            const query = queryInput.value.trim();
            
            if (!query) {
                alert('Please enter a query');
                return;
            }
            
            // Update UI to show loading state
            const statusElement = document.getElementById('status');
            statusElement.textContent = 'Processing your query... (this may take a minute)';
            submitQueryBtn.disabled = true;
            
            try {
                // Make API call to backend
                const response = await fetch('/api/optimize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }
                
                const result = await response.json();
                console.log('API response:', result);
                
                // Store the query ID for feedback submission
                currentQueryId = result.query_id;
                
                // Update UI with results
                document.getElementById('researchOutput').textContent = result.research || 'No research data available';
                document.getElementById('promptOutput').textContent = result.optimized_prompt || 'No prompt data available';
                document.getElementById('evaluationOutput').textContent = result.evaluation || 'No evaluation data available';
                
                // Show results section
                document.getElementById('results').style.display = 'block';
                statusElement.textContent = '';
                
                // Reset rating values for new query
                effectivenessRating = 0;
                clarityRating = 0;
                document.querySelectorAll('.star').forEach(s => s.classList.remove('active'));
                document.getElementById('feedbackComments').value = '';
                
            } catch (error) {
                console.error('Error during API call:', error);
                statusElement.textContent = 'Error: ' + error.message;
            } finally {
                submitQueryBtn.disabled = false;
            }
        });
    }

    // Handle feedback submission
    const submitFeedbackBtn = document.getElementById('submitFeedback');
    if (submitFeedbackBtn) {
        submitFeedbackBtn.addEventListener('click', async function() {
            if (!currentQueryId) {
                alert('No active query to provide feedback for');
                return;
            }
            
            if (effectivenessRating === 0 || clarityRating === 0) {
                alert('Please provide ratings for both effectiveness and clarity');
                return;
            }
            
            const comments = document.getElementById('feedbackComments').value;
            
            // Update UI to show loading state
            submitFeedbackBtn.disabled = true;
            submitFeedbackBtn.textContent = 'Submitting...';
            
            try {
                const response = await fetch('/api/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query_id: currentQueryId,
                        effectiveness_rating: effectivenessRating * 2, // Scale to 1-10 
                        clarity_rating: clarityRating * 2, // Scale to 1-10
                        comments: comments
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }
                
                const result = await response.json();
                console.log('Feedback response:', result);
                
                // Update UI to show success
                submitFeedbackBtn.textContent = 'Feedback Submitted!';
                setTimeout(() => {
                    submitFeedbackBtn.textContent = 'Submit Feedback';
                    submitFeedbackBtn.disabled = false;
                }, 2000);
                
            } catch (error) {
                console.error('Error submitting feedback:', error);
                submitFeedbackBtn.textContent = 'Error';
                setTimeout(() => {
                    submitFeedbackBtn.textContent = 'Submit Feedback';
                    submitFeedbackBtn.disabled = false;
                }, 2000);
            }
        });
    }

    // Add copy to clipboard functionality
    const copyPromptBtn = document.getElementById('copyPrompt');
    if (copyPromptBtn) {
        copyPromptBtn.addEventListener('click', function() {
            const promptText = document.getElementById('promptOutput').textContent;
            navigator.clipboard.writeText(promptText)
                .then(() => {
                    copyPromptBtn.textContent = 'Copied!';
                    setTimeout(() => {
                        copyPromptBtn.textContent = 'Copy to Clipboard';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Could not copy text: ', err);
                    alert('Failed to copy to clipboard');
                });
        });
    }
});