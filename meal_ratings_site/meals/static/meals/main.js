function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('sort-select');
    const elementContainer = document.getElementById('meals-container');
    

    sortSelect.addEventListener('change', function () {
        const selectedValue = sortSelect.value;
        console.log(selectedValue);
        fetch('/morning/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // これは正しいヘッダー名
                'X-CSRFToken': getCookie('csrftoken') // CSRFトークンの取得
            }
        })
            .then(response => response.json())
            .then(data => {
                const querySetData = data.data;
                let sorted_html = '';

                querySetData.forEach(element => {
                    sorted_html += `
                        <div class="uk-card uk-card-default uk-grid-collapse uk-child-width-1-2@s uk-margin" uk-grid>
                            <div class="uk-card-media-left uk-cover-container">
                                <img src="/media/${ element.imageUrl }" alt="" uk-cover>
                                <canvas width="600" height="400"></canvas>
                            </div>
                            <div class="uk-flex uk-flex-center">
                                <div class="uk-card-body uk-flex uk-flex-column uk-flex-around uk-text-center">
                                    <h3 class="uk-card-title">${ element.name }</h3>
                                    <div>
                                        <p>Avg Score: ${ element.avgRating }</p>
                                        <p>Votes: ${ element.numberOfVotes}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                console.log(sorted_html)
                elementContainer.innerHTML = sorted_html;
            })
            .catch(error => console.error('Fetch error:', error));
    });


});


