📱 Student Social Hub (Full-Stack)A modern, lightweight social media platform built with FastAPI and React JS. This project allows students to register accounts, maintain a profile, and share image-based posts in a community feed.🎯 Project OverviewThis application demonstrates a complete CRUD (Create, Read, Update, Delete) lifecycle with a focus on:Persistent Storage: Moving from simple lists to a permanent SQL Database.Media Management: Handling image uploads and static file serving.Session Logic: Restricting content management so only owners can edit/delete their own posts.🛠️ Technology StackLayerTechnologyDescriptionFrontendUI with Hooks and Functional ComponentsBackendHigh-performance Python API frameworkDatabaseLocal SQL storage via SQLAlchemy ORMStylingCustom modern CSS (no frameworks)📂 Repository StructurePlaintext├── backend/                # FastAPI Server
│   ├── main.py             # API Routes & SQL Logic
│   ├── social_app.db       # SQL Database File
│   └── static/             # Uploaded user images
└── frontend/               # React Application
    ├── src/
    │   ├── App.js          # Logic & Page Routing
    │   └── App.css         # UI Styling
    └── package.json        # Dependencies
⚙️ Setup & Installation1. Backend ConfigurationBashcd backend
pip install fastapi uvicorn sqlalchemy python-multipart
python main.py
