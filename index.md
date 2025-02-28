# TODO App - Basic Design

## Overview

This document outlines the basic design of the TODO application.

## Data Model

### Category

*   `id` (Integer, Primary Key)
*   `name` (String(50), Not Nullable)

### Todo

*   `id` (Integer, Primary Key)
*   `content` (String(200), Not Nullable)
*   `date_created` (DateTime, Default: datetime.utcnow)
*   `deadline` (Date, Nullable)
*   `completed` (Boolean, Default: False)
*   `category_id` (Integer, ForeignKey('category.id'), Not Nullable)

## UI Design

The application will use a Kanban-style board with the following columns:

*   TODO: Tasks that are not yet completed and have a deadline that is today or in the past.
*   Upcoming: Tasks that are not yet completed and have a deadline in the future.
*   Completed: Tasks that are marked as complete.

Each task will display:

*   Content
*   Deadline (if applicable)
*   Category

## Functionality

*   Adding new tasks
*   Deleting tasks
*   Marking tasks as complete/incomplete
*   Categorizing tasks