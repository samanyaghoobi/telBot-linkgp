
# 📦 Telegram Link Management Bot - Project Structure

This bot manages a Telegram link-sharing channel using a scheduled and permission-based system. Below is the structure of the project and what each component is responsible for.

---

## 📁 Project Directory Structure

```
my_link_bot/
│
├── main.py                         # Entry point to run the bot
├── config.py                       # Configuration (tokens, DB, etc.)
├── .env                            # Environment variables (optional)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── app/
│   ├── __init__.py
│   ├── telegram/                   # Telegram bot logic
│   │   ├── bot_instance.py         # Bot creation and setup
│   │   ├── filters/                # Custom filters like is_admin
│   │   │   └── is_admin.py
│   │   ├── handlers/               # Message/callback handlers
│   │   │   ├── user.py             # End-user features
│   │   │   ├── admin.py            # Admin panel commands
│   │   │   ├── banner.py           # Banner creation/view
│   │   │   ├── schedule.py         # Link reservation system
│   │   │   └── payment.py          # Payments and points
│   │   ├── middlewares/           # Membership validation
│   │   │   └── check_membership.py
│   │   ├── utils/                  # Shared tools and logic
│   │   │   ├── logger.py           # Log system with restart alerts
│   │   │   ├── keyboard.py         # Telegram keyboards
│   │   │   └── time_tools.py       # Time-related utilities
│   │   └── tasks/                  # Background tasks (cron-style)
│   │       ├── scheduler.py
│   │       └── dispatch_links.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py               # MySQL connection logic
│   ├── models.py                   # Database schema definitions
│   ├── queries/                    # SQL queries per module
│   │   ├── user_queries.py
│   │   ├── reservation_queries.py
│   │   └── admin_queries.py
│
├── logs/
│   └── latest.log                  # Bot logs
│
└── tests/
    └── test_schedule.py            # Tests for reservation features
```

---

## 📌 Highlights

- **Separation of Concerns**: All modules are logically separated and independently testable.
- **Custom Filters & Middlewares**: For checking admin rights and channel membership.
- **Scheduled Link Posting**: Users can reserve time slots; system posts links at reserved times.
- **Payment & Points System**: Users earn points from payments and can redeem them later.
- **Error Logging & Notification**: Crashes are logged and admins are notified on restart.
- **Extensible**: New handlers or features can be added easily without touching core logic.

---

## ✅ Next Steps

You can begin with setting up:
- `config.py` and `.env`
- The bot instance and `/start` command
- Admin/user differentiation via custom filter
- Membership checker for the main channel

More functionality will be added incrementally.
