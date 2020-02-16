## Inspiration
One of our team members underwent speech therapy as a child, and the therapy helped him gain a sense of independence and self-esteem. In fact, over 7 million Americans, ranging from children with gene-related diseases to adults who suffer from stroke, go through some sort of speech impairment. We wanted to create a solution that could help amplify the effects of in-person treatment by giving families a way to practice at home. We also wanted to make speech therapy accessible to everyone who cannot afford the cost or time to seek institutional help.

## What it does

BeHeard makes speech therapy interactive, insightful, and fun. We present a hybrid text and voice assistant visual interface that guides patients through voice exercises. First, we have them say sentences designed to exercise specific nerves and muscles in the mouth. We use deep learning to identify mishaps and disorders on a word-by-word basis, and show users where exactly they could use more practice. Then, we lead patients through mouth exercises that target those neural pathways. They imitate a sound and mouth shape, and we use deep computer vision to display the desired lip shape directly on their mouth. Finally, when they are able to hold the position for a few seconds, we celebrate their improvement by showing them wearing fun augmented-reality masks in the browser.

## How we built it

- On the frontend, we used Flask, Bootstrap, Houndify and JavaScript/css/html to build our UI. We used Houndify extensively to navigate around our site and process speech during exercises.
- On the backend, we used two Flask servers that split the processing load, with one running the server IO with the frontend and the other running the machine learning.
- On our algorithms side, we used deep_disfluency to identify speech irregularities and filler words and used the IBM Watson speech-to-text (STT) API for a more raw, fine-resolution transcription.
- We used the tensorflow.js deep learning library to extract 19 points representing the mouth of a face. With exhaustive vector analysis, we determined the correct mouth shape for pronouncing basic vowels and gave real-time guidance for lip movements. To increase motivation for the user to practice, we even incorporated AR to draw the desired lip shapes on users mouths, and rewards them with fun masks when they get it right!

## Challenges we ran into

- It was quite challenging to smoothly incorporate voice our platform for navigation, while also being sensitive to the fact that our users may have trouble with voice AI. We help those who are still improving gain competence and feel at ease by creating a chat bubble interface that reads messages to users, and also accepts text and clicks.
- We also ran into issues finding the balance between getting noisy, unreliable STT transcriptions and transcriptions that autocorrected our users’ mistakes. We ended up employing a balance of the Houndify and Watson APIs. We also adapted a dynamic programming solution to the Longest Common Subsequence problem to create the most accurate and intuitive visualization of our users’ mistakes.

## Accomplishments that we are proud of

We’re proud of being one of the first easily-accessible digital solutions that we know of that both conducts interactive speech therapy, while also deeply analyzing our users speech to show them insights. We’re also really excited to have created a really pleasant and intuitive user experience given our time constraints. 

We’re also proud to have implemented a speech practice program that involves mouth shape detection and correction that customizes the AR mouth goals to every user’s facial dimensions.

## What we learned

We learned a lot about the strength of the speech therapy community, and the patients who inspire us to persist in this hackathon. We’ve also learned about the fundamental challenges of detecting anomalous speech, and the need for more NLP research to strengthen the technology in this field.

We learned how to work with facial recognition systems in interactive settings. All the vector calculations and geometric analyses to make detection more accurate and guidance systems look more natural was a challenging but a great learning experience.

## What's next for Be Heard

We have demonstrated how technology can be used to effectively assist speech therapy by building a prototype of a working solution. From here, we will first develop more models to determine stutters and mistakes in speech by diving into audio and language related algorithms and machine learning techniques. It will be used to diagnose the problems for users on a more personal level. We will then develop an in-house facial recognition system to obtain more points representing the human mouth. We would then gain the ability to feature more types of pronunciation practices and more sophisticated lip guidance.
