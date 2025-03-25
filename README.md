📝 Django App
A discussion platform where users can:

Create topics (like forum threads)

Add/edit entries (like posts/comments)

Like/dislike content

Manage profiles

🚀 Features
✅ User Profiles – Update username/password
✅ Topics System – Create, view, and manage discussion topics
✅ Entries (Posts) – Add, edit, and comment on entries within topics
✅ Voting – Like/dislike topics
✅ Admin Panel – Full Django admin support

🔧 Setup
Prerequisites
Python 3.8+

Django 4.0+

Database (SQLite)

## 🌐 API/URL Endpoints

| Endpoint                      | Method      | Description                               | Auth Required       |
|-------------------------------|-------------|-------------------------------------------|---------------------|
| `/`                           | `GET`       | Homepage with navbar                      | No                 |
| `/topics/`                    | `GET`       | View your topics                          | Yes                |
| `/all_topics/`                | `GET`       | Browse all public topics                  | No                 |
| `/topics/<int:topic_id>/`     | `GET`       | View specific topic + entries             | No*                |
| `/new_topic/`                 | `POST`      | Create new topic                          | Yes                |
| `/like/<int:topic_id>/`       | `POST`      | Like a topic                              | Yes                |
| `/dislike/<int:topic_id>/`    | `POST`      | Dislike a topic                           | Yes                |
| `/comment/<int:topic_id>/`    | `POST`      | Add comment to topic                      | Yes                |
| `/new_entry/<int:topic_id>/`  | `POST`      | Add new entry to topic                    | Yes                |
| `/edit_entry/<int:entry_id>/` | `POST`      | Edit existing entry                       | Yes (owner only)   |
| `/profile/`                   | `GET`, `PUT`| View/update profile                       | Yes                |
| `/admin/`                     | `GET`       | Django admin panel                        | Yes (admin only)   |

> *Public topics are visible to all; private topics may require auth.

🔐 Authentication
Default Django session-based auth.

Use /admin/ for superuser access.

