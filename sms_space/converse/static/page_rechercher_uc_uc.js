document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const resultContainer = document.getElementById('resultContainer');

    input.addEventListener('input', function () {
        const query = input.value;

        fetch(`/ajax/rechercher/?q=${encodeURIComponent(query)}&user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                resultContainer.innerHTML = '';
                if (data.resultats.length === 0) {
                    resultContainer.innerHTML = '<p style="padding:12px;">😕 Aucun utilisateur trouvé.</p>';
                } else {
                    data.resultats.forEach(user => {
                        const div = document.createElement('div');

                        const pseudoSpan = document.createElement('span');
                        pseudoSpan.className = 'pseudo';
                        pseudoSpan.textContent = user.pseudo;

                        const btn = document.createElement('button');
                        btn.className = 'btn-demande';
                        btn.textContent = 'Envoyer une demande';
                        btn.onclick = () => {
                            alert(`Demande envoyée à ${user.pseudo}`);
                        };

                        div.appendChild(pseudoSpan);
                        div.appendChild(btn);
                        resultContainer.appendChild(div);
                    });
                }
            });
    });
});
