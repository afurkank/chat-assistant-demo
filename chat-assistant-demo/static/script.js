document.addEventListener('DOMContentLoaded', () => {
    const fillForm = document.getElementById('fillForm');
    const changeBackground = document.getElementById('changeBackground');
    const gender = document.getElementById('gender');
    const personality = document.getElementById('personality');
    const avatarImage = document.getElementById('avatarImage');
    const formLogo = document.getElementById('formLogo');
    const formTitle = document.getElementById('formTitle');

    fillForm.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        if (formId) {
            // Update form info (logo and title) immediately
            fetch('/update_form_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ formID: formId }),
            })
            .then(response => response.json())
            .then(data => {
                formTitle.textContent = data.title;
                
                if (data.logoType === 'svg+xml') {
                    // For SVG, set the innerHTML directly
                    formLogo.innerHTML = data.logo;
                } else {
                    // For other image types, use base64 encoding
                    formLogo.src = `data:image/${data.logoType};base64,${data.logo}`;
                }
            })
            .catch((error) => {
                console.error('Error updating form info:', error);
            });

            // Update background
            fetch('/update_background', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ formID: formId }),
            })
            .then(response => response.json())
            .then(data => {
                document.body.style.backgroundImage = `url(data:image/png;base64,${data.background})`;
            })
            .catch((error) => {
                console.error('Error updating background:', error);
            });

            // Update avatar
            fetch('/update_avatar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ formID: formId, gender: gender.value}),
            })
            .then(response => response.json())
            .then(data => {
                avatarImage.src = `data:image/png;base64,${data.avatar}`;
            })
            .catch((error) => {
                console.error('Error updating avatar:', error);
            });
        } else {
            console.log('Please enter a Form ID');
        }
    });

    function updateAvatar() {
        const formId = document.getElementById('formId').value;
        fetch('/update_avatar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formID: formId, gender: gender.value }),
        })
        .then(response => response.json())
        .then(data => {
            avatarImage.src = `data:image/png;base64,${data.avatar}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    gender.addEventListener('change', updateAvatar);
    // personality.addEventListener('change', updateAvatar); this is related to chat agent

    changeBackground.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        fetch('/update_background', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formID: formId }),
        })
        .then(response => response.json())
        .then(data => {
            document.body.style.backgroundImage = `url(data:image/png;base64,${data.background})`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});