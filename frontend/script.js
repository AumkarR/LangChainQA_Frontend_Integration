import bot from './assets/bot.svg' //Importing logos for the user and bot logos
import user from './assets/user.svg'

const form = document.querySelector('form') //Accessing the form and the chat container from the index.html file
const chatContainer = document.querySelector('#chat_container')

let loadInterval

function loader(element) { //Adding a loading functionaility (...) while the backend is working to get a response
    element.textContent = ''
    loadInterval = setInterval(() => {
        element.textContent += '.';
        if (element.textContent === '....') {
            element.textContent = '';
        }
    }, 300);
}

function typeText(element, text) { //Instead of showing all of the response text at once, showing the text as it is being typed similar to how ChatGPT does
    let index = 0
    let interval = setInterval(() => {
        if (index < text.length) {
            element.innerHTML += text.charAt(index)
            index++
        } else {
            clearInterval(interval)
        }
    }, 20)
}

function generateUniqueId() { //Generating a uniqueID for each response to ensure that the typeText() is not executed everytime a new response is generated
    const timestamp = Date.now();
    const randomNumber = Math.random();
    const hexadecimalString = randomNumber.toString(16);
    return `id-${timestamp}-${hexadecimalString}`;
}

function chatStripe(isAi, value, uniqueId) { //Creating a visual difference between the user's and bot's response instead of having a constant screen
    return (
        `
        <div class="wrapper ${isAi && 'ai'}">
            <div class="chat">
                <div class="profile">
                    <img 
                      src=${isAi ? bot : user} 
                      alt="${isAi ? 'bot' : 'user'}" 
                    />
                </div>
                <div class="message" id=${uniqueId}>${value}</div>
            </div>
        </div>
    `
    )
}

const handleSubmit = async (e) => { //Handing the submit feature
    e.preventDefault()
    const data = new FormData(form)
    chatContainer.innerHTML += chatStripe(false, data.get('prompt')) //Getting teh prompt from the user's input box, and clearing the response
    form.reset()

    const uniqueId = generateUniqueId() //Generating a uniqueID for the bot's response
    chatContainer.innerHTML += chatStripe(true, " ", uniqueId)
    chatContainer.scrollTop = chatContainer.scrollHeight;
    const messageDiv = document.getElementById(uniqueId)
    loader(messageDiv) //Executing the loader

    const response = await fetch('http://localhost:2784/query', { //Sending a post request to the backend Flask server, and storing the response
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: data.get('prompt')
        })    
    })

    clearInterval(loadInterval)
    messageDiv.innerHTML = " "

    if (response.ok) { //Checking if the response is appropriate, and typing out the text
        const data = await response.json();
        const parsedData = data.bot.trim() // trims any trailing spaces/'\n' 
        typeText(messageDiv, parsedData)
    } else { //Handling the case where the response isn't as expected
        const err = await response.text()
        messageDiv.innerHTML = "Something went wrong"
        alert(err)
    }
}


form.addEventListener('submit', handleSubmit) //Calling the handleSubmit function when the send button is clicked or if the enter key is pressed
form.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        handleSubmit(e)
    }
})

//Credit for front-end code: Adrian Hajdin
