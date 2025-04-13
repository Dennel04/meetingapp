# 📅 meetingapp — GraphQL Meeting Management API

**meetingapp** is a lightweight GraphQL API built with **Python**, **Flask**, **Strawberry GraphQL**, and **SQLAlchemy**. It lets you create users, schedule meetings, and manage attendees effortlessly. Designed for learning, prototyping, or as a base for more advanced meeting platforms.  
Made with ❤️ by [Dennel04](https://github.com/Dennel04)

---

## 🚀 Features

- 🧑 Create and manage users
- 📆 Create and manage meetings
- 🔗 Add or remove users from meetings
- 🔍 Query all users and meetings
- ⚡ GraphQL interface with full flexibility
- 🪶 Built with Strawberry (GraphQL for Python)

---

## 📦 Installation

```bash
git clone https://github.com/Dennel04/meetingapp.git
cd meetingapp
pip install -r requirements.txt
python app.py
```
---

## 📬 GraphQL Examples:

➕ Create a user
```
mutation {
  createUser(name: "Ivan", email: "ivan@example.com") {
    id
    name
    email
  }
}
```

➕ Create a meeting
```
mutation {
  createMeeting(title: "Team Sync", time: "14:00", content: "Weekly update") {
    id
    title
    time
    content
  }
}
```

🔗 Add user to a meeting
```
mutation {
  addUserToMeeting(userId: 1, meetingId: 1) {
    id
    title
    attendees {
      id
      name
    }
  }
}

```

🔗 Remove user from a meeting
```
mutation {
  removeUserFromMeeting(userId: 1, meetingId: 1) {
    id
    title
    attendees {
      id
      name
    }
  }
}
```

❌ Delete a user
```
mutation {
  removeUser(userId: 1)
}
```

❌ Delete a meeting
```
mutation {
  removeMeeting(meetingId: 1)
}
```


