# salik/portfolio.py

class Portfolio:
    def __init__(self):
        # Basic Information
        self.name = "Salik Uddin"
        self.role = "Full Stack Developer with Advanced Back-end and Front-end Skills"
        self.contact = {
            "phone": "+919044431440",
            "email": "uddinsalik@outlook.com",
            "linkedin": "https://www.linkedin.com/in/salik-uddin/",
            "github": "https://github.com/salik03",
            "website": "https://bento.me/salikuddin"
        }

        # Skills Summary
        self.skills = {
            "Expertise": ["Cloud Computing", "Cybersecurity", "Machine Learning", "AI", "Computer Vision", "Data Analysis", "Blockchain", "Game Development"],
            "Frameworks": ["Flutter", "MERN", "React Native", "Prisma", "Node.js", "Streamlit", "Flask", "FastAPI", "Selenium", "Unity"],
            "Languages": ["Python", "Java", "Dart", "Kotlin", "Swift", "Objective C", "C#", "C++", "JavaScript", "TypeScript"],
            "Tools": ["Git", "Docker", "AWS", "Firebase", "Figma", "Tailwind CSS", "Kaggle", "Kubernetes", "SQL"],
            "Libraries": ["TensorFlow", "TFLite", "OpenCV", "Selenium", "Pandas"],
            "Soft Skills": ["Problem Solving", "Communication", "Time Management", "Leadership", "Teamwork"]
        }

        # Education
        self.education = {
            "institution": "Bennett University - The Times Group",
            "degree": "Bachelor of Technology - Computer Science and Engineering",
            "gpa": 9.2,
            "years": "Sep 2021 - June 2025",
            "specialization": "Cloud, Minor: Innovation and Entrepreneurship"
        }

        # Experience
        self.experience = [
            {
                "title": "Computer Vision Engineer (Consultant)",
                "company": "Samsung Display Noida",
                "duration": "May 2024 – Aug 2024",
                "description": [
                    "Automated calibration of manufacturing robots, saving 4000 work hours annually.",
                    "Achieved high precision with Computer Vision algorithms."
                ],
                "technologies": ["OpenCV", "TensorFlow", "TFLite", "CVAT", "Android", "Java", "Python"]
            },
            # Add other experiences here in a similar format
        ]

        # Projects
        self.projects = [
            {
                "title": "Nom-Nom: Cut Calories, Not Taste",
                "description": "Full-stack app for meal planning and tracking with OCR and nutrition expert chatbot.",
                "technologies": ["React Native", "OCR", "Azure", "Node.js"]
            },
            # Add other projects in similar format
        ]

        # Achievements
        self.achievements = [
            "Finalist, Kavach Cybersecurity Hackathon",
            "Winner, Industry Hackathon for Nom-Nom project",
            "Top 100, IBM TechXchange Hackathon"
        ]

        # Certifications
        self.certifications = [
            "Google: Foundations of Project Management",
            "AWS Academy Graduate - AWS Academy Cloud Architecting"
        ]

    def display(self):
        # Print portfolio information
        print(f"{self.name} - {self.role}\n")
        print("Contact Info:")
        for key, value in self.contact.items():
            print(f"  {key.capitalize()}: {value}")
        print("\nSkills Summary:")
        for category, skills in self.skills.items():
            print(f"  {category}: {', '.join(skills)}")
        print("\nEducation:")
        print(f"  {self.education['institution']} - {self.education['degree']}, GPA: {self.education['gpa']}")
        print("\nExperience:")
        for exp in self.experience:
            print(f"  {exp['title']} at {exp['company']} ({exp['duration']})")
            for desc in exp["description"]:
                print(f"    - {desc}")
        print("\nProjects:")
        for proj in self.projects:
            print(f"  {proj['title']}: {proj['description']}")
        print("\nAchievements:")
        for ach in self.achievements:
            print(f"  - {ach}")
        print("\nCertifications:")
        for cert in self.certifications:
            print(f"  - {cert}")
