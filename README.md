# Fight Covid-19 Django Project
### Introduction
Fight Covid-19 is an online discussion site where people can hold conversations on Covid-19 during the pandemic in the form of posted messages. There are two sections, including articles and questions on Covid-19. In the articles section, users can publish and comment on posts such as modes of transmission for Covid-19 that help people better protect themselves and fight Covid-19. We count page views for each article, including external traffic, as a signal of popularity. Meanwhile, users can ask and answer Covid-19 related questions such as grocery store inventories, restaurants doing taking out. They can also vote for the best answers based on whatever criteria they choose. We enable a tag system for both sections that let site administrators attach labels. Everyone who wants to join is asked to sign up (register with a single click) or do a social login. 

We plan to have three applications for our project, including “Article”, “Microblog”, “Q&A”. We have finished the “Article” and “Q&A” application.

### Article’s Model
There are two data models within Article application -- Article and Comment. We have one Many-to-Many relationship and two Many-to-One relationships in this application. One article could have many comments; one owner could also have many comments. Two Many-to-One relationships are under the class of Comment. Many-to-Many relationship is through Comment, and it is under the class of Article. 

### Q&A’s Model
We have three data models within Q&A application -- Question, Tag and Answer. Question stores question related information, including owner, edit date, title along with question content. Tag stores keywords of the question while in Answer, we have the solvers’ names and content of answers. Many-to-one relationship between Answer and Question. Many-to-Many relationship between Question and Tag: one question could have multiple tags; one tag could also have many questions. 


This is the project for SI 664 final assignment. https://si664project.pythonanywhere.com/

Contributor: @Siyinz @Anranmg
