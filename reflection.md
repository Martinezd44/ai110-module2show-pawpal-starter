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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
