// Update progress bars on input change
function updateProgressBars() {
    const heartRate = document.getElementById('heart-rate').value;
    const bloodOxygen = document.getElementById('blood-oxygen').value;
    
    const hrProgress = ((heartRate - 40) / 160) * 100;
    const o2Progress = ((bloodOxygen - 80) / 20) * 100;
    
    document.getElementById('hr-progress').style.width = `${Math.min(100, Math.max(0, hrProgress))}%`;
    document.getElementById('o2-progress').style.width = `${Math.min(100, Math.max(0, o2Progress))}%`;
}

document.getElementById('heart-rate').addEventListener('input', updateProgressBars);
document.getElementById('blood-oxygen').addEventListener('input', updateProgressBars);

// Gender theme toggle
let selectedGender = 'male';
let selectedDiet = 'non-veg';

document.querySelectorAll('.gender-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedGender = this.getAttribute('data-gender');
        
        if (selectedGender === 'female') {
            document.body.classList.add('female-theme');
        } else {
            document.body.classList.remove('female-theme');
        }
    });
});

document.querySelectorAll('.diet-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.diet-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedDiet = this.getAttribute('data-diet');
    });
});

let hasSearched = false;

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const heartRate = document.getElementById('heart-rate').value;
    const bloodOxygen = document.getElementById('blood-oxygen').value;
    const activityLevel = document.getElementById('activity-level').value;

    const btn = document.getElementById('analyze-btn');
    const btnText = btn.querySelector('.btn-text');
    const originalText = btnText.textContent;
    btnText.textContent = '🔍 Analyzing your data...';
    btn.disabled = true;
    btn.style.opacity = '0.7';

    try {
        const response = await fetch('/api/suggest-meals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                heart_rate: heartRate,
                blood_oxygen: bloodOxygen,
                activity_level: activityLevel,
                gender: selectedGender,
                diet_preference: selectedDiet
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayResults(data);
            if (!hasSearched) {
                btnText.textContent = '🔄 Show More Alternatives';
                hasSearched = true;
            } else {
                btnText.textContent = originalText;
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('😔 Oops! Something went wrong. Let\'s try that again!');
        btnText.textContent = originalText;
    } finally {
        btn.disabled = false;
        btn.style.opacity = '1';
    }
});

function displayResults(data) {
    const resultsSection = document.getElementById('results');
    const analysisCard = document.getElementById('analysis-card');
    const mealsGrid = document.getElementById('meals-grid');

    // Display analysis
    let analysisHTML = `
        <h3>💡 ${data.analysis.energy_state.replace('_', ' ').toUpperCase()}</h3>
        <p>${data.analysis.recommendation}</p>
        <div class="gender-info">🎯 ${data.analysis.gender_info}</div>
    `;

    if (data.analysis.health_alert) {
        analysisHTML += `<div class="health-alert">💙 ${data.analysis.health_alert}</div>`;
    }

    analysisCard.innerHTML = analysisHTML;

    // Display meals
    mealsGrid.innerHTML = data.meals.map((meal, index) => `
        <div class="meal-card">
            <h4>
                <span>🍽️ ${meal.name}</span>
                <span class="meal-type">${meal.type}</span>
            </h4>
            <div class="nutrition-info">
                <div class="nutrition-item">
                    <strong>${meal.calories}</strong>
                    <span>Calories</span>
                </div>
                <div class="nutrition-item">
                    <strong>${meal.protein}g</strong>
                    <span>Protein</span>
                </div>
                <div class="nutrition-item">
                    <strong>${meal.carbs}g</strong>
                    <span>Carbs</span>
                </div>
                <div class="nutrition-item">
                    <strong>${meal.fat}g</strong>
                    <span>Fat</span>
                </div>
                <div class="nutrition-item">
                    <strong>${meal.fiber}g</strong>
                    <span>Fiber</span>
                </div>
            </div>
            ${meal.details ? `
                <button class="info-btn" data-index="${index}">
                    <span class="info-icon">ℹ️</span> More Info
                </button>
                <div class="meal-details" id="details-${index}">
                    <p><strong>📍 Ingredients & Portions:</strong><br>${meal.details}</p>
                    ${meal.recipe ? `<p><strong>👩‍🍳 Recipe:</strong><br>${meal.recipe}</p>` : ''}
                </div>
            ` : ''}
        </div>
    `).join('');

    resultsSection.classList.remove('results-hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Add event listeners to info buttons
    document.querySelectorAll('.info-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            toggleInfo(index, this);
        });
    });
}

function toggleInfo(index, btn) {
    const details = document.getElementById(`details-${index}`);
    
    if (details.classList.contains('show')) {
        details.classList.remove('show');
        btn.innerHTML = '<span class="info-icon">ℹ️</span> More Info';
    } else {
        details.classList.add('show');
        btn.innerHTML = '<span class="info-icon">ℹ️</span> Less Info';
    }
}
