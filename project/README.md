# Yum Willow - Recipe Sharing Platform

## Overview

Yum Willow is a recipe sharing platform inspired by the warm, cozy aesthetics of Studio Ghibli food scenes. Users can browse community recipes, maintain their own recipe collections, and enjoy an artsy interface that celebrates cooking. The platform lets everyone view all recipes.

## Technical Stack

- Backend: Python with Flask framework
- Database: SQLite (SQL)
- Frontend: HTML, CSS, JavaScript
- Session Management: Flask sessions for authentication

## File Descriptions

### app.py

The main Flask application file that handles all routing and database interactions. Key routes include:

- **Authentication routes** (`/register`, `/login`, `/logout`): Manages user registration with password hashing, login verification, and session management
- **Recipe routes** (`/`, `/add`, `/edit/<id>`, `/delete/<id>`): Handles displaying recipes, adding new ones through forms, editing existing recipes with ownership verification, and deleting recipes with authorization checks
- **Detail route** (`/recipe/<id>`): Displays full recipe information including ingredients, instructions, cooking time, and author details

The file uses a `login_required` decorator to protect routes requiring authentication by checking session data.

### helpers.py

Contains the `login_required` decorator that wraps route functions to ensure only authenticated users can access protected pages. Unauthenticated users are redirected to the login page.

### schema.sql

Defines the database structure with four tables:

- **users**: Stores id, username (unique), and password hash
- **recipes**: Stores id, user_id (foreign key), title, description, prep_time, cook_time, and servings
- **ingredients**: Stores id, recipe_id (foreign key), ingredient name, and amount. Uses ON DELETE CASCADE to automatically remove ingredients when their recipe is deleted
- **instructions**: Stores id, recipe_id (foreign key), step_number, and instruction text.

Foreign key relationships ensure data integrity between users and recipes, and between recipes and their ingredients/instructions.


### Templates

#### layout.html

Base template extended by all pages. Contains the navigation bar, footer, and CSS/JavaScript imports. The navbar dynamically displays different options based on authentication status.

#### home.html

Main landing page visible to all users regardless of login status. Includes a description of what the website does.

#### login.html and register.html

Authentication forms with client-side validation. Register includes username, password, and confirmation fields. Both display server-side error messages when needed.

#### add.html and edit.html

Forms for creating and modifying recipes with fields for title, description, ingredients, instructions, cooking time, servings, and prep time. Before deletion, the form asks users to confirm they want to proceed. Edit and delete buttons only appear if the current logged-in user_id matches the recipe author.

### recipe.html

Detailed single recipe view showing all information. Authors see edit and delete buttons for their own recipes.

### style.css

Creates the Studio Ghibli aesthetic with warm color palettes, rounded corners, and subtle shadows.

## Design Choices

### SQL Database

SQL allows for a relational structure where recipes belong to users, which fits perfectly with a relational database. Foreign key constraints ensure data integrity, and SQL queries make filtering recipes straightforward. Delete Cascade was added to the ingredients and instructions tables to prevent foreign key conflicts when deleting recipes.

### Edit/Delete Permissions

Only recipe authors can edit or delete their own recipes. I implemented backend verification to prevent users from accessing or modifying other people's recipes through URL manipulation.

### Session-Based Authentication

Flask's built-in session management is simpler than token-based authentication for browser applications. Sessions are secure, handled server-side, and integrate smoothly with Flask.

### Web Layout

The layout gives a "tablecloth" and recipe book feeling, creating an interface that resonates with the purpose of browsing and sharing recipes.

### Studio Ghibli Aesthetic

The warm, nostalgic design creates an inviting atmosphere that makes recipe browsing feel comforting rather than clinical.


### Video Demo Link

https://youtu.be/zRBHg7mqROM
