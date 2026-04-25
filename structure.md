Brew-Time/
├── app.py                  # Application factory, routes, and main entry point
├── models.py               # Database models (Product, Order, OrderItem)
├── init_db.py              # Script to create tables and populate products
├── requirements.txt        # List of Python dependencies
├── templates/
│   ├── base.html           # Common layout (Bootstrap navbar)
│   ├── index.html          # Customer menu and cart page
│   ├── track.html          # Customer order tracking page
│   └── barista.html        # Staff dashboard with order queue
├── static/
│   ├── style.css           # Custom styles
│   └── script.js           # Common JavaScript functions
├── tests/
│   └── test_app.py         # Unit and integration tests
└── diagrams/               # Original UML diagram files