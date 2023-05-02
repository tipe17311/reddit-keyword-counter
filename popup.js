document.getElementById('keyword-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const keyword = document.getElementById('keyword').value;
  
    // Define your subreddit names, start_date, and end_date here
    const subredditNames = ['AskReddit', 'worldnews', 'gaming'];
    const startDate = '2023-04-01';
    const endDate = '2023-04-30';
  
    const response = await fetch('http://localhost:5000', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        keyword,
        subreddit_names: subredditNames,
        start_date: startDate,
        end_date: endDate
      })
    });
    
  
    const result = await response.json();
  
    // Update the result element with the response from the backend server
    document.getElementById('result').innerHTML = JSON.stringify(result);
});
