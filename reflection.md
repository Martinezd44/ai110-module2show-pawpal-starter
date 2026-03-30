# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
I want my system to be able for the User to add a pet that they can track what they need to be feed and what execersies they have to do. The app should have daily tasks for the pet so the  User can interact with it and complete them. It will also include a grooming section where it tells the User based of the pet they have when should they have the dog groomed and showered and everything. Also when the user is checking off the tasks should be able to track pets improvment overtime which is getting faster or losing weight or whatever things it can track. When adding it pet has to include the breed , weight , and color.
- What classes did you include, and what responsibilities did you assign to each?
So the main objects and class are going to be the Owner who owns the pet and it contains a name , and preferences. Next is the Pet which containts a name , species or breed, and age. Next is the Task which has the title , duration of minutes , the priority of the task like how important it is and category of what it is, then a completed boolean value. Then we have a Scheduler which has the Owner , contains the pet and tasks then it generates a plan which coorelates to a Daily plan containing all the tasks and how long it will take.  


**b. Design changes**

- Did your design change during implementation?
Yes during implementation it generated it a little differently than the diagram hwoever it implemented eveyrthing it generated from the diagram recarding the priority levels of the tasks and it comes down to the scheduler and daily plan it seemed very stable and it would run efficiently
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My schuedule considers time conflicts and time budget enforcement also Claude and I implemented a priority ordering and sort by time. Also there are not Recurring tasks so if you complete one task it would not show up again in the schueduler. 
- How did you decide which constraints mattered most?
Definiely the Priority ordering because if it is something important like the Pets medication you don't want that showing up in the bottom of the tasks so we made it matter a lot. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
I would say the sort by time and Proiority ordering because you would want to see the pets important tasks they need to complete in benefit of what time it is at and the order of the tasks you need to complete them in.
- Why is that tradeoff reasonable for this scenario?
This is reasonable because if someone is opening the app to check their dogs tasks if some of the tasks they see aren't in pan on what they want then they would be unsatisfied with the app and delete it. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI a lot to help construct the edge cases in this assignment and also help implement the functions into the app.py as importing the class and methods into the app were kind of difficult. I used it a lot in building the app UI as well to make it friendly as possible. 
- What kinds of prompts or questions were most helpful?
I would use the pormpts like for the edge cases. "After viewing the class and methods what edge cases would you suggest are the biggest problems for the app?" I would also view what claude had said and watch it implement it into the code and go over what it has changed before approving it.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
There was one edge cases where I did not agree with and it was changing the pets time and schudule based of the time of day which I did not agree with because that is completely up to the User preference. 
- How did you evaluate or verify what the AI suggested?
I evaluated it because I also tell the AI agent to explain in detail what it has changed and I have the mode where you have to approve and push on what it is changing so I can view and think about if I want to change that given part it had suggested. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
The behaviors I tested was the Sorting correctness that I verift the tasks are in the riht order. Time conflict detection that verify the scheduler flags duplicate times. Recurrence logic that confirms that making a daily task complete create a new tasks for the following day. 
- Why were these tests important?
These tests were important because it was showing off the core features of the app and what the User downloads the app for. Without these tests we can't really find out if our core function and methods work which would defeat the purpose of our app. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
 I am pretty confident that my scheudler works correctly mainly because I ran the tests with the given test cases which were all green and I ran the app myself in streamlit and tested it for a little and saw that it was working as intended. 
- What edge cases would you test next if you had more time?
 I feel like after working on this for 3 hours I would say I covered all of the edge cases because I have also had AI lookover and tell me if there is any other edge cases and it didn't really comeback with any so I would say most of them are covered. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I would say I am satisfied with how well the app works and How i can add the pets and owners and create the schedule pretty efficiently and well. Which I am happy with and satisfied with because it took a while to implement it. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would redesign the UI of the app because it seems a little wonky but the core features of the app work really well. Also maybe fix the reposnes in the App as well. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I would say you would have to take things step by step especially while working with an AI agent on a project. Like if I just tell it to do everything at once it will have a lot of mistakes and it would be very sloppy. However if I take my time with making a project and go step by step with the AI and build like little blocks overtime you can create something thats well constructed and well polished like the app. 
