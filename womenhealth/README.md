# Over 50 Women Heath
## Project Description

My final project, **Over 50 Women Health**, is a web application inspired by my personal experience. After turning 50, I began facing several health-related issues despite having considered myself healthy and active before. I began working with medical doctors to improve my diet before relying on medication. At the same time, I conducted my own research to better understand what I should be eating to improve my health. 

During this process, I repeatedly encountered the concept of “food is medicine” in podcasts featuring medical professionals. It emphasizes the importance of being mindful about what we eat to help prevent illness and support our overall health. This idea resonated with me and motivated me to explore the connection between diet and health more deeply. From this exploration, the idea for my CS50 Web final project emerged. 

The goal of this project is to create a collaborative space where users can share knowledge about health topics and contribute practical recipes based on selected ingredients or components. My target audience is women over the age of 50, particularly those navigating similar health concerns. The platform focuses on delivering up-to-date medical knowledge grounded in credible, peer-reviewed research, especially within the framework of “food is medicine”. By learning how everyday dietary choices impact health, users can better manage or potentially prevent conditions that commonly arise after age 50. Through shared knowledge and community engagement, users are encouraged to take a more proactive role in their well-being. 

The site is designed in two main parts. 

The first part is a **wiki-like system** that allows users to **create a new article or edit existing ones** related to various health topics. The platform includes **role-based permissions** to ensure content quality and proper moderation. When a regular user submits an article, it is automatically placed in a pending state and must go through a peer review process before publication. Editors (users with is_staff status) have the ability to publish articles directly without review. They also have access to a **review dashboard** where they can evaluate pending submissions and decide whether to accept or reject them. The review process itself is conducted outside the platform such as through email communication. 

For each article, the author must select **three to five food components** from a predefined list. For example, an article about cholesterol might include a Mediterranean-style diet as one of its components. These components connect to the second part of the platform: the **recipe contribution system**. 

In the recipe section, users can share home-cooked recipes associated with specific food components. This feature emphasizes cultural exchange and practical learning. For instance, someone like me, with a background in Northeast Asian and North American cuisines, may not be familiar with Mediterranean-style cooking. Through this platform, I can learn from community members who have experience with that cuisine. Similarly, I can contribute recipes – such as different ways to cook tofu – that may be useful to others who are less familiar with this specific food ingredient. 

Editors (is_staff users) also have the ability to create new health topics and add new food components as needed, ensuring that the platform remains flexible and continues to grow with user contributions. 

Overall, this project aims to bridge the gap between medical knowledge and everyday practice by combining evidence-based health information with community-driven recipe sharing.  

## Distinctiveness and Complexity
This project is distinctive because it meaningfully combines multiple existing concepts—health education, recipe sharing, and collaborative content creation—into a single, integrated system with a clear and purposeful structure. While there are platforms focusing on user-generated recipes, collaborative food knowledge, and dietary tracking, none of these platforms connect medical knowledge with practical, community-driven application in a structured way. This project bridges that gap by introducing a “food is medicine” framework, where evidence-based health articles are directly linked to actionable dietary practices.

The project’s complexity lies in both the data modeling and workflow design. I implemented a relational structure in which each health article is associated with three to five predefined food components, and each user-contributed recipe must be linked to exactly one of these components. This creates a layered relationship between abstract medical knowledge and concrete user contributions. Additionally, the project incorporates a role-based permission system with a multi-step moderation workflow: regular users submit content that enters a pending state, while staff users (is_stff) manage a review dashboard to approve or reject submissions. This requires handling different user roles, content states, and administrative interfaces.

Finally, the project is designed with scalability in mind, allowing future additions such as notifications, commenting systems, and search functionality.

## File Structure Overview
models.py
I have the following models: User, Topic, FoodComponent, Entry, Revision, and Recipe

views.py
My views include 
1. login, logout, register to handle users who want to share articles or recipes; 
2. index for the home page listing health topics and recipes displayed based on submitted time;
3. topic_page for entry_detail under each topic;
4. is_staff to assign is_staff status for editors or staffs;
5. topic_entry for is_staff to enter new topics after login;
6. entry_detail to display an article list, selected article content (default display is the first article), 3-5 food components associated to the article, and recipes related to these food components; 
7. create_entry and submit_edit to create a new or edit an existing article, respectively, by sharing the same template file; 
8. review_dashboard to list pending articles for is_staff to approve or reject;
9. review_revision to update revision status and revised article content, 
10. bulk_foodcomponent_entry for is_staff to seed food components;
11. recipe_entry and edit_recipe for users to submit a new or edited recipe based on one food component.

urls.py
Routes URLs to the appropriate views.

templates/
I have HTML templates for rendering pages for each of the above views.

static/
Styles.css

forms.py
I have TopicForm, EntryForm, BulkFoodComponentForm, and RecipeForm for sending topics and food components and for creating and editing articles and recipes.

Requirements.txt
None. 

README.md
Project documentation (this file).

## How to Run the Application
Clone the repository:
git clone <repository_url>
cd project_directory
Create and activate a virtual environment:
`python -m venv venv`
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Apply migrations:
`python manage.py migrate`
Run the development server:
`python manage.py runserver`
Open the application in your browser:
http://127.0.0.1:8000/
