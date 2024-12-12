document.querySelectorAll('input[name="priority"]').forEach((radio) => {
    radio.addEventListener('change', (event) => {
        const selectedPriority = event.target.value;
        console.log(`Selected Priority: ${selectedPriority}`);
    });
});
